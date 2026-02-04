#!/usr/bin/env python
"""
Script de diagnóstico para GameSearchService
"""
import sys
import traceback

try:
    from src.services.game_search import get_game_search
    print("✓ GameSearchService import successful")
    
    gs = get_game_search()
    print("✓ GameSearchService initialized successfully")
    
    result = gs.search_by_genre('Rol', limit=2)
    print(f"✓ Search by genre returned: {len(result)} games")
    
    if result:
        game = result[0]
        print(f"  - First game: {game.get('name')}")
    else:
        print("  ⚠ No games found for genre 'Rol'")
        
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
