import requests
from config_data.config import BASE_URL, RAPID_API_KEY, BASE_PARAMS
from api.error_handling import error_handling
from random import randint
from utils.movie_utils import parse_movie_details


def search_movie(query: str):

    response = requests.get(f'{BASE_URL}/search/movie', params={**BASE_PARAMS,
                                                                "query": query,
                                                                "include_adult": False})
    if not error_handling(response):
        return None

    data = response.json()
    if not data["results"]:
        return None
    movie = data["results"][0]
    movie_id = movie.get('id')

    details_response = requests.get(f'{BASE_URL}/movie/{movie_id}', params={**BASE_PARAMS})
    if not error_handling(details_response):
        return None

    return parse_movie_details(details_response.json())


def get_movies_by_genre(id_genre: int):

    first_response = requests.get(f"{BASE_URL}/discover/movie", params={**BASE_PARAMS,
                                                                        "sort_by": "vote_average.desc",
                                                                        "vote_count.gte": 1000,
                                                                        "with_genres": str(id_genre),
                                                                        "page": 1})
    if not error_handling(first_response):
        return None

    data = first_response.json()

    total_pages = min(data.get("total_pages", 1), 20)
    random_page = randint(1, total_pages)

    response = requests.get(f"{BASE_URL}/discover/movie", params={**BASE_PARAMS,
                                                                  "page": random_page})
    if not error_handling(response):
        return None

    movies = response.json().get("results", [])[:5]

    result = []
    for movie in movies:
        result.append(parse_movie_details(movie))
    return result

