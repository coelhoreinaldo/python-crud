import mysql.connector
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional

import json

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="the_office_db",
)

cursor = connection.cursor()

app = FastAPI()


class Person(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    gender: str


with open("people.json", "r") as f:
    people = json.load(f)


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


@app.post("/person", status_code=201)
def create_person(person: Person):
    p_id = max([p["id"] for p in people]) + 1
    new_person = {
        "id": p_id,
        "name": person.name,
        "age": person.age,
        "gender": person.gender,
    }

    people.append(new_person)

    with open("people.json", "w") as f:
        json.dump(people, f)

    return new_person


@app.put("/person/{p_id}", status_code=200)
def update_person(p_id: int, person: Person):
    new_person = {
        "id": p_id,
        "name": person.name,
        "age": person.age,
        "gender": person.gender,
    }
    person = [p for p in people if p["id"] == p_id]
    if len(person) > 0:
        people.remove(person[0])
        people.append(new_person)
        with open("people.json", "w") as f:
            json.dump(people, f)

        return new_person
    else:
        return HTTPException(
            status_code=404, detail=f"Person with id {p_id} does not exist"
        )


@app.delete("/person/{p_id}}", status_code=204)
def delete_person(p_id: int):
    person_to_delete = [p for p in people if p["id"] == p_id]
    if len(person_to_delete) > 0:
        people.remove(person_to_delete[0])
        with open("people.json", "w") as f:
            json.dump(people, f)
    else:
        raise HTTPException(
            status_code=404, detail=f"Person with id {p_id} does not exist"
        )


connection.close()
cursor.close()
