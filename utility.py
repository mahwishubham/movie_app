'''
This module is used to store Utility Methods like
1. Generate Website
2. Statistics
3. Graphs etc.
'''

import random
from string import Template
from colorama import Fore, Style
from matplotlib import pyplot as plt

class Utility:
    '''
    Utility class represents a utility function used by my movie app.

    Args:
        storage: The storage system used.
    '''

    def __init__(self, storage):
        '''
        Initialize local storage.
        '''
        self._storage = storage

    @staticmethod
    def _generate_movie_html(movie):
        '''
        Generate Website Helper Function
        '''

        title = movie.get('title', 'Title not available')
        year = movie.get('year', 'Year not available')
        poster = movie.get('poster_url')
        rating = movie.get('rating', 0)
        notes = movie.get('notes', "No Notes Added")
        link = f"https://www.imdb.com/title/{movie.get('imdbID')}"
        if poster in ('N/A', None):
            poster = "https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1420&q=80"
        return f"""
        <div class="col-md-4 mb-4">
            <a href="{link}" target="_blank">
                <div class="card h-100 shadow">
                    <img class="card-img-top movie-poster" src="{poster}" alt="{title}">
                    <div class="card-body">
                        <h5 class="card-title movie-title">{title}</h5>
                        <div class="d-flex justify-content-between movie-details">
                            <p class="card-text movie-year badge badge-primary p-2"><strong>Year:</strong> {year}</p>
                            <p class="card-text movie-rating badge badge-success p-2"><strong>Rating:</strong> {rating}</p>
                        </div>
                    </div>
                    <div class="card-footer">
                        <p class="card-text notes">{notes}</p>
                    </div>
                </div>
            </a>
        </div>
        """

    def generate_website(self):
        '''
        Generate Website Code.
        '''
        movies = self._storage.load_movies()
        movie_html = ''.join(self._generate_movie_html(movie) for movie in movies.values())

        with open('_static/index_template.html', 'r', encoding='utf-8') as file:
            template = Template(file.read())

        website_html = template.substitute(movie_list=movie_html)

        with open('_static/index.html', 'w', encoding='utf-8') as file:
            file.write(website_html)

    def stats(self):
        """Calculate and print stats of the movies."""
        movies = self._storage.load_movies()
        n = len(movies)
        # Calculate average rating
        avg = round(sum(float(movie['rating']) for movie in movies.values()) / n, 2)
        print(f"1. Average rating in the database: {avg}")

        # Calculate median rating
        sorted_ratings = sorted(movie['rating'] for movie in movies.values())
        mid = n // 2
        if n % 2 == 0:  # Even number of values
            median = (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2
        else:  # Odd number of values
            median = sorted_ratings[mid]
        print(f"2. Median rating in the database: {median}")

        # The best and worst movie/movies
        max_rating = sorted_ratings[-1]
        min_rating = sorted_ratings[0]
        best_movies = []
        worst_movies = []
        for movie, data in movies.items():
            if data['rating'] == min_rating:
                worst_movies.append(movie)
            elif data['rating'] == max_rating:
                best_movies.append(movie)
        temp1 = '\n'.join(best_movies)
        temp2 = '\n'.join(worst_movies)
        print(f"3. The best movie(s) by rating:\n{temp1}")
        print(f"   The worst movie(s) by rating:\n{temp2}")

    def random_movie(self):
        """Suggest a random movie from the list."""
        movies = self._storage.load_movies()
        rand = random.randint(0, (len(movies) - 1))
        temp = list(movies.items())
        print(f"Here's my movie suggestion for you: "
            f"{temp[rand][0]} ({temp[rand][1]['year']}), Rating: {temp[rand][1]['rating']}")

    def search_movie(self, query):
        """Search movies by query."""
        movies = self._storage.load_movies()
        matching_movies = {}
        for movie, data in movies.items():
            if query.lower() in movie.lower():
                matching_movies[movie] = data['rating']

        if len(matching_movies) == 0:
            print(Fore.RED, "No matching movies found...", Style.RESET_ALL)
        else:
            print("Matching movies:")
            print(matching_movies)

    def movies_sorted_by_rating(self):
        """Print movies sorted by rating."""
        movies = self._storage.load_movies()
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)

        print("\nMovies sorted by ratings: \n------------------------------------------ \n")
        for movie in sorted_movies:
            title = movie[0].ljust(30)
            rating = movie[1]['rating']
            print(f"{title}{rating}")

    def create_rating_histogram(self):
        """Create histogram of movie ratings."""
        movies = self._storage.load_movies()
        ratings = [movie['rating'] for movie in movies.values()]
        plt.hist(ratings)
        plt.xlabel('Rating')
        plt.ylabel('Frequency')
        plt.title('Movie Rating Histogram')
        plt.show()
