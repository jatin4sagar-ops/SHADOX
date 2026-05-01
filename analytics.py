# =============================================================
# SHADOX — core/analytics.py
# Uses Pandas, NumPy, and Matplotlib to analyze chat data.
# =============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from db.db import messages_col  # Import the messages collection from your DB layer

def get_message_dataframe():
    """
    Fetches all chat messages from MongoDB and converts them 
    into a structured Pandas DataFrame.
    """
    try:
        # Step 1 — Fetch all documents from the messages collection
        # We exclude the MongoDB '_id' field for a cleaner DataFrame
        raw_messages = list(messages_col.find({}, {"_id": 0}))

        # Step 2 — Check if there is data to process
        if not raw_messages:
            print("[SHADOX] No messages found in database to analyze.")
            return pd.DataFrame(columns=["codename", "text", "timestamp"])

        # Step 3 — Convert the list of dictionaries into a Pandas DataFrame
        df = pd.DataFrame(raw_messages)

        # Step 4 — Ensure timestamp is in proper datetime format for analysis
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

        return df

    except Exception as e:
        print(f"[SHADOX] Error fetching data for analytics: {e}")
        return None

def generate_user_activity_chart():
    """
    Analyzes which anonymous users (codenames) are most active
    and displays a bar chart of message counts.
    """
    # Step 1 — Get the data
    df = get_message_dataframe()

    if df is None or df.empty:
        print("[SHADOX] Analytics cancelled: No data available.")
        return

    # Step 2 — Count messages per codename using Pandas groupby
    # We group by 'codename' and count the number of 'text' entries
    activity_counts = df.groupby("codename")["text"].count().sort_values(ascending=False)

    # Step 3 — Create the Bar Chart using Matplotlib
    plt.figure(figsize=(10, 6))
    activity_counts.plot(kind='bar', color='skyblue', edgecolor='black')

    # Step 4 — Add chart styling and labels
    plt.title("SHADOX: User Activity (Messages per Codename)", fontsize=14)
    plt.xlabel("Anonymous Codename", fontsize=12)
    plt.ylabel("Number of Messages Sent", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Step 5 — Adjust layout and show the chart
    plt.tight_layout()
    print("[SHADOX] Generating activity chart...")
    plt.show()

# ── Manual Test Block ─────────────────────────────────────────
# This part only runs if you execute analytics.py directly.
if __name__ == "__main__":
    # Test 1: Fetch and print the DataFrame
    data = get_message_dataframe()
    if data is not None:
        print("--- Message Data Snapshot ---")
        print(data.head()) # Shows the first few rows
        