'''
main file.
Run: python3 main.py file_path
Arguments:
    1. file_path with .csv or .json extension
'''
import os
import argparse
from dotenv import load_dotenv
from api_requester import ApiRequester
from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv

load_dotenv()  # load environment variables from .env file
API_KEY = os.getenv("API_KEY")  # read the API key from the .env file
BASE_URL = "http://www.omdbapi.com"


def create_app(file_path: str) -> MovieApp:
    """
    Creates an instance of the MovieApp using the appropriate storage
    class based on the file extension.

    Args:
        file_path (str): The path to the storage file.

    Returns:
        MovieApp: An instance of the MovieApp.
    """
    api_requester = ApiRequester(BASE_URL, API_KEY)

    if file_path.endswith('.json'):
        storage = StorageJson(file_path, api_requester)
    elif file_path.endswith('.csv'):
        storage = StorageCsv(file_path, api_requester)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    return MovieApp(storage)


def main():
    """
    The main entry point of the script.
    Parses command-line arguments, creates the MovieApp, and runs it.
    """
    parser = argparse.ArgumentParser(description='Process storage file.')
    parser.add_argument('file_path', help='The storage file path')
    args = parser.parse_args()

    app = create_app(args.file_path)
    app.run()


if __name__ == "__main__":
    main()
