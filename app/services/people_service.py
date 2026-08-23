# app/services/people_service.py

from app.repositories.repository_factory import get_people_repository
from dataclasses import dataclass

def find_all():
    repository = get_people_repository()
    return repository.find_all()


def find_by_id(persona_id: int):
    repository = get_people_repository()
    return repository.find_by_id(persona_id)


def create(persona: dict):
    repository = get_people_repository()
    return repository.create(persona)


def update(persona_id: int, persona: dict):
    repository = get_people_repository()
    return repository.update(persona_id, persona)

@dataclass
class DeletePersonResult:
    deleted: bool
    persona: dict | None = None


def delete(persona_id: str) -> DeletePersonResult:
    repository = get_people_repository()
    print(f"Deleting persona with ID: {persona_id}")  # Debugging line
    persona = repository.find_by_id(persona_id)

    if persona is None:
        return DeletePersonResult(
            deleted=False,
            persona=None,
        )

    deleted = repository.delete(persona_id)

    if not deleted:
        return DeletePersonResult(
            deleted=False,
            persona=persona,
        )

    return DeletePersonResult(
        deleted=True,
        persona=persona,
    )