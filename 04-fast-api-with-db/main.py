import mysql.connector
from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional


def get_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="the_office_db",
    )
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        connection.commit()
        cursor.close()
        connection.close()


app = FastAPI()


class Person(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    gender: str


@app.get("/person/{p_id}", status_code=200)
def get_person_by_id(
    p_id: int, cursor: mysql.connector.cursor.MySQLCursor = Depends(get_db)
):
    query = f"SELECT * FROM people WHERE id = {p_id}"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        column_names = [desc[0] for desc in cursor.description]
        person_dict = dict(zip(column_names, result))
        return person_dict
    else:
        raise HTTPException(
            status_code=404, detail=f"Person with id {p_id} does not exist"
        )


@app.get("/search", status_code=200)
def get_person(
    age: Optional[int] = Query(
        None, title="Age", description="The age to filter for"
    ),
    name: Optional[str] = Query(
        None, title="Name", description="The name to filter for"
    ),
    cursor: mysql.connector.cursor.MySQLCursor = Depends(get_db),
):
    query = "SELECT * FROM people WHERE 1=1"

    if age is not None:
        query += f" AND age = {age}"

    if name is not None:
        query += f" AND name LIKE '%{name}%'"

    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        column_names = [desc[0] for desc in cursor.description]
        people_list = [dict(zip(column_names, row)) for row in results]
        return people_list
    else:
        return []


@app.post("/person", status_code=201)
def create_person(
    person: Person,
    cursor: mysql.connector.cursor.MySQLCursor = Depends(get_db),
):
    query = "INSERT INTO people (name, age, gender) VALUES (%s, %s, %s)"
    values = (person.name, person.age, person.gender)
    cursor.execute(query, values)

    new_person_id = cursor.lastrowid

    new_person = {
        "id": new_person_id,
        "name": person.name,
        "age": person.age,
        "gender": person.gender,
    }

    return new_person


@app.put("/person/{p_id}", status_code=200)
def update_person(
    p_id: int,
    person: Person,
    cursor: mysql.connector.cursor.MySQLCursor = Depends(get_db),
):
    query = "SELECT * FROM people WHERE id = %s"
    cursor.execute(query, (p_id,))
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Person with id {p_id} does not exist"
        )

    query = "UPDATE people SET name = %s, age = %s, gender = %s WHERE id = %s"
    values = (person.name, person.age, person.gender, p_id)
    cursor.execute(query, values)

    updated_person = {
        "id": p_id,
        "name": person.name,
        "age": person.age,
        "gender": person.gender,
    }

    return updated_person


# @app.delete("/person/{p_id}}", status_code=204)
# def delete_person(p_id: int):
#     person_to_delete = [p for p in people if p["id"] == p_id]
#     if len(person_to_delete) > 0:
#         people.remove(person_to_delete[0])
#         with open("people.json", "w") as f:
#             json.dump(people, f)
#     else:
#         raise HTTPException(
#             status_code=404, detail=f"Person with id {p_id} does not exist"
#         )
