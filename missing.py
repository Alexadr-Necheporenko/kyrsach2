import pandas as pd

def check_missing_data():
    try:
        df = pd.read_csv("IMDb_Top_250_Movies.csv", encoding="ISO-8859-1")
        missing_data = df.isnull().sum()
        print("Missing Data Summary:")
        print(missing_data)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_missing_values()
