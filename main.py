from structures.game import SteamGame, PriceOverview, Genre, Platforms
import requests

def main():
    appid = 570  
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
    response = requests.get(url).json()

    data = response[str(appid)]["data"]

    game = SteamGame(
        appid=data["steam_appid"],
        name=data["name"],
        short_description=data.get("short_description", ""),
        developers=data.get("developers", []),
        publishers=data.get("publishers", []),
        price_overview=PriceOverview(**data["price_overview"]) if "price_overview" in data else None,
        platforms=Platforms(**data["platforms"]),
        genres=[Genre(**g) for g in data.get("genres", [])],
        is_free=data.get("is_free", False)
    )

    print(game)

if __name__ == "__main__":
    main()
    