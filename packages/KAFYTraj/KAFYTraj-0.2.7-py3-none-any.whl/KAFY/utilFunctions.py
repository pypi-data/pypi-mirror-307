# Use this subroutine to install a package to make sure it will be imported successfully
from  math import atan2, sin, cos, radians,degrees
from pickle import load as pkl_load
from os import path as os_path
from h3 import cell_to_latlng,latlng_to_cell,is_valid_cell
from numpy import array as np_array
from json import load as json_load
from pathlib import Path as pathlib_Path
from pandas import read_csv, DataFrame,concat
def token2centroid_h3_yx(lat: float, lon: float, res: int) -> str:
    """
    Converts a latitude and longitude into an H3 token.

    This function uses the H3 library to convert a latitude and longitude into
    the centroid of the corresponding H3 hexagon.

    Args:
        lat (float): The latitude of the point.
        lon (float): The longitude of the point.
        res (float): The resolution of the token.

    Returns:
        str: The token corresponding to the centroid of the H3 hexagon.
    """
    # returns centroid of the hexagon
    token = latlng_to_cell(lat, lon, res)
    return token


def tokenize_trajectory(
    trajectory: list[tuple[float, float]], resolution: int = 10
) -> list[str]:  # default value for resolution is 10
    """
    Tokenizes a list of GPS points.

    This function processes a list of GPS points, where each point is represented
    as a tuple of latitude and longitude, and converts them into tokens.

    Args:
        gps_points (List[Tuple[float, float]]): A list of tuples where each tuple
        contains a latitude and a longitude.
        resolution (int): tokenizes the input based on this resolution

    Returns:
        List[str]: A list of tokens generated from the GPS points.
    """
    tokens = [token2centroid_h3_yx(lat, lon, resolution) for lat, lon in trajectory]
    return tokens


def detokenize_trajectory(tokenized_trajectory: list[str]) -> list[tuple[float, float]]:
    """
    Detokenizes a list of H3 tokens into a list of (latitude, longitude) tuples.

    Args:
        tokenized_trajectory (list of str): A list of H3 tokens (strings) representing a trajectory.
        bertImputerInstance: An instance of the class that contains the token2point_cluster_centroid method.

    Returns:
        list of tuples: A list of tuples where each tuple contains two floats representing (latitude, longitude).
    """
    detokenized_trajectory = []
    previous_point = None

    for token in tokenized_trajectory:
        if is_valid_cell(token):
            point = DeTokenizer.token2point_cluster_centroid(token, previous_point)
            previous_point = point
            detokenized_trajectory.append((round(point.y, 6), round(point.x, 6)))

    return detokenized_trajectory


def load_tokenized_trajectories(txt_file):
    tokenized_trajectories = []
    with open(txt_file, "r") as f:
        lines = f.readlines()
    for line in lines:
        tokens = line.strip().split("[PAD]")
        tokenized_trajectories.append(tokens)
    return tokenized_trajectories


def load_metadata(metadata_file_path):
    with open(metadata_file_path, "r") as metadata_file:
        metadata = json_load(metadata_file)
    return metadata


class Point:
    """
    Represents a geographical point with latitude and longitude coordinates.

    Attributes:
        x (float): The longitude coordinate of the point.
        y (float): The latitude coordinate of the point.

    Methods:
        __init__(x, y):
            Initializes a Point object with the given longitude and latitude.
        calculate_bearing(point_a, point_b):
            Calculates the bearing (angle) from point_a to point_b in degrees.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate_bearing(self, point_a, point_b):
        """
        Calculates the bearing (angle) from one geographical point to another.

        Args:
            point_a (tuple): A tuple (latitude, longitude) representing the starting point.
            point_b (tuple): A tuple (latitude, longitude) representing the destination point.

        Returns:
            float: The bearing from point_a to point_b in degrees, where 0° represents north.
        """
        lat1 = radians(point_a[0])
        lat2 = radians(point_b[0])
        diff_long = radians(point_b[1] - point_a[1])

        x = sin(diff_long) * cos(lat2)
        y = cos(lat1) * sin(lat2) - (
            sin(lat1) * cos(lat2) * cos(diff_long)
        )

        initial_bearing = atan2(x, y)
        initial_bearing = degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing


class DeTokenizer(object):
    """
    A class for de-tokenizing H3 tokens into geographical points.

    This class is responsible for converting H3 tokens into geographical coordinates
    using different methods:
    1. H3 centroid method: Converts tokens to geographical points based on
    H3's own centroid calculations.
    2. Data centroid method: Converts tokens to geographical points using
    precomputed cluster centroids from a dataset.
    3. Cluster centroid method: Converts tokens to geographical points using
    clustering models, adjusting the results based on previous points.

    Attributes:
        h3_clusters (dict): A dictionary mapping H3 tokens to cluster data,
        including 'x' and 'y' coordinates.
        h3_kmeans (dict): A dictionary mapping H3 tokens to clustering models
        used for predicting points.

    Methods:
        token2point_h3_centroid(token):
            Converts an H3 token to a geographical point using H3 centroid data.
        token2point_data_centroid(token):
            Converts an H3 token to a geographical point using data cluster centroids.
        token2point_cluster_centroid(token, previous_point):
            Converts an H3 token to a geographical point using clustering models
            and adjusts based on previous points.
    """

    def __init__(self):
        # adjust data dir as needed.
        # data_dir = "."
        data_dir = os_path.dirname(os_path.abspath(__file__))
        with open(f"{data_dir}/h3_clusters.pkl", "rb") as file:
            self.h3_clusters = pkl_load(file)
        with open(
            f"{data_dir}/h3_kmeans_clustering_all_models_precise.pkl", "rb"
        ) as file:
            self.h3_kmeans = pkl_load(file)

    def token2point_h3_centroid(self, token):
        """Tokenize a point into a token"""
        y, x = cell_to_latlng(token)
        return Point(x, y)

    def token2point_data_centroid(self, token):
        """Tokenize a point into a token"""
        if token in self.h3_clusters:
            cluster = self.h3_clusters[token]
            x, y = cluster["x"], cluster["y"]
            return Point(x, y)
        else:
            return self.token2point_h3_centroid(token)

    def token2point_cluster_centroid(self, token, previous_point):
        """Tokenize a point into a token"""
        c = self.token2point_data_centroid(token)

        if token not in self.h3_kmeans:
            return c

        if not previous_point:
            return c

        if token in self.h3_clusters and self.h3_clusters[token]["current_count"] <= 20:
            return c

        angle = Point.calculate_bearing(
            self, (previous_point.y, previous_point.x), (c.y, c.x)
        )
        m, means = self.h3_kmeans[token]
        x, y, _ = means[m.predict(np_array([angle]).reshape(-1, 1))][0]
        return Point(x, y)
def add_entry_to_csv(file_path: str, new_entry: dict):
    """
    Loads a CSV file, adds a new entry, and saves the file back.
    
    Args:
        file_path (str): Path to the CSV file.
        new_entry (dict): Dictionary representing the new entry with keys
                        DatasetPath, Level, Cell, NumOfTokens, PretrainedModels.
    """
    # Convert the file path to a Path object for convenience
    file_path = pathlib_Path(file_path)
    
    # Load the existing CSV file, or create an empty DataFrame if it doesn't exist
    if file_path.exists():
        df = read_csv(file_path)
    else:
        raise ValueError("Could not find the datasetsMetadata table .csv file")
    new_entry_df = DataFrame([new_entry])
    df = concat([df, new_entry_df], ignore_index=True)
    # Append the new entry as a new row
    # df = df.append(new_entry, ignore_index=True)
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    print(f"New entry added to {file_path}")