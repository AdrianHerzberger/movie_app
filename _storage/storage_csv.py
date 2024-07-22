from storage_interface import IStorage
from movie_app.movie_app import MovieApp
import json
import csv



class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.movies_file_path = file_path
        self.movies = self.load_movies()

    def load_movies(self):
        try:
            with open(self.movies_file_path, "r") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
                else:
                    return {}
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def list_movie(self):
        movies = self.load_movies()
        for movie, details in movies.items():
            print(f"{movie} ({details['year']}): {details['rating']}")

    def save_movie(self, csv_file_path):
        movies = self.load_movies()
        csv_columns = ["Title", "Year", "Rating", "Poster"]
        try:
            with open(csv_file_path, "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for title, details in movies.items():
                    print(title, details)
                    writer.writerow({
                        "Title": title,
                        "Year": details["year"],
                        "Rating": details["rating"],
                        "Poster": details.get("poster", "")
                    })
        except IOError:
            print("I/O error")

    def add_movie(self, title, year, rating, poster):
        movies = self.load_movies()
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        save_movies(movies)

    def delete_movie(self, title):
        movies = self.load_movies()
        if title in movies:
            del movies[title]
            save_movies(movies)
            print(f"Movie {title} successfully deleted")
        else:
            print("Movie doesn't exist")

    def update_movie(self, title, rating):
        movies = self.load_movies()
        if title in movies:
            movies[title]["rating"] = rating
            save_movies(movies)
        else:
            print("Movie doesn't exist")
            

