from tft_fetcher import TFTDataFetcher

# API configuration
API_KEY = "INSERT KEY HERE"  # Replace with your Riot API key
BASE_LEAGUE_URL = "https://europe.api.riotgames.com"  # Change region if needed
BASE_TFT_URL = "https://euw1.api.riotgames.com"  # Change region if needed
REGION = "EUW"

# Create Class instance
fetcher = TFTDataFetcher(API_KEY, BASE_LEAGUE_URL, BASE_TFT_URL, REGION)

# Summoner name to fetch data for
summoner_name = "Halo214"

# Get win/loss ratio
result = fetcher.win_loss_ratio(summoner_name)

# Print the result
if isinstance(result, dict) and "error" in result:
    print(f"Error: {result['error']}")
    if "details" in result:
        print(f"Details: {result['details']}")
else:
    print(f"Win/Loss Ratio for {summoner_name}: {result:.2f}")
