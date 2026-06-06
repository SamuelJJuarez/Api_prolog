import os
from .prolog import PrologConnector

# Ruta al archivo juegos.pl
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "juegos.pl")
DESARROLLOS_DB_PATH = os.path.join(BASE_DIR, "desarrollos.pl")
DISPONIBILIDADES_DB_PATH = os.path.join(BASE_DIR, "disponibilidades.pl")

#repositorio de juegos
class GamesRepository:
    #metodos de operacion
    def get_games(self, limit:int)->list:
        #contenedor
        games = []
        
        #obtener conexion
        con = PrologConnector.get_instance()
        
        #obtener registros
        cont = 0
        for game in con.do_query("juego(J,F)"):
            #hasta el limite
            if cont > limit:
                break
            
            #obtener datos
            games.append(game)
            cont += 1
            
        #retornar registros    
        return games
    
    #verificar si existe
    def game_exists(self, name:str)->bool:
        #realizar query
        con = PrologConnector.get_instance()
        
        #ejecutar la query
        query = con.do_query(f"esJuego({name.lower()})")
        
        #retornar respuesta
        return bool(list(query))
    
    #registrar un juego
    def create_game(self, name:str, date:str)->None:
        #obtener conexion
        con = PrologConnector.get_instance()
        
        name_lower = name.lower()
        date_lower = date.lower()
        
        # Guardar en memoria de Prolog
        con.create_fact(f"juego({name_lower},{date_lower})")
        
        # Guardar en archivo juegos.pl (append)
        with open(DB_PATH, "a", encoding="utf-8") as f:
            f.write(f"juego({name_lower},{date_lower}).\n")
        
    #eliminar un juego
    def delete_game(self, name:str)->None:
        #obtener conexion
        con = PrologConnector.get_instance()
        
        name_lower = name.lower()
        
        # Eliminar de memoria de Prolog
        con.retract_fact(f"juego({name_lower},_)")
        
        # Reescribir el archivo juegos.pl obteniendo todos los juegos actuales de Prolog
        games = self.get_games(limit=999999)
        with open(DB_PATH, "w", encoding="utf-8") as f:
            for game in games:
                j = game.get('J')
                date_val = game.get('F')
                if j and date_val:
                    f.write(f"juego({j},{date_val}).\n")
                    
        # --- CASCADING DELETES ---
        # 1. Eliminar relaciones de desarrollo (desarrolla)
        con.retract_fact(f"desarrolla({name_lower},_)")
        
        # Reescribir desarrollos.pl
        devs = list(con.do_query("desarrolla(J,E)"))
        with open(DESARROLLOS_DB_PATH, "w", encoding="utf-8") as f:
            for dev in devs:
                j = dev.get('J')
                e = dev.get('E')
                if j and e:
                    f.write(f"desarrolla({j},{e}).\n")
                    
        # 2. Eliminar relaciones de disponibilidad (disponible)
        con.retract_fact(f"disponible({name_lower},_)")
        
        # Reescribir disponibilidades.pl
        disps = list(con.do_query("disponible(J,P)"))
        with open(DISPONIBILIDADES_DB_PATH, "w", encoding="utf-8") as f:
            for disp in disps:
                j = disp.get('J')
                p = disp.get('P')
                if j and p:
                    f.write(f"disponible({j},{p}).\n")