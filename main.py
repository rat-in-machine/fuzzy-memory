from utils.steam_requests import SteamAPI
from utils.gg_deals_requests import GGDealGame, GGDealsPricesAPI
from dotenv import load_dotenv

import os

def main():
    load_dotenv()

    steam = SteamAPI()
    results = steam.search_game_by_name("GUILTY GEAR", limit=3)

    for game in results:
        print(game.name, game.appid, game.price_overview if game.price_overview is not None else "Free!")

    # def main():
    #     steam = SteamAPI()
    #     game = steam.get_game_by_appid(570)
    #     print(game)

if __name__ == "__main__":
    main()
