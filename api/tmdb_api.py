import requests
from config_data.config import BASE_URL, RAPID_API_KEY, IMG_BASE_URL
from api.error_handling import error_handling


def search_movie(query: str):
    response = requests.get(f'{BASE_URL}/search/movie', params={"api_key": RAPID_API_KEY,
                                                                "query": query,
                                                                "language": "ru-RU",
                                                                "include_adult": False})
    if not error_handling(response):
        return None

    data = response.json()
    if not data["results"]:
        return None
    movie = data["results"][0]
    movie_id = movie.get('id')

    details_response = requests.get(f'{BASE_URL}/movie/{movie_id}', params={"api_key": RAPID_API_KEY,
                                                                            "language": "ru-RU"})
    if not error_handling(details_response):
        return None

    details = details_response.json()

    movie_data = {
        "title": details.get("title"),
        "overview": details.get("overview"),
        "release_date": details.get("release_date", "")[:4],
        "rating": details.get("vote_average"),
        "poster_url": IMG_BASE_URL + details["poster_path"] if details.get("poster_path") else None,
        "genres": [genre["name"] for genre in details.get("genres", [])]}
    return movie_data
