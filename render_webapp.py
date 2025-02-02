import os
from tft_fetcher import TFTDataFetcher
from dotenv import load_dotenv
from flask import Flask, request, render_template

load_dotenv()

app = Flask(__name__)

# API configuration
API_KEY = os.environ.get("RIOT_API_KEY")  # Replace with your Riot API key
BASE_LEAGUE_URL = "https://europe.api.riotgames.com"  # Change region if needed
BASE_TFT_URL = "https://euw1.api.riotgames.com"  # Change region if needed
REGION = "EUW"

# Create Class instance
fetcher = TFTDataFetcher(API_KEY, BASE_LEAGUE_URL, BASE_TFT_URL, REGION)

# Summoner name to fetch data for
summoner_name = "Halo214"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        summoner_name = request.form["summoner_name"]
        tft_data = fetcher.get_tft_data(summoner_name)
        result = fetcher.win_loss_ratio(summoner_name,tft_data)
        result = result.replace("\n", "<br>")
        print(result)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
