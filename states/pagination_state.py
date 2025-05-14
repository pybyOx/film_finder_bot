from typing import Optional
from models.movie_model import Movie
from utils.exceptions import UserPagesError


class PageState:
    def __init__(self, movies: list[Movie], current_index: int = 0, is_favorite: bool = False):
        self._movies = movies
        self._current_index = current_index
        self._is_favorite = is_favorite

    def current_movie(self) -> Movie:
        if not self.movies:
            raise UserPagesError('Нет данных о фильмах в PageState')
        return self.movies[self.current_index]

    def total(self) -> int:
        if not self.movies:
            raise UserPagesError('Нет данных о фильмах в PageState')
        return len(self.movies)

    def next(self):
        if self.current_index < self.total() - 1:
            self.current_index += 1

    def prev(self):
        if self.current_index > 0:
            self.current_index -= 1

    @property
    def movies(self):
        return self._movies

    @property
    def current_index(self):
        return self._current_index

    @current_index.setter
    def current_index(self, new_value: int):
        if isinstance(new_value, int):
            self._current_index = new_value
        else:
            raise ValueError("Переданное значение не является целым числом")

    @property
    def is_favorite(self):
        return self._is_favorite


class UserPaginationState:
    def __init__(self):
        self._states: dict[int, PageState] = {}

    @property
    def states(self):
        return self._states

    def set_state(self, user_id: int, state: PageState):
        self._states[user_id] = state

    def get_state(self, user_id: int) -> Optional[PageState]:
        return self._states.get(user_id)

    def delete_state(self, user_id: int):
        self._states.pop(user_id, None)


USER_PAGES = UserPaginationState()
