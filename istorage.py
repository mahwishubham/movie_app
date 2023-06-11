'''
This module contains abstract storage class.
'''

from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Interface for storage class.
    Defines abstract methods that each storage class must implement.
    """

    @abstractmethod
    def list_movies(self):
        """
        Abstract method to list all movies.

        Returns:
            list: A list of all movies stored.
        """

    @abstractmethod
    def add_movie(self, title):
        """
        Abstract method to add a movie.

        Args:
            title (str): The title of the movie.
        """

    @abstractmethod
    def delete_movie(self, title):
        """
        Abstract method to delete a movie.

        Args:
            title (str): The title of the movie to delete.
        """

    @abstractmethod
    def update_movie(self, title, notes):
        """
        Abstract method to update a movie.

        Args:
            title (str): The title of the movie to update.
            notes (str): Any additional notes or details about the movie.
        """
