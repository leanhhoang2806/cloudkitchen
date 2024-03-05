import pandas as pd
import numpy as np
import logging


logging.basicConfig(level=logging.INFO)


class ZipcodeSearchReader:
    def __init__(self, csv_file="src/media/long_lat/zip_lat_long.csv"):
        self.zipcode_data = self.load_zipcode_data(csv_file)

    def load_zipcode_data(self, csv_file):
        zipcode_df = pd.read_csv(csv_file)
        return zipcode_df

    def _haversine(self, lat1, lon1, lat2, lon2):
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

    def calculate_distances(self, target_zip):
        target_lat = None
        target_lon = None

        # Find the coordinates of the target zip code
        target_row = self.zipcode_data.loc[self.zipcode_data["ZIP"] == target_zip]
        if not target_row.empty:
            target_lat = target_row["LAT"].values[0]
            target_lon = target_row["LNG"].values[0]

        if target_lat is None or target_lon is None:
            print("Target zip code not found in the dataset")
            return

        # Calculate distance from target zip to all other zip codes
        self.zipcode_data["Distance"] = self.zipcode_data.apply(
            lambda row: self._haversine(target_lat, target_lon, row["LAT"], row["LNG"]),
            axis=1,
        )

    def find_neighbors(self, zipcode: int, radius_km=50):
        self.calculate_distances(zipcode)
        neighbors = self.zipcode_data[self.zipcode_data["Distance"] <= radius_km]
        raw_data = neighbors[["ZIP"]].to_numpy().tolist()
        return [raw[0] for raw in raw_data]
