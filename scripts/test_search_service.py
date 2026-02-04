#!/usr/bin/env python
"""Test para verificar GameSearchService"""

import sys
from pathlib import Path

# Agregar chatbot al path
chatbot_path = Path(__file__).parent / "chatbot"
sys.path.insert(0, str(chatbot_path))

try:
    print("[1] Importando GameSearchService...")
    from src.services.game_search import GameSearchService
    print("    [OK] Importación exitosa")
    
    print("\n[2] Inicializando servicio...")
    service = GameSearchService()
    print("    [OK] Servicio inicializado")
    
    print("\n[3] Buscando 'elden'...")
    results = service.search_by_name("elden", limit=3)
    print(f"    [OK] Encontrados {len(results)} resultados")
    
    if results:
        print("\n[4] Formateando resultados...")
        for game in results:
            formatted = service.format_game_info(game)
            print(f"\n{formatted}")
    else:
        print("    [AVISO] No se encontraron resultados")
        
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
