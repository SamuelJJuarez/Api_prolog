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
    name = data.get("name")
    date = data.get("date")
    state = data.get("state", "activo")
    
    if not name or not date:
        return jsonify({"detail":"faltan campos obligatorios"}), 400
        
    #crear registro
    repo.create_game(name, date, state)
    
    #mensaje de exito
    return jsonify({"msg":"juego creado"}), 200

@games_router.put("/state")
def update_game_state():
    #validar json
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
        
    #obtener datos
    data = request.get_json()
    name = data.get("name")
    state = data.get("state")
    
    if not name or not state:
        return jsonify({"detail":"faltan campos obligatorios"}), 400
        
    #actualizar registro
    res = repo.update_game_state(name, state)
    if not res:
        return jsonify({"detail":"el juego no existe"}), 404
        
    return jsonify({"msg":"estado de juego actualizado"}), 200

@games_router.delete("/<string:name>")
def delete_game(name=""):
    #validar nombre
    if not name:
        return jsonify({"msg":"sin nombre que eliminar"}), 200
    
    #eliminar juego
    repo.delete_game(name)
    
    #mensaje de exito
    return jsonify({"msg":"juego eliminado"}), 200

# añadir género
@games_router.post("/genre")
def add_genre():
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
    data = request.get_json()
    game = data.get("game")
    genre = data.get("genre")
    if not game or not genre:
        return jsonify({"detail":"faltan campos obligatorios"}), 400
    repo.add_genre(game, genre)
    return jsonify({"msg":"género agregado al juego"}), 200

# eliminar género
@games_router.delete("/genre")
def delete_genre():
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
    data = request.get_json()
    game = data.get("game")
    genre = data.get("genre")
    if not game or not genre:
        return jsonify({"detail":"faltan campos obligatorios"}), 400
    repo.delete_genre(game, genre)
    return jsonify({"msg":"género eliminado del juego"}), 200

# añadir calificación
@games_router.post("/rating")
def add_rating():
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
    data = request.get_json()
    game = data.get("game")
    rating = data.get("rating")
    if not game or rating is None:
        return jsonify({"detail":"faltan campos obligatorios"}), 400
    repo.add_rating(game, rating)
    return jsonify({"msg":"calificación agregada al juego"}), 200

# eliminar calificación
@games_router.delete("/rating")
def delete_rating():
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
    data = request.get_json()
    game = data.get("game")
    if not game:
        return jsonify({"detail":"faltan campos obligatorios"}), 400
    repo.delete_rating(game)
    return jsonify({"msg":"calificación eliminada del juego"}), 200

# añadir precio
@games_router.post("/price")
def add_price():
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
    data = request.get_json()
    game = data.get("game")
    price = data.get("price")
    if not game or price is None:
        return jsonify({"detail":"faltan campos obligatorios"}), 400
    repo.add_price(game, price)
    return jsonify({"msg":"precio agregado al juego"}), 200

# eliminar precio
@games_router.delete("/price")
def delete_price():
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
    data = request.get_json()
    game = data.get("game")
    if not game:
        return jsonify({"detail":"faltan campos obligatorios"}), 400
    repo.delete_price(game)
    return jsonify({"msg":"precio eliminado del juego"}), 200
    
    