'''
This module is implementation of storage system using
csv.
'''

import os
import pandas as pd
from istorage import IStorage
from api_requester import IApiRequester


class StorageCsv(IStorage):
    """
    StorageCsv class represents a storage implementation using CSV files for a movie database.

    Args:
        file_path (str): The path to the CSV file storing the movie data.
        api_requester (IApiRequester): An object implementing the IApiRequester interface for
        making API requests.

    Attributes:
        _file_path (str): The path to the CSV file storing the movie data.
        _api_requester (IApiRequester): An object implementing the
        IApiRequester interface for making API requests.
    """

    def __init__(self, file_path: str, api_requester: IApiRequester):
        self._file_path = file_path
        self._api_requester = api_requester

    def load_movies(self):
        """
        Load movies from the CSV file.

        Returns:
            dict: A dictionary representing the loaded movie data.

        """
        if os.path.exists(self._file_path):
            data_frame = pd.read_csv(self._file_path, index_col=0)
            return data_frame.to_dict('index')
        return {}    

    def _save_movies(self, movies):
        """
        Save movies to the CSV file.

        Args:
            movies (dict): A dictionary representing the movie data to be saved.

        """
        data_frame = pd.DataFrame.from_dict(movies, orient='index')
        data_frame.to_csv(self._file_path, index=True)

    def list_movies(self):
        """
        List all movies in the database.

        """
        movies = self.load_movies()
        if not movies:
            print("No movies found in the database.")
        else:
            print("List of movies:")
            for title, movie in movies.items():
                if 'year' not in movie:
                    print("Error: Movie data is missing the 'year' field.")
                    continue
                print(f"{title} ({movie.get('year', '')})")
                print(f"Director: {movie.get('director', 'N/A')}")
                print(f"Genre: {movie.get('genre', 'N/A')}")
                print(f"Rating: {movie.get('rating', 'N/A')}/10")
                print()

    def add_movie(self, title):
        """
        Add a movie to the database.

        Args:
            title (str): The title of the movie to be added.

        """
        movies = self.load_movies()
        if title in movies:
            print(f"Movie {title} already exists!")
            return
        movie_data = self._api_requester.request_movie_data(title)
        if movie_data.get("Response") == "False":
            print(f"Error: Movie {title} not found.")
            return
        movie = self._api_requester.extract_data(movie_data)
        movies[title] = movie
        self._save_movies(movies)
        print(f"Movie {title} successfully added")

    def delete_movie(self, title):
        """
        Delete a movie from the database.

        Args:
            title (str): The title of the movie to be deleted.

        """
        movies = self.load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            print(f"{title} Deleted Successfully!")
        else:
            print(f"{title} doesn't exist in the database!")

    def update_movie(self, title, notes):
        """
        Update a movie in the database with additional notes.

        Args:
            title (str): The title of the movie to be updated.
            notes (str): The additional notes for the movie.

        """
        movies = self.load_movies()
        if title in movies:
            movies[title]['notes'] = notes
            self._save_movies(movies)
            print(f"{title} Updated Successfully!")
        else:
            print(f"{title} doesn't exist in the database!")
