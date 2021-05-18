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
        return True

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


userdb = UserDB()


@app.get("/")                                                                           # Rota padrao (index)
def index():
    return {"msg": "Bem Vindo!"}

@app.get("/user-management/users/")                                                     # Rota para listar todos os usuarios
def getAllUsers():
    msg = ""
    users = userdb.getAllUsers()
    for item in users:
        msg += item.json()
    return {msg}

@app.get("/user-management/users/{user_id}")                                            # Rota para busca de um usuario (get)
def getUser(user_id: int):
    try:
        user = userdb.getUser(user_id)
    except Exception as e:
        print(e)
        return { 'msg' : str(e) }

    return {user.json()}

@app.post("/user-management/users/{user}")                                              # Rota para registrar um usuario (post)
def addUser(name: str):
    try:
        add_user = userdb.appendUser(name)
    except Exception as e:
        print(e)
        return { 'msg' : str(e) }
        
    return {"user": name, 
            "Added" : add_user}

@app.delete("/user-management/users/{user_id}")                                         # Rota para deletar um usuario (delete)
def delete_user(user_id: int):
    try:
        user = userdb.deleteUser(user_id)
    except Exception as e:
        print(e)
        return { 'msg' : str(e) }
    return {"deleted": True, "User": user}