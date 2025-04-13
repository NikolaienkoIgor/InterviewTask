from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI(title="User Processor API")


# ========================
# Config Section
# ========================
DATA_FILE = "data.txt"
OUTPUT_FILE = "output.json"

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        f.write("Alice,30\nBob,25\n")


class User(BaseModel):
    name: str
    age: int


def read_file(filepath: str) -> List[str]:
    with open(filepath, "r") as f:
        return f.readlines()


def process_lines(lines: List[str]) -> List[User]:
    users = []
    for line in lines:
        if line.strip():
            try:
                name, age = line.strip().split(",")
                users.append(User(name=name, age=int(age)))
            except ValueError:
                continue  # skip malformed lines
    return users


def save_to_json(data: List[User], filepath: str) -> None:
    with open(filepath, "w") as f:
        json.dump([user.dict() for user in data], f)


@app.get("/users", response_model=List[User])
def get_users():
    lines = read_file(DATA_FILE)
    users = process_lines(lines)
    save_to_json(users, OUTPUT_FILE)
    return users

