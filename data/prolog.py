from pyswip import Prolog

#clase conectora de prolog
class PrologConnector:
    #conexion
    connection = None
    
    #constructor de clase
    def __init__(self):
        #objeto de conexion
        self.plg = Prolog()

        #cargar el archivo
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        main_pl_path = os.path.join(base_dir, "main.pl").replace("\\", "/")
        self.plg.consult(main_pl_path)
        
    def do_query(self, query:str):
        #realizar la query
        return self.plg.query(query)
    
    def create_fact(self, fact:str)->None:
        #añade a la base de hechos
        self.plg.assertz(fact)
        
    def retract_fact(self, fact:str)->None:
        #elimina el registro
        self.plg.retract(fact)
        
    #metodo singleton
    @classmethod
    def get_instance(cls)->PrologConnector:
        #validar instancia
        if not cls.connection:
            cls.connection = PrologConnector()
            
        #retornar conexion
        return cls.connection