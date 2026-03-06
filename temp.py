import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

# Step 1: Get the Wikipedia page with proper User-Agent header
url = "https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data"

# Add User-Agent to avoid 403 Forbidden error
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    print("✓ Successfully fetched Wikipedia page")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print("Trying alternative URL...")
    # Alternative URL
    url = "https://en.wikipedia.org/wiki/COVID-19_pandemic"
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
    exit()

# Step 2: Parse HTML with BeautifulSoup
soup = BeautifulSoup(res.text, "html.parser")

# Step 3: Find all wikitables (there may be multiple)
tables = soup.find_all("table", {"class": "wikitable"})

if not tables:
    print("No wikitable found. Trying alternative parsing...")
    tables = soup.find_all("table")

if not tables:
    print("Error: No tables found on the page")
    exit()

print(f"✓ Found {len(tables)} table(s)")

# Step 4: Read table into pandas
for idx, table in enumerate(tables):
    try:
        df = pd.read_html(StringIO(str(table)))[0]
        
        if len(df) > 0 and len(df.columns) >= 2:
            print(f"\n--- Processing Table {idx + 1} ---")
            print(f"Original shape: {df.shape}")
            
            # Drop the repeated header row (first row of table) if needed
            if df.iloc[0].astype(str).str.contains("Location|Country|Region", case=False).any():
                df = df.drop(0).reset_index(drop=True)
            
            # Keep first 3-4 columns
            df = df.iloc[:, :4]
            
            # Rename columns
            if len(df.columns) == 4:
                df.columns = ["Location", "Cases", "Deaths", "Extra"]
                df = df.drop(columns=["Extra"], errors="ignore")
            elif len(df.columns) == 3:
                df.columns = ["Location", "Cases", "Deaths"]
            else:
                df.columns = ["Location", "Cases", "Recovery"]
            
            # Step 5: Data cleaning
            df["Location"] = df["Location"].astype(str).str.replace(r"\[.*\]", "", regex=True).str.strip()
            
            df["Cases"] = (
                df["Cases"]
                .astype(str)
                .str.replace(",", "")
                .str.replace(r"[^\d]", "", regex=True)
            )
            
            if "Deaths" in df.columns:
                df["Deaths"] = (
                    df["Deaths"]
                    .astype(str)
                    .str.replace(",", "")
                    .str.replace(r"[^\d]", "", regex=True)
                )
            
            # Convert to numeric
            df["Cases"] = pd.to_numeric(df["Cases"], errors="coerce").fillna(0).astype(int)
            
            if "Deaths" in df.columns:
                df["Deaths"] = pd.to_numeric(df["Deaths"], errors="coerce").fillna(0).astype(int)
                
                # Step 6: Add Case Fatality Rate (CFR)
                df["CFR (%)"] = (df["Deaths"] / (df["Cases"] + 1) * 100).round(2)
                df["CFR (%)"] = df["CFR (%)"].fillna(0)
            
            # Remove rows with empty locations or zero cases
            df = df[df["Location"].str.strip() != ""]
            df = df[df["Cases"] > 0]
            
            # Step 7: Show cleaned data
            print(f"Cleaned shape: {df.shape}")
            print("\nFirst 10 rows:")
            print(df.head(10))
            
            # Save to CSV
            output_file = f"covid_data_table_{idx + 1}.csv"
            df.to_csv(output_file, index=False)
            print(f"\n✓ Data saved to: {output_file}")
            
            break  # Process only the first valid table
            
    except Exception as e:
        print(f"Error processing table {idx + 1}: {e}")
        continue

print("\n✓ Script completed successfully!")
