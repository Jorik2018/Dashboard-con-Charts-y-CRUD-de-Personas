from functools import lru_cache
from app.repositories.people_repository import PeopleRepository

@lru_cache
def get_people_repository():
    return PeopleRepository()
