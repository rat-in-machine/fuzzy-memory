from utils.steam_requests import SteamAPI


def main():
    steam = SteamAPI()
    game = steam.get_game_by_appid(570)
    print(game)


if __name__ == "__main__":
    main()
