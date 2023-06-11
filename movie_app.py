'''
This module contains the code to run our Movies App.
'''

from colorama import Fore, Style
from utility import Utility

class MovieApp:
    """
    MovieApp class represents an application for managing a movie database.

    Args:
        storage: The storage object that implements the required methods for managing movies.

    Attributes:
        _storage: The storage object used for accessing and manipulating movie data.

    """

    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        """
        Command to list all movies in the database.
        """
        self._storage.list_movies()

    def _command_add_movie(self):
        """
        Command to add a new movie to the database.
        """
        print(Fore.MAGENTA, "Enter Movie Name:", Style.RESET_ALL, end="\t")
        title = input()
        self._storage.add_movie(title)

    def _command_delete_movies(self):
        """
        Command to delete movies from the database.
        """
        print(Fore.MAGENTA, "Enter titles of the movies to delete (separated by commas):",
              Style.RESET_ALL, end="\t")
        titles = [title.strip() for title in input().split(",")]
        for title in titles:
            self._storage.delete_movie(title)

    def _command_update_movie(self):
        """
        Command to update a movie in the database.
        """
        print(Fore.MAGENTA, "Enter Movie Name:", Style.RESET_ALL, end="\t")
        title = input()
        print(Fore.MAGENTA, "Enter movie notes:", Style.RESET_ALL, end="\t")
        notes = input()
        self._storage.update_movie(title, notes)
    
    def _command_generate_website(self):
        """
        Command to generate website_html.
        """
        util = Utility(self._storage)
        util.generate_website()

    def run(self):
        """
        Runs the movie database application.

        Displays a menu and performs the corresponding actions based on user input.
        """
        while True:
            print(Fore.GREEN, "********** My Movies Database **********", Style.RESET_ALL)
            print(Fore.BLUE, '''Movie Menu:
            0. Exit
            1. List movies
            2. Add movies
            3. Delete movies
            4. Update movies
            5. Generate Website
            ''', Style.RESET_ALL)

            print(Fore.MAGENTA, "\n\nEnter 0, 1, 2, 3, 4:", Style.RESET_ALL, end="\t")
            selection = input()

            if selection == "1":
                self._command_list_movies()
            elif selection == "2":
                self._command_add_movie()
            elif selection == "3":
                self._command_delete_movies()
            elif selection == "4":
                self._command_update_movie()
            elif selection == "5":
                self._command_generate_website()
                print("Website Created!")
            elif selection == "0":
                print("Goodbye!")
                break
            else:
                print(Fore.YELLOW, "Please enter a valid input from 0 ... 4\n\n\n",
                      Style.RESET_ALL)
                continue

            print(Fore.MAGENTA, "\n\n\nPress Enter To Continue ... \n\n", Style.RESET_ALL)
            if input():
                break
