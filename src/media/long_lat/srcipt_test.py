import pandas as pd
import numpy as np


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth specified in decimal degrees
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    # Radius of earth in kilometers is 6371
    distance = 6371 * c
    return distance


def calculate_distances(zipcode_data, target_zip):
    target_lat = None
    target_lon = None

    # Find the coordinates of the target zip code
    target_row = zipcode_data.loc[zipcode_data["ZIP"] == target_zip]
    if not target_row.empty:
        target_lat = target_row["LAT"].values[0]
        target_lon = target_row["LNG"].values[0]

    if target_lat is None or target_lon is None:
        print("Target zip code not found in the dataset")
        return

    # Calculate distance from target zip to all other zip codes
    zipcode_data["Distance"] = zipcode_data.apply(
        lambda row: haversine(target_lat, target_lon, row["LAT"], row["LNG"]), axis=1
    )


# Read data from CSV file
zipcode_data = pd.read_csv(
    "/Users/hoang/Desktop/Resume/Personal/cloudkichen/cloudkitchen-BE/src/media/long_lat/zip_lat_long.csv"
)

# Test the function
target_zip = 75025
calculate_distances(zipcode_data, target_zip)
filtered_zipcodes = zipcode_data[zipcode_data["Distance"] < 50]
print("Zip codes with distance smaller than 50 km:")
print(len(filtered_zipcodes))
