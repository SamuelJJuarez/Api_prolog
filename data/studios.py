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
        for studio in con.do_query("estudio(E,S)"):
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
    
    #registrar un estudio
    def create_studio(self, name:str, state:str = "activo")->None:
        #obtener conexion
        con = PrologConnector.get_instance()
        name_lower = name.lower()
        state_lower = state.lower()
        
        #crear registro en memoria
        con.create_fact(f"estudio({name_lower},{state_lower})")
        
        # guardar en archivo estudios.pl
        with open(STUDIOS_DB_PATH, "a", encoding="utf-8") as f:
            f.write(f"estudio({name_lower},{state_lower}).\n")
            
    #modificar el estado de un estudio
    def update_studio_state(self, name:str, state:str)->bool:
        con = PrologConnector.get_instance()
        name_lower = name.lower()
        state_lower = state.lower()
        
        # verificar si existe antes de actualizar
        if not self.studio_exists(name_lower):
            return False
            
        # eliminar el hecho anterior y agregar el nuevo
        con.retract_fact(f"estudio({name_lower},_)")
        con.create_fact(f"estudio({name_lower},{state_lower})")
        
        # reescribir estudios.pl
        studios = self.get_studios(limit=999999)
        with open(STUDIOS_DB_PATH, "w", encoding="utf-8") as f:
            for studio in studios:
                e = studio.get('E')
                s = studio.get('S')
                if e and s:
                    f.write(f"estudio({e},{s}).\n")
        return True
        
    #eliminar un juego
    def delete_studio(self, name:str)->None:
        #obtener conexion
        con = PrologConnector.get_instance()
        name_lower = name.lower()
        
        #eliminar de memoria de Prolog
        con.retract_fact(f"estudio({name_lower},_)")
        
        # reescribir el archivo estudios.pl
        studios = self.get_studios(limit=999999)
        with open(STUDIOS_DB_PATH, "w", encoding="utf-8") as f:
            for studio in studios:
                e = studio.get('E')
                s = studio.get('S')
                if e and s:
                    f.write(f"estudio({e},{s}).\n")
                    
        # eliminar también los desarrollos asociados a este estudio
        con.retract_fact(f"desarrolla(_,{name_lower})")
        
        # reescribir desarrollos.pl
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
        
        # verificar si el juego y el estudio existen
        game_exists = bool(list(con.do_query(f"juego({game_lower}, _, _)")))
        studio_exists = bool(list(con.do_query(f"estudio({studio_lower}, _)")))
        
        if game_exists and studio_exists:
            # registrar desarrollo
            con.create_fact(f"desarrolla({game_lower}, {studio_lower})")
            
            # guardar en archivo desarrollos.pl
            with open(DESARROLLOS_DB_PATH, "a", encoding="utf-8") as f:
                f.write(f"desarrolla({game_lower},{studio_lower}).\n")
                
            return True
        return False
        