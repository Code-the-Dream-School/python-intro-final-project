import requests
import os


API_URL = "https://api.restcountries.com/countries/v5"  # Replace with your chosen API endpoint

def fetch_data():
    """Fetch data from the API. Returns the raw JSON response, or an empty list on failure."""
    API_KEY = os.environ.get("REST_COUNTRIES_API_KEY")
    if not API_KEY:
        print("No API key found. Set REST_COUNTRIES_API_KEY and try again.")

    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        return response.json()["data"]["objects"]
    except requests.exceptions.RequestException as e:
        print(f"Error could not fetch data: {e}")
        return []

def process_data(records):
    """Extract and transform the fields you need. Returns a list of dictionaries."""
    country_code_dict = {record.get("codes", {}).get("alpha_3"):
                        record.get("names", {}).get("common","Unknown")
                        for record in records}
    result = []
    for record in records:
        result.append({
            "name": record.get("names", {}).get("common","Unknown"),
            "region": record.get("region", "Unknown"),
            "languages": ", ".join([lang["name"] for lang in record.get("languages", [])]),
            "borders": ", ".join(country_code_dict.get(code,code)
                for code in record.get("borders", [])) or "None",
            "code": record.get("codes", {}).get("alpha_3", "Unknown") or "None",
        })
    return result


def display_results(results):
    """Print results to the terminal in a readable format."""
    for result in results:
        print(f"\nCountry: {result["name"]}"
            f"\nCountry Code: {result["code"]}"
            f"\nRegion: {result["region"]}"
            f"\nBorders: {result["borders"]}"
            f"\nOfficial Languages: {result["languages"]}"
              )


def main():
    data = fetch_data()
    records = process_data(data)
    if not records:
        print("No data returned.")
        return
    print(f"Fetched {len(records)} records.")
    display_results(records)


if __name__ == "__main__":
    main()
