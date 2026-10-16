import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class FredDataExtractor:
    """
    Extracts macroeconomic time-series data from the St. Louis FRED REST API.
    """
    BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        if not self.api_key:
            raise ValueError("FRED API Key is missing. Add it to your .env file.")

    def fetch_series(self, series_id: str, observation_start: str = "2000-01-01") -> pd.DataFrame:
        """
        Fetches macroeconomic observations for a given series ID (e.g., 'CPIAUCSL' for CPI Inflation).
        
        Returns:
            pd.DataFrame: Clean DataFrame with 'date' and 'value' columns.
        """
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "observation_start": observation_start
        }

        response = requests.get(self.BASE_URL, params=params)
        
        if response.status_code != 200:
            raise RuntimeError(f"API Request failed with status code {response.status_code}: {response.text}")

        data = response.json()
        observations = data.get("observations", [])

        # Convert raw JSON response into a pandas DataFrame
        df = pd.DataFrame(observations)[["date", "value"]]
        
        # Add metadata column
        df["series_id"] = series_id
        
        return df

if __name__ == "__main__":
    # Quick execution test
    extractor = FredDataExtractor()
    
    # Test fetching US Consumer Price Index (CPI)
    print("Fetching CPI Inflation Data...")
    cpi_df = extractor.fetch_series("CPIAUCSL")
    print(cpi_df.head())
    print(f"\nSuccessfully fetched {len(cpi_df)} observations!")