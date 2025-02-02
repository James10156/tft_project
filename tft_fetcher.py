import os
import requests
import argparse
from dotenv import load_dotenv

load_dotenv()

class TFTDataFetcher:
    def __init__(self, api_key, base_league_url, base_tft_url, region):
        self.api_key = api_key
        self.base_league_url = base_league_url
        self.base_tft_url = base_tft_url
        self.region = region
        self.headers = {"X-Riot-Token": self.api_key}

    def get_puuid_by_name(self, summoner_name):
        url = f"{self.base_league_url}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{self.region}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}

    def get_summoner_by_puuid(self, puuid):
        url = f"{self.base_tft_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}

    def get_tft_data_by_id(self, summoner_id):
        url = f"{self.base_tft_url}/tft/league/v1/entries/by-summoner/{summoner_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}

    def get_tft_data(self, summoner_name):
        puuid_data = self.get_puuid_by_name(summoner_name)
        if "error" in puuid_data:
            return puuid_data

        puuid = puuid_data.get("puuid", "")
        if not puuid:
            return {"error": "PUUID not found"}

        summoner_data = self.get_summoner_by_puuid(puuid)
        if "error" in summoner_data:
            return summoner_data

        summoner_id = summoner_data.get("id", "")
        if not summoner_id:
            return {"error": "Summoner ID not found"}

        tft_data = self.get_tft_data_by_id(summoner_id)
        if "error" in tft_data:
            return tft_data

        return tft_data

    def win_loss_ratio(self,summoner_name,tft_data):

        # Assuming `tft_data` contains entries for win/loss data
        try:
            output = ""
            queue_type = tft_data[0]["queueType"]
            wins = tft_data[1]["wins"]
            losses = tft_data[1]["losses"]
            ratio = float(wins) / float(losses)

            output += f"Summoner ID: {summoner_name} \n"
            output += f"Game Mode: {queue_type} \n"
            output += f"Wins: {wins} \n"
            output += f"Losses: {losses} \n"
            output += "Win/Loss Ratio: " + str(ratio)
            return output

        except (IndexError, KeyError) as e:
            return {"error": "Invalid data structure", "details": str(e)}

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="A script that fetches TFT data.")
    parser.add_argument("--arg", default="JustYuri1", type=str, help="Summoner Name (e.g., JustYuri1)")
    args = parser.parse_args()

    summoner_name = args.arg

    # API configuration
    API_KEY = os.environ.get("RIOT_API_KEY")  # Replace with your Riot API key
    BASE_LEAGUE_URL = "https://europe.api.riotgames.com"  # Change region if needed
    BASE_TFT_URL = "https://euw1.api.riotgames.com"  # Change region if needed
    REGION = "EUW"

    # Create an instance of TFTDataFetcher
    tft_data_fetcher = TFTDataFetcher(API_KEY, BASE_LEAGUE_URL, BASE_TFT_URL, REGION)

    # Get win/loss ratio
    tft_data = tft_data_fetcher.get_tft_data(summoner_name)
    result = tft_data_fetcher.win_loss_ratio(summoner_name,tft_data)

    if isinstance(result, dict) and "error" in result:
        print(f"Error: {result['error']}")
        if "details" in result:
            print(f"Details: {result['details']}")
    else:
        print(f"{result}")


if __name__ == "__main__":
    main()

