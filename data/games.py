import os
from .prolog import PrologConnector

# Rutas a los archivos de prolog
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "juegos.pl")
DESARROLLOS_DB_PATH = os.path.join(BASE_DIR, "desarrollos.pl")
DISPONIBILIDADES_DB_PATH = os.path.join(BASE_DIR, "disponibilidades.pl")
GENEROS_DB_PATH = os.path.join(BASE_DIR, "generos.pl")
CALIFICACION_DB_PATH = os.path.join(BASE_DIR, "calificacion.pl")
PRECIO_DB_PATH = os.path.join(BASE_DIR, "precio.pl")

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
        for game in con.do_query("juego(J,F,E)"):
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
    def create_game(self, name:str, date:str, state:str = "activo")->None:
        #obtener conexion
        con = PrologConnector.get_instance()
        
        name_lower = name.lower()
        date_lower = date.lower()
        state_lower = state.lower()
        
        # guardar en memoria de Prolog
        con.create_fact(f"juego({name_lower},{date_lower},{state_lower})")
        
        # guardar en archivo juegos.pl
        with open(DB_PATH, "a", encoding="utf-8") as f:
            f.write(f"juego({name_lower},{date_lower},{state_lower}).\n")
            
    #modificar el estado de un juego
    def update_game_state(self, name:str, state:str)->bool:
        con = PrologConnector.get_instance()
        name_lower = name.lower()
        state_lower = state.lower()
        
        # consultar la fecha del juego existente
        results = list(con.do_query(f"juego({name_lower}, F, _)"))
        if not results:
            return False
            
        date_val = results[0].get('F')
        
        # eliminar el hecho anterior y agregar el nuevo
        con.retract_fact(f"juego({name_lower},_,_)")
        con.create_fact(f"juego({name_lower},{date_val},{state_lower})")
        
        # reescribir juegos.pl
        games = self.get_games(limit=999999)
        with open(DB_PATH, "w", encoding="utf-8") as f:
            for game in games:
                j = game.get('J')
                date_str = game.get('F')
                st = game.get('E')
                if j and date_str and st:
                    f.write(f"juego({j},{date_str},{st}).\n")
        return True
        
    #eliminar un juego
    def delete_game(self, name:str)->None:
        #obtener conexion
        con = PrologConnector.get_instance()
        
        name_lower = name.lower()
        
        # eliminar de memoria de Prolog
        con.retract_fact(f"juego({name_lower},_,_)")
        
        # reescribir el archivo juegos.pl
        games = self.get_games(limit=999999)
        with open(DB_PATH, "w", encoding="utf-8") as f:
            for game in games:
                j = game.get('J')
                date_val = game.get('F')
                st = game.get('E')
                if j and date_val and st:
                    f.write(f"juego({j},{date_val},{st}).\n")
                    
        # eliminar relaciones de desarrollo
        con.retract_fact(f"desarrolla({name_lower},_)")
        devs = list(con.do_query("desarrolla(J,E)"))
        with open(DESARROLLOS_DB_PATH, "w", encoding="utf-8") as f:
            for dev in devs:
                j = dev.get('J')
                e = dev.get('E')
                if j and e:
                    f.write(f"desarrolla({j},{e}).\n")
                    
        # eliminar relaciones de disponibilidad
        con.retract_fact(f"disponible({name_lower},_)")
        disps = list(con.do_query("disponible(J,P)"))
        with open(DISPONIBILIDADES_DB_PATH, "w", encoding="utf-8") as f:
            for disp in disps:
                j = disp.get('J')
                p = disp.get('P')
                if j and p:
                    f.write(f"disponible({j},{p}).\n")
                    
        # eliminar relaciones de género
        con.retract_fact(f"genero({name_lower},_)")
        self._rewrite_generos(con)
        
        # eliminar calificaciones
        con.retract_fact(f"calificacion({name_lower},_)")
        self._rewrite_calificacion(con)
        
        # eliminar precios 
        con.retract_fact(f"precio({name_lower},_)")
        self._rewrite_precio(con)

    # añadir género
    def add_genre(self, game:str, genre:str)->None:
        con = PrologConnector.get_instance()
        game_lower = game.lower()
        genre_lower = genre.lower()
        con.create_fact(f"genero({game_lower},{genre_lower})")
        with open(GENEROS_DB_PATH, "a", encoding="utf-8") as f:
            f.write(f"genero({game_lower},{genre_lower}).\n")

    # eliminar género
    def delete_genre(self, game:str, genre:str)->None:
        con = PrologConnector.get_instance()
        game_lower = game.lower()
        genre_lower = genre.lower()
        con.retract_fact(f"genero({game_lower},{genre_lower})")
        self._rewrite_generos(con)

    # añadir calificación
    def add_rating(self, game:str, rating:float)->None:
        con = PrologConnector.get_instance()
        game_lower = game.lower()
        con.create_fact(f"calificacion({game_lower},{rating})")
        with open(CALIFICACION_DB_PATH, "a", encoding="utf-8") as f:
            f.write(f"calificacion({game_lower},{rating}).\n")

    # eliminar calificación
    def delete_rating(self, game:str)->None:
        con = PrologConnector.get_instance()
        game_lower = game.lower()
        con.retract_fact(f"calificacion({game_lower},_)")
        self._rewrite_calificacion(con)

    # añadir precio
    def add_price(self, game:str, price:float)->None:
        con = PrologConnector.get_instance()
        game_lower = game.lower()
        con.create_fact(f"precio({game_lower},{price})")
        with open(PRECIO_DB_PATH, "a", encoding="utf-8") as f:
            f.write(f"precio({game_lower},{price}).\n")

    # eliminar precio
    def delete_price(self, game:str)->None:
        con = PrologConnector.get_instance()
        game_lower = game.lower()
        con.retract_fact(f"precio({game_lower},_)")
        self._rewrite_precio(con)