from flask import Blueprint, request, jsonify
from data.games import GamesRepository

#router de juegos
games_router = Blueprint("games",__name__)

#repositorio
repo = GamesRepository()

#metodos REST
@games_router.get("/<int:limit>")
def get_games(limit=5)->list:
    #obtener juegos
    return repo.get_games(limit)

@games_router.get("/<string:name>")
def game_exists(name=""):
    #validar nombre
    if not name:
        return jsonify({"msg":"no se ingresó nombre"}), 200
    
    #eliminar juego
    res = repo.game_exists(name)
    
    #mensaje de exito
    return jsonify({"msg":"juego existente" if res else "juego no existe"}), 200

@games_router.post("/")
def create_game():    
    #validar json
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
    
    #obtener datos
    data = request.get_json()
    
    #crear registro
    repo.create_game(**data)
    
    #mensaje de exito
    return jsonify({"msg":"juego creado"}), 200

@games_router.delete("/<string:name>")
def delete_game(name=""):
    #validar nombre
    if not name:
        return jsonify({"msg":"sin nombre que eliminar"}), 200
    
    #eliminar juego
    repo.delete_game(name)
    
    #mensaje de exito
    return jsonify({"msg":"juego eliminado"}), 200
    
    