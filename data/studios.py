import os
from .prolog import PrologConnector

# Rutas a los archivos de bases de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDIOS_DB_PATH = os.path.join(BASE_DIR, "estudios.pl")
DESARROLLOS_DB_PATH = os.path.join(BASE_DIR, "desarrollos.pl")

#repositorio de juegos
class StudiosRepository:
    #metodos de operacion
    def get_studios(self, limit:int)->list:
        #contenedor
        studios = []
        
        #obtener conexion
        con = PrologConnector.get_instance()
        
        #obtener registros
        cont = 0
        for studio in con.do_query("estudio(E)"):
            #hasta el limite
            if cont > limit:
                break
            
            #obtener datos
            studios.append(studio)
            cont += 1
            
        #retornar registros    
        return studios
    
    #verificar si existe
    def studio_exists(self, name:str)->bool:
        #realizar query
        con = PrologConnector.get_instance()
        
        #ejecutar la query
        query = con.do_query(f"esEstudio({name.lower()})")
        
        #retornar respuesta
        return bool(list(query))
    
    #registrar un juego
    def create_studio(self, name:str)->None:
        #obtener conexion
        con = PrologConnector.get_instance()
        name_lower = name.lower()
        
        #crear registro en memoria
        con.create_fact(f"estudio({name_lower})")
        
        # Guardar en archivo estudios.pl
        with open(STUDIOS_DB_PATH, "a", encoding="utf-8") as f:
            f.write(f"estudio({name_lower}).\n")
        
    #eliminar un juego
    def delete_studio(self, name:str)->None:
        #obtener conexion
        con = PrologConnector.get_instance()
        name_lower = name.lower()
        
        #eliminar de memoria de Prolog
        con.retract_fact(f"estudio({name_lower})")
        
        # Reescribir el archivo estudios.pl
        studios = self.get_studios(limit=999999)
        with open(STUDIOS_DB_PATH, "w", encoding="utf-8") as f:
            for studio in studios:
                e = studio.get('E')
                if e:
                    f.write(f"estudio({e}).\n")
                    
        # Eliminar también los desarrollos asociados a este estudio de Prolog
        con.retract_fact(f"desarrolla(_,{name_lower})")
        
        # Reescribir desarrollos.pl
        devs = list(con.do_query("desarrolla(J,E)"))
        with open(DESARROLLOS_DB_PATH, "w", encoding="utf-8") as f:
            for dev in devs:
                j = dev.get('J')
                e = dev.get('E')
                if j and e:
                    f.write(f"desarrolla({j},{e}).\n")
        
    #asignar juego
    def asign_game(self, game:str, studio:str)->bool:        
        game_lower = game.lower()
        studio_lower = studio.lower()
        
        con = PrologConnector.get_instance()
        
        # Verificar si el juego y el estudio existen
        game_exists = bool(list(con.do_query(f"juego({game_lower}, _)")))
        studio_exists = bool(list(con.do_query(f"estudio({studio_lower})")))
        
        if game_exists and studio_exists:
            # Registrar desarrollo en la base de hechos
            con.create_fact(f"desarrolla({game_lower}, {studio_lower})")
            
            # Guardar en archivo desarrollos.pl
            with open(DESARROLLOS_DB_PATH, "a", encoding="utf-8") as f:
                f.write(f"desarrolla({game_lower},{studio_lower}).\n")
                
            return True
        return False
        