from utils.steam_requests import SteamAPI
from utils.gg_deals_requests import GGDealGame, GGDealsPricesAPI
from dotenv import load_dotenv

import os

def main():
    load_dotenv()

    API_KEY = os.getenv('API_KEY')      # OBTIENE DESDE .ENV LA API_KEY

    print(API_KEY)
    gg = GGDealsPricesAPI(str(API_KEY))
    
    prices_dict = gg.get_prices_by_appids([570, 440], region="es")
    
    for appid, game in prices_dict.items():
        if game is None:
            print(f"{appid} no tiene datos en GG.deals")
        else:
            print(f"{appid}: {game.title} - {game.prices.currentKeyshops} {game.prices.currency}")

    # def main():
    #     steam = SteamAPI()
    #     game = steam.get_game_by_appid(570)
    #     print(game)


if __name__ == "__main__":
    main()
