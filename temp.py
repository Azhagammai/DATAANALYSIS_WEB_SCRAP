import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

# Step 1: Get the Wikipedia page
url = "https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data"
res = requests.get(url)
res.raise_for_status()

# Step 2: Parse HTML with BeautifulSoup
soup = BeautifulSoup(res.text, "html.parser")

# Step 3: Find the first wikitable
table = soup.find("table", {"class": "wikitable"})

# Step 4: Read table into pandas
df = pd.read_html(StringIO(str(table)))[0]

# Drop the repeated header row (first row of table)
df = df.drop(0).reset_index(drop=True)

# Keep first 4 columns (Location, Cases, Deaths, maybe Ref/Extra)
df = df.iloc[:, :4]

# Rename columns
df.columns = ["Location", "Cases", "Deaths", "Extra"]

# Drop unused column if exists
df = df.drop(columns=["Extra"], errors="ignore")

# Step 5: Data cleaning
df["Location"] = df["Location"].astype(str).str.replace(r"\[.*\]", "", regex=True).str.strip()

df["Cases"] = (
    df["Cases"]
    .astype(str)
    .str.replace(",", "")
    .str.replace(r"\D", "", regex=True)
)

df["Deaths"] = (
    df["Deaths"]
    .astype(str)
    .str.replace(",", "")
    .str.replace(r"\D", "", regex=True)
)

# Convert to numeric
df["Cases"] = pd.to_numeric(df["Cases"], errors="coerce").fillna(0).astype(int)
df["Deaths"] = pd.to_numeric(df["Deaths"], errors="coerce").fillna(0).astype(int)

# Step 6: Add Case Fatality Rate (CFR)
df["CFR (%)"] = (df["Deaths"] / df["Cases"] * 100).round(2)
df["CFR (%)"] = df["CFR (%)"].fillna(0)

# Step 7: Show cleaned data
print(df.head(10))
