import os
from .prolog import PrologConnector

# Rutas a los archivos de bases de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORMS_DB_PATH = os.path.join(BASE_DIR, "plataformas.pl")
DISPONIBILIDADES_DB_PATH = os.path.join(BASE_DIR, "disponibilidades.pl")

#repositorio de juegos
class PlatformsRepository:
    #metodos de operacion
    def get_platforms(self, limit:int)->list:
        #contenedor
        platforms = []
        
        #obtener conexion
        con = PrologConnector.get_instance()
        
        #obtener registros
        cont = 0
        for platform in con.do_query("plataforma(P)"):
            #hasta el limite
            if cont > limit:
                break
            
            #obtener datos
            platforms.append(platform)
            cont += 1
            
        #retornar registros    
        return platforms
    
    #verificar si existe
    def platform_exists(self, name:str)->bool:
        #realizar query
        con = PrologConnector.get_instance()
        
        #ejecutar la query
        query = con.do_query(f"esPlataforma({name.lower()})")
        
        #retornar respuesta
        return bool(list(query))
    
    #registrar un juego
    def create_platform(self, name:str)->None:
        #obtener conexion
        con = PrologConnector.get_instance()
        name_lower = name.lower()
        
        #crear registro en memoria
        con.create_fact(f"plataforma({name_lower})")
        
        # Guardar en archivo plataformas.pl
        with open(PLATFORMS_DB_PATH, "a", encoding="utf-8") as f:
            f.write(f"plataforma({name_lower}).\n")
        
    #eliminar un juego
    def delete_platform(self, name:str)->None:
        #obtener conexion
        con = PrologConnector.get_instance()
        name_lower = name.lower()
        
        #eliminar de memoria de Prolog
        con.retract_fact(f"plataforma({name_lower})")
        
        # Reescribir el archivo plataformas.pl
        platforms = self.get_platforms(limit=999999)
        with open(PLATFORMS_DB_PATH, "w", encoding="utf-8") as f:
            for platform in platforms:
                p = platform.get('P')
                if p:
                    f.write(f"plataforma({p}).\n")
                    
        # Eliminar también las disponibilidades asociadas a esta plataforma de Prolog
        con.retract_fact(f"disponible(_,{name_lower})")
        
        # Reescribir disponibilidades.pl
        disps = list(con.do_query("disponible(J,P)"))
        with open(DISPONIBILIDADES_DB_PATH, "w", encoding="utf-8") as f:
            for disp in disps:
                j = disp.get('J')
                p = disp.get('P')
                if j and p:
                    f.write(f"disponible({j},{p}).\n")
        
    #asignar juego
    def asign_game(self, game:str, platform:str)->bool:        
        game_lower = game.lower()
        platform_lower = platform.lower()
        
        con = PrologConnector.get_instance()
        
        # Verificar si el juego y la plataforma existen
        game_exists = bool(list(con.do_query(f"juego({game_lower}, _)")))
        platform_exists = bool(list(con.do_query(f"plataforma({platform_lower})")))
        
        if game_exists and platform_exists:
            # Registrar disponibilidad en la base de hechos
            con.create_fact(f"disponible({game_lower}, {platform_lower})")
            
            # Guardar en archivo disponibilidades.pl
            with open(DISPONIBILIDADES_DB_PATH, "a", encoding="utf-8") as f:
                f.write(f"disponible({game_lower},{platform_lower}).\n")
                
            return True
        return False