"""
Pipeline de ingesta de juegos a MongoDB
Flujo: Steam API → GG.deals API (EUR) → MongoDB
"""

import sys
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import time

# Añadir paths
chatbot_path = Path(__file__).parent / 'chatbot'
sys.path.insert(0, str(chatbot_path))

from dotenv import load_dotenv
load_dotenv(chatbot_path / '.env')

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from src.ingestion.steam_client import SteamAPIClient
from src.ingestion.ggdeals_client import GGDealsAPIClient


class GameIngestionPipeline:
    """Pipeline para ingestar juegos desde Steam y GG.deals a MongoDB"""
    
    def __init__(self, mongo_uri: str, db_name: str, ggdeals_api_key: str):
        """
        Args:
            mongo_uri: URI de conexión a MongoDB
            db_name: Nombre de la base de datos
            ggdeals_api_key: API key de GG.deals
        """
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client[db_name]
        self.games_collection = self.db['games']
        
        # Crear índice único en steam_id
        self.games_collection.create_index('steam_id', unique=True)
        
        # Clientes API
        self.steam_client = SteamAPIClient()
        self.ggdeals_client = GGDealsAPIClient(api_key=ggdeals_api_key)
        
    def enrich_game_with_prices(self, game_data: Dict, region: str = "eu") -> Dict:
        """
        Enriquece datos de Steam con precios de GG.deals
        
        Args:
            game_data: Datos del juego desde Steam
            region: Región para precios (eu = euros, us = dólares)
        
        Returns:
            Juego enriquecido con precios
        """
        steam_id = game_data["steam_id"]
        
        try:
            price_data = self.ggdeals_client.get_game_prices(steam_id, region=region)
            
            if price_data:
                game_data.update({
                    "ggdeals_url": price_data.get("url", ""),
                    "current_price_retail": price_data.get("current_retail", 0.0),
                    "current_price_keyshop": price_data.get("current_keyshops", 0.0),
                    "historical_low_retail": price_data.get("historical_retail", 0.0),
                    "historical_low_keyshop": price_data.get("historical_keyshops", 0.0),
                    "currency": price_data.get("currency", "EUR"),
                    "price_region": region,
                    "price_updated_at": datetime.now().isoformat(),
                })
            else:
                # Juego sin precios disponibles
                game_data.update({
                    "ggdeals_url": "",
                    "current_price_retail": None,
                    "current_price_keyshop": None,
                    "historical_low_retail": None,
                    "historical_low_keyshop": None,
                    "currency": "EUR",
                    "price_region": region,
                    "price_updated_at": datetime.now().isoformat(),
                })
                
        except Exception as e:
            print(f"   [AVISO] Error obteniendo precios para {game_data['name']}: {e}")
            # Mantener sin precios
            game_data["price_updated_at"] = datetime.now().isoformat()
        
        # Añadir timestamp de ingesta
        game_data["ingested_at"] = datetime.now().isoformat()
        
        return game_data
    
    def fetch_and_enrich_batch(self, steam_ids: List[int], region: str = "eu") -> List[Dict]:
        """
        Obtiene datos de Steam y los enriquece con precios en batch
        
        Args:
            steam_ids: Lista de Steam App IDs
            region: Región para precios
        
        Returns:
            Lista de juegos enriquecidos
        """
        enriched_games = []
        
        print(f"\n[STEAM] Obteniendo datos de {len(steam_ids)} juegos desde Steam...")
        
        # Obtener datos de Steam
        for i, steam_id in enumerate(steam_ids, 1):
            try:
                game_data = self.steam_client.get_app_details(steam_id)
                
                if game_data:
                    print(f"   [{i}/{len(steam_ids)}] [OK] {game_data['name']}")
                    enriched_games.append(game_data)
                else:
                    print(f"   [{i}/{len(steam_ids)}] [AVISO] Steam ID {steam_id}: No disponible")
                    
                # Pequeña pausa para no saturar API
                time.sleep(0.3)
                
            except Exception as e:
                print(f"   [{i}/{len(steam_ids)}] [ERROR] Error con Steam ID {steam_id}: {e}")
        
        if not enriched_games:
            print("[ERROR] No se obtuvieron juegos desde Steam")
            return []
        
        print(f"\n[GGDEALS] Obteniendo precios de GG.deals ({region.upper()})...")
        
        # Obtener precios en batch de GG.deals
        steam_ids_to_fetch = [g["steam_id"] for g in enriched_games]
        
        try:
            batch_prices = self.ggdeals_client.get_prices_by_steam_ids(
                steam_ids_to_fetch, 
                region=region
            )
            
            print(f"   [OK] Precios obtenidos para {len(batch_prices)} juegos")
            
            # Enriquecer cada juego con sus precios
            for game in enriched_games:
                steam_id = str(game["steam_id"])
                
                if steam_id in batch_prices:
                    price_data = batch_prices[steam_id]
                    prices = price_data.get("prices", {})
                    
                    # Convertir precios a float
                    def to_float(value):
                        if value is None:
                            return None
                        try:
                            return float(value)
                        except (ValueError, TypeError):
                            return None
                    
                    game.update({
                        "ggdeals_url": price_data.get("url", ""),
                        "current_price_retail": to_float(prices.get("currentRetail")),
                        "current_price_keyshop": to_float(prices.get("currentKeyshops")),
                        "historical_low_retail": to_float(prices.get("historicalRetail")),
                        "historical_low_keyshop": to_float(prices.get("historicalKeyshops")),
                        "currency": prices.get("currency", "EUR"),
                        "price_region": region,
                        "price_updated_at": datetime.now().isoformat(),
                    })
                else:
                    # Sin precios disponibles
                    game.update({
                        "ggdeals_url": "",
                        "current_price_retail": None,
                        "current_price_keyshop": None,
                        "historical_low_retail": None,
                        "historical_low_keyshop": None,
                        "currency": "EUR",
                        "price_region": region,
                        "price_updated_at": datetime.now().isoformat(),
                    })
                
                game["ingested_at"] = datetime.now().isoformat()
                
        except Exception as e:
            print(f"   [AVISO] Error obteniendo precios en batch: {e}")
            # Continuar sin precios
            for game in enriched_games:
                game["ingested_at"] = datetime.now().isoformat()
        
        return enriched_games
    
    def insert_games(self, games: List[Dict]) -> Dict[str, int]:
        """
        Inserta juegos en MongoDB
        
        Args:
            games: Lista de juegos enriquecidos
        
        Returns:
            Estadísticas de inserción
        """
        stats = {
            "inserted": 0,
            "duplicated": 0,
            "errors": 0
        }
        
        print(f"\n[MONGODB] Insertando {len(games)} juegos en MongoDB...")
        
        for game in games:
            try:
                self.games_collection.insert_one(game)
                stats["inserted"] += 1
                print(f"   [OK] {game['name']}")
                
            except DuplicateKeyError:
                stats["duplicated"] += 1
                print(f"   [DUP] {game['name']} (ya existe)")
                
            except Exception as e:
                stats["errors"] += 1
                print(f"   [ERROR] Error insertando {game.get('name', 'Unknown')}: {e}")
        
        return stats
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de la colección"""
        total = self.games_collection.count_documents({})
        with_prices = self.games_collection.count_documents({
            "current_price_retail": {"$ne": None}
        })
        
        return {
            "total_games": total,
            "games_with_prices": with_prices,
            "games_without_prices": total - with_prices
        }
    
    def close(self):
        """Cierra conexión a MongoDB"""
        self.mongo_client.close()


def get_popular_steam_ids() -> List[int]:
    """
    Devuelve lista de 120+ Steam App IDs unicos de juegos populares
    Incluye juegos de diferentes generos y rangos de precio
    """
    steam_ids = [
        # AAA Recientes (2020-2026)
        1091500,  # Cyberpunk 2077
        1245620,  # Elden Ring
        1174180,  # Red Dead Redemption 2
        1938090,  # Call of Duty: Modern Warfare II
        2358720,  # Black Myth: Wukong
        1888930,  # Manor Lords
        1623730,  # Palworld
        1086940,  # Baldur's Gate 3
        2050650,  # Starfield
        990080,   # Hogwarts Legacy
        1203220,  # NARAKA: BLADEPOINT
        1888160,  # Balatro
        2321470,  # The Last of Us Part I
        2050650,  # Resident Evil 4
        813780,   # Age of Empires IV
        1063730,  # New World
        1172620,  # Forza Horizon 5
        2239550,  # Armored Core VI
        
        # Clasicos populares
        292030,   # The Witcher 3
        271590,   # GTA V
        413150,   # Stardew Valley
        374320,   # DARK SOULS III
        489830,   # The Elder Scrolls V: Skyrim
        367520,   # Hollow Knight
        548430,   # Deep Rock Galactic
        892970,   # Valheim
        1449560,  # Hades
        620,      # Portal 2
        8930,     # Sid Meier's Civilization V
        570940,   # DARK SOULS Remastered
        
        # Competitivos/Multijugador
        730,      # Counter-Strike 2
        570,      # Dota 2
        578080,   # PUBG: BATTLEGROUNDS
        1172470,  # Apex Legends
        359550,   # Rainbow Six Siege
        252490,   # Rust
        1966720,  # Overwatch 2
        1517290,  # Battlefield 2042
        1811260,  # Days Gone
        2357570,  # THE FINALS
        
        # Survival/Craft
        346110,   # ARK: Survival Evolved
        251570,   # 7 Days to Die
        418370,   # Subnautica
        268500,   # XCOM 2
        264710,   # Subnautica Below Zero
        1282100,  # Remnant II
        1928980,  # Nightingale
        2073850,  # Pacific Drive
        
        # Estrategia
        236390,   # War Thunder
        281990,   # Stellaris
        394360,   # Hearts of Iron IV
        1158310,  # Crusader Kings III
        466560,   # RimWorld
        261550,   # Mount & Blade II: Bannerlord
        1966720,  # Total War: WARHAMMER III
        813780,   # Age of Empires IV
        
        # Indie populares
        435150,   # Divinity: Original Sin 2
        975370,   # Dwarf Fortress
        1446780,  # Monster Hunter Rise
        504230,   # Celeste
        253230,   # A Hat in Time
        774241,   # Castle Crashers
        253230,   # Cuphead
        1145360,  # Hades
        1203220,  # ULTRAKILL
        
        # Simulacion
        427520,   # Factorio
        244850,   # Space Engineers
        255710,   # Cities: Skylines
        304930,   # Unturned
        365960,   # BeamNG.drive
        739630,   # Phasmophobia
        1091500,  # Microsoft Flight Simulator
        
        # Accion/Aventura
        1144200,  # Ready or Not
        1517290,  # Dying Light 2
        287700,   # METAL GEAR SOLID V
        1174180,  # God of War
        750920,   # Shadow of the Tomb Raider
        883710,   # Days Gone
        1817230,  # Satisfactory
        
        # RPG
        1687950,  # Persona 5 Royal
        1086940,  # Final Fantasy VII Remake
        1091500,  # Divinity: Original Sin 2
        292030,   # Dragon Age: Inquisition
        374320,   # Kingdom Come: Deliverance
        1245620,  # Skyrim
        892970,   # Monster Hunter World
        
        # Terror
        1229490,  # Lethal Company
        952060,   # Phasmophobia
        952060,   # Resident Evil Village
        418370,   # Resident Evil 2
        883710,   # Resident Evil 3
        221100,   # DayZ
        418370,   # Outlast
        1966720,  # Dead by Daylight
        
        # Racing
        1172620,  # Forza Horizon 5
        805550,   # Assetto Corsa Competizione
        244210,   # Assetto Corsa
        365960,   # BeamNG.drive
        1080110,  # F1 2023
        683320,   # GRID Legends
        
        # Deportes
        1811260,  # EA SPORTS FIFA 23
        1313860,  # NBA 2K24
        976730,   # Halo Infinite
        1693980,  # EA SPORTS FC 24
        
        # Plataformas
        504230,   # Celeste
        253230,   # A Hat in Time
        774241,   # Castle Crashers
        418370,   # Ori and the Will of the Wisps
        
        # F2P populares
        440,      # Team Fortress 2
        570,      # Dota 2
        730,      # Counter-Strike 2
        1172470,  # Apex Legends
        230410,   # Warframe
        1659040,  # Wuthering Waves
        1811260,  # Realm Royale
        813780,   # Lost Ark
        
        # Mas variedad
        620980,   # Beat Saber
        1203220,  # HITMAN World of Assassination
        1174180,  # Sekiro: Shadows Die Twice
        1449560,  # Inscryption
        1593500,  # God of War
        1817070,  # Marvel's Spider-Man Remastered
        1774580,  # Spider-Man: Miles Morales
        1551360,  # Forza Horizon 4
        1237970,  # Titanfall 2
        1222680,  # Vampire Survivors
    ]
    
    # Eliminar duplicados manteniendo orden
    seen = set()
    unique_ids = []
    for steam_id in steam_ids:
        if steam_id not in seen:
            seen.add(steam_id)
            unique_ids.append(steam_id)
    
    return unique_ids


def main():
    """Ejecuta pipeline de ingesta"""
    
    print("=" * 80)
    print("  PIPELINE DE INGESTA: STEAM + GG.DEALS -> MONGODB")
    print("=" * 80)
    
    # Configuración desde .env
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "videogames_recommender")
    ggdeals_key = os.getenv("GGDEALS_API_KEY")
    
    if not ggdeals_key:
        print("[ERROR] Error: GGDEALS_API_KEY no configurada en .env")
        return
    
    # Inicializar pipeline
    print(f"\n[INIT] Inicializando pipeline...")
    print(f"   MongoDB: {mongo_uri}")
    print(f"   Base de datos: {db_name}")
    print(f"   Region de precios: EU (euros)")
    
    pipeline = GameIngestionPipeline(mongo_uri, db_name, ggdeals_key)
    
    # Obtener lista de juegos populares
    steam_ids = get_popular_steam_ids()
    print(f"\n[INFO] Juegos a procesar: {len(steam_ids)}")
    
    # Obtener y enriquecer juegos
    enriched_games = pipeline.fetch_and_enrich_batch(steam_ids, region="eu")
    
    if not enriched_games:
        print("\n[ERROR] No se pudieron obtener juegos")
        pipeline.close()
        return
    
    # Insertar en MongoDB
    stats = pipeline.insert_games(enriched_games)
    
    # Mostrar estadísticas finales
    print("\n" + "=" * 80)
    print("  RESUMEN DE INGESTA")
    print("=" * 80)
    
    print(f"\n[RESULTADOS]")
    print(f"   Insertados: {stats['inserted']}")
    print(f"   Duplicados (omitidos): {stats['duplicated']}")
    print(f"   Errores: {stats['errors']}")
    
    db_stats = pipeline.get_stats()
    print(f"\n[BD] Estado de la base de datos:")
    print(f"   Total juegos: {db_stats['total_games']}")
    print(f"   Con precios: {db_stats['games_with_prices']}")
    print(f"   Sin precios: {db_stats['games_without_prices']}")
    
    # Mostrar algunos ejemplos
    print(f"\n[PRECIOS] Ejemplos de juegos con precios (EUR):")
    sample_games = pipeline.games_collection.find(
        {"current_price_retail": {"$ne": None}},
        {"name": 1, "current_price_retail": 1, "currency": 1}
    ).limit(5)
    
    for game in sample_games:
        price = game.get("current_price_retail", 0)
        if isinstance(price, (int, float)):
            currency = game.get("currency", "EUR")
            print(f"   - {game['name']}: {price:.2f} {currency}")
        else:
            print(f"   - {game['name']}: {price} (formato invalido)")
    
    print("\n[OK] Pipeline completada")
    print("=" * 80)
    
    pipeline.close()


if __name__ == "__main__":
    main()
