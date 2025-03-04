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

@app.route('/compare_friends',methods=["GET", "POST"])
def compare_friends():
    result = None
    summoner_id = request.form.get("summoner_id")
    friend_summoner_id = request.form.get("friend_summoner_id")

    if summoner_id and friend_summoner_id:
    # Call your logic to fetch data for both summoners and compare
        result_string = ""
        user_data = fetcher.get_tft_data(summoner_id)
        friend_data = fetcher.get_tft_data(friend_summoner_id)

        user_wins = user_data[1]["wins"]
        friend_wins = friend_data[1]["wins"]

        if (user_wins < friend_wins):
            result_string = friend_summoner_id
            result_string += " is the superior TFTer with " 
            result_string += str(friend_wins)
            result_string += " wins!"
        elif (user_wins > friend_wins):
            result_string = summoner_id
            result_string += " is the superior TFTer with " 
            result_string += str(user_wins)
            result_string += " wins!"
        else:
            result_string = summoner_id
            result_string += " and " 
            result_string += friend_summoner_id
            result_string += " are equally versed!"

        # Implement logic to compare both users' stats
        result = {
           "User 1": summoner_id,
           "User 2": friend_summoner_id,
           "User 1 Wins": user_wins,
           "User 2 Wins": friend_wins,
           "ZComparison": result_string  # Replace with actual comparison logic
        }
    else:
        print("Both summoner IDs are required.")

    return render_template("compare_friends.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
