# app/repositories/mongo_people_repository.py

from app.db import get_people_collection
from bson import ObjectId

class PeopleRepository:

    def find_all(self):
        collection = get_people_collection()

        documents = collection.find({})

        personas = []

        for document in documents:
            document["id"] = str(document.pop("_id"))
            personas.append(document)

        return personas

    def find_by_id(self, persona_id: str):
        collection = get_people_collection()
        document = collection.find_one(
            {"_id": ObjectId(persona_id)}
        )
        document["id"] = str(document.pop("_id"))
        return document

    def create(self, persona: dict):
        collection = get_people_collection()

        result = collection.insert_one(persona)

        persona["id"] = str(result.inserted_id)
        persona.pop("_id", None)
        return persona

    def update(self, persona_id: int, data: dict):
        collection = get_people_collection()

        result = collection.update_one(
            {"id": persona_id},
            {"$set": data},
        )

        if result.matched_count == 0:
            return None

        return self.find_by_id(persona_id)

    def delete(self, persona_id: str) -> bool:
        collection = get_people_collection()

        result = collection.delete_one(
            {"_id": ObjectId(persona_id)}
        )

        return result.deleted_count > 0