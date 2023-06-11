'''
This module is used to store Utility Methods like
1. Generate Website
2. Statistics
3. Graphs etc.
'''

from string import Template


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
        movies = self._storage._load_movies()
        movie_html = ''.join(self._generate_movie_html(movie) for movie in movies.values())

        with open('_static/index_template.html', 'r', encoding='utf-8') as file:
            template = Template(file.read())

        website_html = template.substitute(movie_list=movie_html)

        with open('_static/index.html', 'w', encoding='utf-8') as file:
            file.write(website_html)
