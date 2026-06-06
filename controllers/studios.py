from flask import Blueprint, request, jsonify
from data.studios import StudiosRepository

#router de juegos
studios_router = Blueprint("studios",__name__)

#repositorio
repo = StudiosRepository()

#metodos REST
@studios_router.get("/<int:limit>")
def get_Studios(limit=5)->list:
    #obtener juegos
    return repo.get_studios(limit)

@studios_router.get("/<string:name>")
def game_exists(name=""):
    #validar nombre
    if not name:
        return jsonify({"msg":"no se ingresó un nombre"}), 200
    
    #eliminar juego
    res = repo.studio_exists(name)
    
    #mensaje de exito
    return jsonify({"msg":"el estudio existe" if res else "el estudio no existe"}), 200

@studios_router.post("/")
def create_studio():    
    #validar json
    if not request.is_json:
        return jsonify({"detail":"sin contenido a procesar"}), 422
    
    #obtener datos
    data = request.get_json()
    name = data.get("name")
    state = data.get("state", "activo")
    
    if not name:
        return jsonify({"detail":"faltan campos obligatorios"}), 400
        
    #crear registro
    repo.create_studio(name, state)
    
    #mensaje de exito
    return jsonify({"msg":"el estudio fue creado"}), 200

@studios_router.put("/state")
def update_studio_state():
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
    res = repo.update_studio_state(name, state)
    if not res:
        return jsonify({"detail":"el estudio no existe"}), 404
        
    return jsonify({"msg":"estado de estudio actualizado"}), 200

@studios_router.post("/asign")
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
        return jsonify({"detail":"no existe el juego o el estudio"}), 404
    
    #mensaje de exito
    return jsonify({"msg":"se asignó el juego al estudio"}), 200

@studios_router.delete("/<string:name>")
def delete_Studio(name=""):
    #validar nombre
    if not name:
        return jsonify({"msg":"no se ingresó un nombre"}), 200
    
    #eliminar juego
    repo.delete_studio(name)
    
    #mensaje de exito
    return jsonify({"msg":"el estudio fue eliminado"}), 200