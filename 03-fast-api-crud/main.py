from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

import json

app = FastAPI()


class Person(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    gender: str


with open("people.json", "r") as f:
    people = json.load(f)["people"]


@app.get("/person/{p_id}", status_code=200)
def get_person_by_id(p_id: int):
    person = [p for p in people if p["id"] == p_id]
    return person[0] if len(person) > 0 else {}


@app.get("/search", status_code=200)
def get_person(
    age: Optional[int] = Query(
        None, title="Age", description="The age to filter for"
    ),
    name: Optional[str] = Query(
        None, title="Name", description="The name to filter for"
    ),
):
    people1 = [p for p in people if p["age"] == age]

    if name is None:
        if age is None:
            return people
        else:
            return people1
    else:
        people2 = [p for p in people if name.lower() in p["name"].lower()]
        if age is None:
            return people2
        else:
            combined = [p for p in people1 if p in people2]
            return combined
