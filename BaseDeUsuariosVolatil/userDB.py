from typing import Optional
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str                           # Nome do usuario
    login: Optional[str]    = None      # Login do usuario
    pw: Optional[str]       = None      # Senha do usuario
    user_id: int                        # ID do usuario

class UserDB():
    db = []
    
    @staticmethod
    def appendUser(name: str):
        for item in userdb.db:
            if name.lower().replace(" ", "") == item.name.lower().replace(" ", ""):     # Verifica se o usuario ja esta no DB
                raise Exception("User already in DB.")                                  # Nao adiciona se ja estiver no DB
        userdb.db.append( User(name = name, user_id = len(userdb.db)+1) )               # Adiciona o usuario ao db, definindo seu id como (tamanho do DB) + 1

    @staticmethod
    def getUser(userid: int):                                                           # Busca de usuario no DB
        for i in range(len(userdb.db)):
            user = userdb.db[i]
            if userid == user.user_id:
                return user
        
        raise Exception('User not found.')
    
    @staticmethod
    def getAllUsers():                                                                  # Retorna o DB
        return userdb.db
        
    @staticmethod
    def deleteUser(userid: int):                                                        # Deleta um usuario do DB pelo ID
        for i in range(len(userdb.db)):
            user = userdb.db[i]
            if userid == user.user_id:
                userdb.db.pop(i)
                return user
        
        raise Exception('User not found.')