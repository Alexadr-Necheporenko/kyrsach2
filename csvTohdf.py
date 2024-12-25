import pandas as pd

# Convert CSV to HDF5
def csv_to_hdf5():
    try:
        # Read the IMDb CSV file with correct encoding
        df = pd.read_csv("IMDb_Top_250_Movies.csv", encoding="ISO-8859-1")
        df.to_hdf("IMDb_Top_250_Movies.h5", key="movies", mode="w")
        print("Successfully converted CSV to HDF5.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    csv_to_hdf5()
