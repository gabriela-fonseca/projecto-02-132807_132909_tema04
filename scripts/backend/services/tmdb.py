import requests

API_KEY = "A_TUA_API_KEY"

def search_movie(title):
    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": title
    }

    response = requests.get(url, params=params)

    data = response.json()

    if not data["results"]:
        return None

    movie = data["results"][0]

    return {
        "title": movie["title"],
        "description": movie["overview"],
        "rating": movie["vote_average"],
        "poster_url":
            f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
    }