MIDI{STATUS==cc}{CC_FUNCTION==sustain}{CC_VALUE>=64} -> swaymsg workspace 5
MIDI{STATUS==cc}{CC_FUNCTION==sustain}{CC_VALUE<64} -> swaymsg workspace 6
37{c==9} -> ps ax ho pid,command | sed "/[l]eague/I!d; s/\s*\([0-9]*\).*/\1/" | xargs kill -TERM
36{c==9} (python $MM_SCRIPT)[BACKGROUND|INVOCATION_FORMAT=f"\n"]->
{
    import requests
    import json
    import time
    from subprocess import run, DEVNULL
    from threading import Thread

    class Summoner:
        def __init__(self, summoner_name, champion_name, total_gold_spent, position, team):
            self.summoner_name = summoner_name
            self.champion_name = champion_name
            self.total_gold_spent = total_gold_spent
            self.position = position
            self.team = team

    def get_icon_path_from_champion_name(champion_name):
        return f"/home/alex/lol-data/data/ddragon-data/img/champion/{champion_ids[champion_name]}.png"

    def get_summoners():
        response = requests.get(f"{base_url}{player_list_endpoint}", verify=root_certificate)
        response_json = response.json()
        return [
            Summoner(
                summoner_json[summoner_name_key],
                summoner_json[champion_name_key],
                sum(item_prices[item_json[item_id_key]] for item_json in summoner_json[items_key]),
                summoner_json[position_key],
                summoner_json[team_key],
            ) for summoner_json in response_json
        ]

    def gather_ddragon_data():
        with open(item_data_file, "r") as json_file:
            items_json = json.load(json_file)
        for item_id, item_json in items_json[data_key].items():
            item_prices[int(item_id)] = item_json[gold_key][total_key]
        with open(champion_data_file, "r") as json_file:
            champions_json = json.load(json_file)
        for champion_id, champion_json in champions_json[data_key].items():
            champion_ids[champion_json[name_key]] = champion_json[id_key]

    def sort_by_role(team):
        team.sort(key=lambda s: role_order[s.position])

    def update_league_gold_stats_for_team(team, team_name):
        for i, member in enumerate(team):
            run(f"eww update {team_name}-champ-{i + 1}-icon={get_icon_path_from_champion_name(member.champion_name)}", stdout=DEVNULL, shell=True)
            run(f"eww update {team_name}-champ-{i + 1}-gold={member.total_gold_spent}", stdout=DEVNULL, shell=True)

    def update_league_gold_stats():
        summoners = get_summoners()
        blue_team = [summoner for summoner in summoners if summoner.team == "ORDER"]
        red_team = [summoner for summoner in summoners if summoner.team == "CHAOS"]
        assert len(blue_team) <= 5
        assert len(red_team) <= 5
        sort_by_role(blue_team)
        sort_by_role(red_team)
        update_league_gold_stats_for_team(blue_team, "blue")
        update_league_gold_stats_for_team(red_team, "red")

    def update_league_gold_stats_forever():
        while True:
            try:
                update_league_gold_stats()
                time.sleep(2)
            except:
                time.sleep(30)

    lol_data_dir = "/home/alex/lol-data/"
    root_certificate = f"{lol_data_dir}riotgames.pem"
    base_url = "https://127.0.0.1:2999/"
    live_client_data_endpoint = "liveclientdata/"
    player_list_endpoint = f"{live_client_data_endpoint}playerlist"
    summoner_name_key = "summonerName"
    current_gold_key = "currentGold"
    champion_name_key = "championName"
    items_key = "items"
    item_id_key = "itemID"
    position_key = "position"
    team_key = "team"
    data_key = "data"
    gold_key = "gold"
    total_key = "total"
    name_key = "name"
    id_key = "id"
    ddragon_data_dir = f"{lol_data_dir}data/ddragon-data/data/en_US/"
    item_data_file = f"{ddragon_data_dir}item.json"
    champion_data_file = f"{ddragon_data_dir}champion.json"
    item_prices = {}
    champion_ids = {}
    role_order = {
        "TOP": 0,
        "JUNGLE": 1,
        "MIDDLE": 2,
        "BOTTOM": 3,
        "UTILITY": 4,
        "NONE": 5,
        "": 5
    }
    gather_ddragon_data()
    Thread(target=update_league_gold_stats_forever, daemon=True).start()
    while True:
        input()
        run("eww open --toggle league-gold-stats-window", stdout=DEVNULL, shell=True)
}
