import os
from tft_fetcher import TFTDataFetcher
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for

load_dotenv()

app = Flask(__name__)

# API configuration
API_KEY = os.environ.get("RIOT_API_KEY")  # Replace with your Riot API key
BASE_LEAGUE_URL = "https://europe.api.riotgames.com"  # Change region if needed
BASE_TFT_URL = "https://euw1.api.riotgames.com"  # Change region if needed
REGION = "EUW"

# Create Class instance
fetcher = TFTDataFetcher(API_KEY, BASE_LEAGUE_URL, BASE_TFT_URL, REGION)

# Utility function to handle common logic for fetching and processing TFT data
def get_tft_data_for_summoner(summoner_name):
    tft_data = fetcher.get_tft_data(summoner_name)
    result = fetcher.win_loss_ratio(summoner_name, tft_data)
    if type(result) == "dict":
        result = result.replace("\n", "<br>")
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        # Handle form selection for different options
        selected_option = request.form.get('option')  # safer way to get form data
        if selected_option == 'players_stats':
            return redirect(url_for('players_stats'))
        elif selected_option == 'compare_friends':
            return redirect(url_for('compare_friends'))

        # Process summoner data if no redirection
        summoner_name = request.form.get("summoner_name")
        if summoner_name:
            result = get_tft_data_for_summoner(summoner_name)
        else:
            print("No summoner name provided")

    return render_template("index.html", result=result)

@app.route('/', methods=["GET", "POST"])
def players_stats():
    print("Back to default page")

@app.route('/compare_friends')
def compare_friends():
    result = None
    summoner_id = request.form.get("summoner_id")
    friend_summoner_id = request.form.get("friend_summoner_id")

    if summoner_id and friend_summoner_id:
    # Call your logic to fetch data for both summoners and compare
        user_data = get_tft_data_for_summoner(summoner_id)
        friend_data = get_tft_data_for_summoner(friend_summoner_id)

        # Implement logic to compare both users' stats
        result = {
           "User": summoner_id,
           "Friend": friend_summoner_id,
           "Comparison": "Comparison Logic Here"  # Replace with actual comparison logic
        }
    else:
        print("Both summoner IDs are required.")

    return render_template("compare_friends.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
