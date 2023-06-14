'''
This module is implementation of storage system using
json.
'''

import json
from istorage import IStorage
from api_requester import IApiRequester


class StorageJson(IStorage):
    """
    StorageJson class represents a storage implementation using JSON files for a movie database.

    Args:
        file_path (str): The path to the JSON file storing the movie data.
        api_requester (IApiRequester): An object implementing the
        IApiRequester interface for making API requests.

    Attributes:
        _file_path (str): The path to the JSON file storing the
        movie data.
        _api_requester (IApiRequester): An object implementing the
        IApiRequester interface for making API requests.

    """

    def __init__(self, file_path: str, api_requester: IApiRequester):
        self._file_path = file_path
        self._api_requester = api_requester

    def load_movies(self):
        """
        Private method to load movies from the JSON file.

        Returns:
            dict: A dictionary representing the loaded movie data.
        """
        try:
            with open(self._file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save_movies(self, movies):
        """
        Private method to save movies to the JSON file.

        Args:
            movies (dict): A dictionary representing the movie data to be saved.

        """
        with open(self._file_path, "w") as file:
            json.dump(movies, file)

    def list_movies(self):
        """
        List all movies in the database.

        """
        movies = self.load_movies()
        if not movies:
            print("No movies found in the database.")
        else:
            print("List of movies:")
            for _, movie in movies.items():
                if 'title' not in movie:
                    print("Error: Movie data is missing the 'title' field.")
                    continue
                print(f"{movie['title']} ({movie['year']})")
                print(f"Director: {movie.get('director', '')}")
                print(f"Genre: {movie.get('genre', '')}")
                print(f"Rating: {movie.get('rating', '')}/10")
                print()

    def add_movie(self, title):
        """
        Add a new movie to the database.

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
        Delete an existing movie from the database.

        Args:
            title (str): The title of the movie to be deleted.

        """
        movies = self.load_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            print(f"Movie {title} Deleted Successfully!")
        else:
            print(f"Movie {title} doesn't exist in the database!")

    def update_movie(self, title, notes):
        """
        Update the notes for an existing movie in the database.

        Args:
            title (str): The title of the movie to be updated.
            notes (str): The additional notes for the movie.

        """
        movies = self.load_movies()
        title_lowercase = title.lower()
        movies_lowercase = {k.lower(): v for k, v in movies.items()}
        if movies_lowercase.get(title_lowercase):
            original_title = [k for k in movies.keys() if k.lower() == title_lowercase][0]
            movies[original_title]["notes"] = notes
            self._save_movies(movies)
            print(f"{original_title} Updated Successfully!")
        else:
            print(f"{title} doesn't exist in the database!")
