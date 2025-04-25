import requests
from config_data.config import BASE_URL, RAPID_API_KEY, BASE_PARAMS
from api.error_handling import error_handling
from random import randint
from utils.movie_utils import parse_movie_details


def get_movie_details_by_id(id_movie: int):
    details = requests.get(f'{BASE_URL}/movie/{id_movie}', params={**BASE_PARAMS})
    if not error_handling(details):
        return None
    return parse_movie_details(details.json())


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

    return get_movie_details_by_id(movie.get('id'))


def get_movies_by_genre(id_genre: int):
    params = {**BASE_PARAMS,
              "sort_by": "vote_average.desc",
              "vote_count.gte": 1000,
              "with_genres": str(id_genre),
              "page": 1
    }
    first_response = requests.get(f"{BASE_URL}/discover/movie", params=params)
    if not error_handling(first_response):
        return None

    data = first_response.json()

    total_pages = min(data.get("total_pages", 1), 20)
    random_page = randint(1, total_pages)
    params["page"] = random_page

    response = requests.get(f"{BASE_URL}/discover/movie", params=params)
    if not error_handling(response):
        return None

    movies = response.json().get("results", [])[:5]

    result = []
    for movie in movies:

        result.append(get_movie_details_by_id(movie.get('id')))
    return result


