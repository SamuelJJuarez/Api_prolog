from flask import Blueprint, request, jsonify
from data.platforms import PlatformsRepository

#router de juegos
platforms_router = Blueprint("platforms",__name__)

#repositorio
repo = PlatformsRepository()

#metodos REST
@platforms_router.get("/<int:limit>")
def get_platforms(limit=5)->list:
    #obtener juegos
    return repo.get_platforms(limit)

@platforms_router.get("/<string:name>")
def game_exists(name=""):
    #validar nombre
    if not name:
        return jsonify({"msg":"no se ingresó un nombre"}), 200
    
    #eliminar juego
    res = repo.platform_exists(name)
    
    #mensaje de exito
    return jsonify({"msg":"la plataforma existe" if res else "la plataforma no existe"}), 200

@platforms_router.post("/")
def create_platform():    
    #validar json
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
    
    #obtener datos
    data = request.get_json()
    
    #crear registro
    repo.create_platform(**data)
    
    #mensaje de exito
    return jsonify({"msg":"la plataforma fue creada"}), 200

@platforms_router.post("/asign")
def asign_game():
    #validar json
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
    
    #obtener datos
    data = request.get_json()
    
    #crear registro
    res = repo.asign_game(**data)
    
    #validar respuesta
    if not res:
        return jsonify({"detail":"no existe el juego o la plataforma"}), 404
    
    #mensaje de exito
    return jsonify({"msg":"se asignó el juego a la plataforma"}), 200

@platforms_router.delete("/<string:name>")
def delete_platform(name=""):
    #validar nombre
    if not name:
        return jsonify({"msg":"no se ingresó un nombre"}), 200
    
    #eliminar juego
    repo.delete_platform(name)
    
    #mensaje de exito
    return jsonify({"msg":"la plataforma fue eliminada"}), 200