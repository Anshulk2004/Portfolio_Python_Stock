import requests
import pandas as pd
from datetime import datetime
import pytz

# Scheme Codes for popular funds (Reliable for Indian MFs)
# You can find any fund's code at https://www.mfapi.in/
MF_SCHEMES = {
    "118989": "HDFC Mid-Cap Opportunities Direct-G",
    "120594": "ICICI Pru Bluechip Direct-G",
    "119598": "Parag Parikh Flexi Cap Direct-G",
    "125497": "SBI Small Cap Direct-G",
    "120503": "Axis Bluechip Direct-G",
    "119063": "UTI Nifty 50 Index Fund Direct-G"
}

TZ = pytz.timezone("Asia/Kolkata")

def fetch_mf_data():
    records = []
    print("Fetching Mutual Fund NAVs...")

    for code, name in MF_SCHEMES.items():
        try:
            # API call to get latest NAV
            url = f"https://api.mfapi.in/mf/{code}"
            response = requests.get(url).json()
            
            if "data" in response and len(response["data"]) > 0:
                current_nav = float(response["data"][0]["nav"])
                prev_nav = float(response["data"][1]["nav"]) if len(response["data"]) > 1 else current_nav
                
                day_change = ((current_nav - prev_nav) / prev_nav) * 100
                
                records.append({
                    "Fund Name": name,
                    "Scheme Code": code,
                    "Current NAV": current_nav,
                    "Day Change %": round(day_change, 2),
                    "Category": response["meta"].get("scheme_category", "N/A"),
                    "Last Updated": response["data"][0]["date"]
                })
                print(f"Success: {name}")
            else:
                print(f"No data for {name}")

        except Exception as e:
            print(f"Error fetching {name}: {e}")

    if records:
        df = pd.DataFrame(records)
        df.to_csv("Live_Mutual_Fund_Data.csv", index=False)
        print("\nSaved: Live_Mutual_Fund_Data.csv")

if __name__ == "__main__":
    fetch_mf_data()