# MovieApp

MovieApp is a command-line application for managing a personal movie database. Users can add, delete, update, and list movies. It also allows for generating a static website displaying the movies.

## Features

- List movies
- Add movies by searching OMDB API
- Delete movies
- Update movie notes
- Show movie stats
- Pick a random movie
- Search movies by name
- Filter movies by rating and year
- Generate a static HTML website

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/MovieApp.git
    cd MovieApp
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the environment variable for OMDB API key:
    ```sh
    echo "API_KEY=your_omdb_api_key" > .env
    ```

## Usage

Run the application:
```sh
python app.py
