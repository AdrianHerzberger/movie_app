from _storage.storage_interface import IStorage
from _storage.storage_json import StorageJson

class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        self._storage.list_movie()

    def _command_add_movies(self):
        user_input_search_movies = str(input("Enter new movie name: "))
        fetch_movie_search_result = self._storage.load_movies_from_api(
            user_input_search_movies
        )
        if fetch_movie_search_result:
            title = fetch_movie_search_result.get("Title")
            year = fetch_movie_search_result.get("Year")
            rating = fetch_movie_search_result.get("imdbRating")
            poster = fetch_movie_search_result.get("Poster")
            self._storage.add_movie(title, year, rating, poster)
        else:
            print("Movie not found!")

    def _command_delete_movies(self):
        user_input_delete_movie = str(input("Enter movie name to delete: "))
        self._storage.delete_movie(user_input_delete_movie)

    def _command_update_movie(self):
        user_input_update_movie = str(input("Enter movie name: "))
        updated_movie_notes = str(input("Enter movie notes to update: "))
        self._storage.update_movie(user_input_update_movie, updated_movie_notes)

    def _command_movie_stats(self):
        user_input_movies = str(input("Enter movie name: "))
        fetch_movie_search_result = self._storage.load_movies_from_api(
            user_input_movies
        )
        if fetch_movie_search_result:
            title = fetch_movie_search_result.get("Title")
            self._storage.movie_stats(title)

    def _command_random_movie(self):
        random_movie_data = self._storage.random_movie()
        if random_movie_data:
            print(f"Your random movie for tonight: {random_movie_data['Title']}")
        else:
            print("Failed to fetch a random movie.")

    def _command_search_movie(self):
        user_input_search_movie = str(input("Enter part of the movie name: ")).strip()
        self._storage.search_movie(user_input_search_movie)

    def _command_filter_movies(self):
        min_rating = float(input("Enter minimum rating (0-10): "))
        min_year = int(input("Enter minimum year: "))
        max_year = int(input("Enter maximum year: "))
        self._storage.filter_movie(min_rating, min_year, max_year)
        
    def _command_generate_website(self):
        self._storage.generate_website()
        

    def run(self):
        print("********** My Movies Database **********")
        print(
            f"0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n8. Filter movies\n9. Generate Website"
        )
        while True:
            try:
                user_input_selection = int(input("Enter choice (0 - 8): "))
                if user_input_selection == 0:
                    print("Goodbye!")
                    break
                elif user_input_selection == 1:
                    self._command_list_movies()
                elif user_input_selection == 2:
                    self._command_add_movies()
                elif user_input_selection == 3:
                    self._command_delete_movies()
                elif user_input_selection == 4:
                    self._command_update_movie()
                elif user_input_selection == 5:
                    self._command_movie_stats()
                elif user_input_selection == 6:
                    self._command_random_movie()
                elif user_input_selection == 7:
                    self._command_search_movie()
                elif user_input_selection == 8:
                    self._command_filter_movies()
                elif user_input_selection == 9:
                    self._command_generate_website()
                else:
                    print("Invalid choice! Please provide a number between 0 and 8.")
            except ValueError:
                print("Invalid input! Please provide a number between 0 and 8.")
