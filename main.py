from movie_app import MovieApp
from storage_json import StorageJson

def main():
    storage = StorageJson()
    movie_app = MovieApp(storage)
    print(movie_app.run())


if __name__ == "__main__":
    main()
