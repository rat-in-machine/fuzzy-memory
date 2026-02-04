"""
Script de integración Steam + GG.deals
Flujo: Steam API (datos del juego) → GG.deals API (precios)
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Añadir paths
chatbot_path = Path(__file__).parent / 'chatbot'
sys.path.insert(0, str(chatbot_path))

from dotenv import load_dotenv

# Cargar .env
load_dotenv(chatbot_path / '.env')

from src.ingestion.steam_client import SteamAPIClient
from src.ingestion.ggdeals_client import GGDealsAPIClient


def print_section(title):
    """Imprime sección visual"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def enrich_game_with_prices(game_data, ggdeals_client):
    """
    Enriquece datos de Steam con precios de GG.deals
    
    Args:
        game_data: Dict con datos de Steam
        ggdeals_client: Cliente de GG.deals
        
    Returns:
        Dict combinado con toda la información
    """
    steam_id = game_data["steam_id"]
    
    # Obtener precios de GG.deals
    price_data = ggdeals_client.get_game_prices(steam_id)
    
    if price_data:
        game_data.update({
            "ggdeals_url": price_data["url"],
            "current_price_retail": price_data["current_retail"],
            "current_price_keyshop": price_data["current_keyshops"],
            "historical_low_retail": price_data["historical_retail"],
            "historical_low_keyshop": price_data["historical_keyshops"],
            "currency": price_data["currency"],
            "price_updated_at": datetime.now().isoformat(),
        })
    else:
        game_data.update({
            "current_price_retail": None,
            "current_price_keyshop": None,
            "price_available": False,
        })
    
    return game_data


def main():
    """Función principal"""
    
    print_section("🎮 INTEGRACIÓN STEAM + GG.DEALS API")
    
    # Inicializar clientes
    API_KEY = os.getenv('GGDEALS_API_KEY')
    
    steam_client = SteamAPIClient()
    ggdeals_client = GGDealsAPIClient(api_key=API_KEY)
    
    print(f"[OK] Clientes inicializados")
    print(f"   Steam: {steam_client.BASE_URL}")
    print(f"   GG.deals: {ggdeals_client.BASE_URL}")
    
    # ========================================================================
    # TEST 1: Obtener juegos populares de Steam
    # ========================================================================
    print_section("TEST 1: Obtener datos de juegos desde Steam")
    
    # IDs de juegos populares conocidos
    popular_games = [
        1091500,  # Cyberpunk 2077
        1245620,  # Elden Ring
        271590,   # Grand Theft Auto V
        292030,   # The Witcher 3
        1174180,  # Red Dead Redemption 2
    ]
    
    games_data = []
    
    for app_id in popular_games:
        print(f"\nObteniendo datos de Steam ID {app_id}...")
        game = steam_client.get_app_details(app_id)
        
        if game:
            print(f"   ✅ {game['name']}")
            print(f"      Géneros: {', '.join(game['genres'][:3])}")
            print(f"      Desarrollador: {', '.join(game['developers'][:2])}")
            print(f"      Metacritic: {game['metacritic']}")
            games_data.append(game)
        else:
            print(f"   ❌ No se pudo obtener")
    
    print(f"\n[INFO] Total juegos obtenidos: {len(games_data)}")
    
    # ========================================================================
    # TEST 2: Enriquecer con precios de GG.deals
    # ========================================================================
    print_section("TEST 2: Enriquecer con precios de GG.deals")
    
    enriched_games = []
    
    for game in games_data:
        print(f"\nObteniendo precios para: {game['name']}")
        enriched = enrich_game_with_prices(game, ggdeals_client)
        
        if enriched.get("current_price_retail"):
            print(f"   ✅ Precio retail: ${enriched['current_price_retail']} {enriched['currency']}")
            print(f"      Precio keyshop: ${enriched['current_price_keyshop']}")
            print(f"      Mínimo histórico: ${enriched['historical_low_retail']} (retail)")
            print(f"      URL: {enriched['ggdeals_url']}")
        else:
            print(f"   ⚠️  Precios no disponibles en GG.deals")
        
        enriched_games.append(enriched)
    
    # ========================================================================
    # TEST 3: Búsqueda batch optimizada
    # ========================================================================
    print_section("TEST 3: Búsqueda batch (optimizada)")
    
    print("Obteniendo precios de todos los juegos en una sola llamada...")
    
    steam_ids = [g["steam_id"] for g in games_data]
    batch_prices = ggdeals_client.get_prices_by_steam_ids(steam_ids)
    
    print(f"✅ Precios obtenidos para {len(batch_prices)} juegos en 1 request")
    
    for steam_id, price_data in batch_prices.items():
        if price_data:
            print(f"\n   [{steam_id}] {price_data['title']}")
            prices = price_data.get('prices', {})
            print(f"       Retail: ${prices.get('currentRetail')} {prices.get('currency')}")
            print(f"       Keyshop: ${prices.get('currentKeyshops')}")
    
    # ========================================================================
    # TEST 4: Validar estructura final de datos
    # ========================================================================
    print_section("TEST 4: Estructura de datos final")
    
    if enriched_games:
        sample = enriched_games[0]
        print(f"\n📦 Juego de ejemplo: {sample['name']}\n")
        
        print("Campos de Steam:")
        print(f"  - steam_id: {sample['steam_id']}")
        print(f"  - name: {sample['name']}")
        print(f"  - type: {sample['type']}")
        print(f"  - genres: {sample['genres']}")
        print(f"  - developers: {sample['developers']}")
        print(f"  - release_date: {sample['release_date']}")
        print(f"  - metacritic: {sample['metacritic']}")
        
        print("\nCampos de GG.deals:")
        print(f"  - current_price_retail: ${sample.get('current_price_retail')} {sample.get('currency')}")
        print(f"  - current_price_keyshop: ${sample.get('current_price_keyshop')}")
        print(f"  - historical_low_retail: ${sample.get('historical_low_retail')}")
        print(f"  - ggdeals_url: {sample.get('ggdeals_url')}")
        print(f"  - price_updated_at: {sample.get('price_updated_at')}")
        
        print("\n✅ Estructura completa lista para MongoDB")
    
    # ========================================================================
    # TEST 5: Buscar ofertas (juegos < $30)
    # ========================================================================
    print_section("TEST 5: Buscar ofertas económicas (<$30)")
    
    deals = ggdeals_client.get_deals(steam_ids, max_price=30.0)
    
    print(f"✅ Encontradas {len(deals)} ofertas bajo $30:\n")
    
    for deal in deals:
        # Buscar nombre en games_data
        game_name = next(
            (g['name'] for g in games_data if g['steam_id'] == deal['steam_app_id']),
            deal['title']
        )
        print(f"   💰 {game_name}")
        print(f"      ${deal['current_retail']} {deal['currency']}")
        print(f"      {deal['url']}")
    
    # ========================================================================
    # Resumen final
    # ========================================================================
    print_section("📊 RESUMEN FINAL")
    
    print(f"\n✅ Integración completada exitosamente")
    print(f"\n   Juegos procesados: {len(games_data)}")
    print(f"   Con precios: {sum(1 for g in enriched_games if g.get('current_price_retail'))}")
    print(f"   Ofertas encontradas: {len(deals)}")
    print(f"\n   Rate limits GG.deals:")
    print(f"   - Por minuto: 100 juegos")
    print(f"   - Por hora: 1000 juegos")
    print(f"\n   Recomendación: Batch de máximo 100 juegos por request")
    
    # Cerrar clientes
    steam_client.close()
    ggdeals_client.close()
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
