from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from controllers.games import games_router
from controllers.studios import studios_router
from controllers.platforms import platforms_router

#app de flask
app = Flask(__name__)

#middleware para manejar errores
@app.errorhandler(Exception)
def error_middleware(error):
    #respuesta
    response = {}
    code = 0
    
    #filtrar error (http o generico)
    if isinstance(error,HTTPException):
        #obtener el codigo y la descripcion
        response['detail'] = error.description
        code = error.code
    else:
        #error generico
        response['detail'] = "error interno del servidor"
        code = 500
    
    #regresar respuesta
    return jsonify(response), code

#registrar routers
app.register_blueprint(games_router,url_prefix="/games")
app.register_blueprint(studios_router,url_prefix="/studios")
app.register_blueprint(platforms_router,url_prefix="/platforms")

#ruta raiz
@app.get("/")
def get_root():
    return {"msg":"flask is working"}

#lanzamiento por script
if __name__ == "__main__":
    app.run(port=8000)