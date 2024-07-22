from storage_interface import IStorage
import json
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


class StorageJson(IStorage):
    def __init__(self):
        self.movies_file_path = "_data/movies.json"
        self.movies = self.load_movies_from_file()

    def load_movies_from_file(self):
        try:
            with open(self.movies_file_path, "r") as file:
                return json.load(file)
        except (IOError, json.JSONDecodeError):
            return {}

    def load_movies_from_api(self, user_search):
        api_url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={user_search}"
        response = requests.get(api_url)
        movie_data = response.json()
        if response.status_code == requests.codes.ok:
            return movie_data
        else:
            print("Error:", response.status_code, response.text)
            return []

    def list_movie(self):
        for movie, details in self.movies.items():
            print(f"{movie} ({details['year']}): {details['rating']}")

    def save_movie(self, movie, title):
        try:
            with open(self.movies_file_path, "w") as file:
                json.dump(movie, file)
            if title in self.movies:
                print(f"Movie {title} successfully added")
        except IOError:
            print("I/O error")

    def add_movie(self, title, year, rating, poster):
        self.movies[title] = {"year": year, "rating": rating, "poster": poster}
        self.save_movie(self.movies, title)

    def delete_movie(self, title):
        if title in self.movies:
            del self.movies[title]
            self.save_movie(self.movies, title)
            print(f"Movie {title} successfully deleted")
        else:
            print("Movie doesn't exist")

    def update_movie(self, title, note):
        if title in self.movies:
            self.movies[title]["note"] = note
            self.save_movie(self.movies, title)
            print(f"Movie {title} successfully updated")
        else:
            print("Movie doesn't exist")

    def movie_stats(self, title):
        movie_data = self.load_movies_from_api(title)
        if not movie_data or movie_data.get("Response") == "False":
            print("Movie not found!")
            return

        imdb_rating = movie_data.get("imdbRating")
        if imdb_rating:
            try:
                imdb_rating = float(imdb_rating)
            except ValueError:
                imdb_rating = None

        ratings = []
        if imdb_rating is not None:
            ratings.append(imdb_rating)

        for rating in movie_data.get("Ratings", []):
            source = rating["Source"]
            value = rating["Value"]
            if source == "Internet Movie Database":
                continue
            elif "%" in value:
                ratings.append(float(value.strip("%")) / 10)
            elif "/" in value:
                numerator, denominator = value.split("/")
                try:
                    ratings.append(float(numerator) / float(denominator) * 10)
                except ValueError:
                    pass

        if not ratings:
            print("No ratings available for this movie.")
            return

        avg_rating = sum(ratings) / len(ratings)
        sorted_ratings = sorted(ratings)
        n = len(ratings)
        median_rating = (
            sorted_ratings[n // 2]
            if n % 2 == 1
            else (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2
        )

        max_rating = max(ratings)
        min_rating = min(ratings)

        print(f"Average rating: {avg_rating:.2f}")
        print(f"Median rating: {median_rating:.2f}")
        print(f"Highest rating: {max_rating:.2f}")
        print(f"Lowest rating: {min_rating:.2f}")

    def random_movie(self):
        api_url = f"https://www.omdbapi.com/?apikey={API_KEY}&s=random"
        response = requests.get(api_url)
        movie_data = response.json()
        if response.status_code == requests.codes.ok:
            if movie_data["Search"]:
                random_movie = random.choice(movie_data["Search"])
                imdb_id = random_movie["imdbID"]
                detail_api_url = (
                    f"https://www.omdbapi.com/?apikey={API_KEY}&i={imdb_id}"
                )
                detail_response = requests.get(detail_api_url)
                random_movie_data = detail_response.json()
                return random_movie_data
            else:
                print("No movies found in the random search.")
        else:
            print("Error:", response.status_code, response.text)
        return None

    def search_movie(self, title):
        movie_data = self.load_movies_from_api(title)
        if movie_data and movie_data.get("Response") == "True":
            title = movie_data.get("Title")
            rating = movie_data.get("imdbRating")
            print(f"{title} has a rating of {rating}")
        else:
            print("Movie not found!")

    def filter_movie(self, min_rating, min_year, max_year):
        movie_data = self.load_movies_from_file()
        filtered_movies = []
        for movie, details in movie_data.items():
            movie_rating = float(details["rating"])
            movie_year = int(details["year"])
            if movie_rating >= min_rating and min_year <= movie_year <= max_year:
                filtered_movies.append((movie, movie_year, movie_rating))

        if filtered_movies:
            for movie, year, rating in filtered_movies:
                print(f"{movie} ({year}): {rating}")
        else:
            print("No movies match the filter criteria.")
            
    def serialize_movie_data(self, movie_title, movie_rating, movie_year, movie_poster):
        output = '<li class="movie">\n'
        output += f'<img src="{movie_poster}" class="movie-poster" alt="{movie_title} Poster"/>\n'
        output += f'<div class="movie-title">{movie_title}</div>\n'
        output += f'<p class="movie-year">{movie_year}</p>\n'
        output += f'<p class="movie-rating">Rating: {movie_rating}</p>\n'
        output += '</li>\n'
        return output

            
    def generate_website(self):
        movie_data = self.load_movies_from_file()

        movies_html = ""
        for movie, details in movie_data.items():
            movie_title = movie
            movie_rating = float(details["rating"])
            movie_year = int(details["year"])
            movie_poster = str(details["poster"])
            movies_html += self.serialize_movie_data(movie_title, movie_rating, movie_year, movie_poster)
        
        with open("_static/movies_template.html", "r") as file:
            html_content = file.read()
        
        updated_html_content = html_content.replace("__TEMPLATE_TITLE__", "My Movie App")
        updated_html_content = updated_html_content.replace("__TEMPLATE_MOVIE_GRID__", movies_html)
        
        with open("_static/movie_app.html", "w") as file:
            file.write(updated_html_content)
