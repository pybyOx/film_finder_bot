from config_data.config import IMG_BASE_URL


class Movie:
    def __init__(self, movie_dict: dict, genres: dict = None):
        self._movie_id = movie_dict.get('id')
        self._title = movie_dict.get('title')
        self._overview = movie_dict.get('overview') or 'Нет описания'
        self._year = movie_dict.get('release_date')[:4]
        self._rating = movie_dict.get('vote_average')
        self._poster_url = IMG_BASE_URL + movie_dict["poster_path"] if movie_dict.get("poster_path") else None
        if genres:
            self._genres = (", ".join([name for id_ in movie_dict.get('genre_ids', [])
                                      for name, genre_id in genres.items() if genre_id == id_])
                            or "Жанры не указаны")
        else:
            self._genres = "Жанры не указаны"

    @property
    def movie_id(self):
        return self._movie_id

    @property
    def title(self):
        return self._title

    @property
    def overview(self):
        return self._overview

    @property
    def year(self):
        return self._year

    @property
    def rating(self):
        return self._rating

    @property
    def poster_url(self):
        return self._poster_url

    @property
    def genres(self):
        return self._genres
