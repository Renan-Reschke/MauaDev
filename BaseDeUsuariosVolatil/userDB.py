from typing import Optional
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str       # Nome do usuario
    login: str      # Login do usuario
    pw: str         # Senha do usuario
    user_id: int    # ID do usuario