import os  # Módulo para manejar rutas del sistema operativo

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) # Define la ruta absoluta del directorio actual

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'biblioteca.db') # URI para conectar con la base de datos SQLite en el archivo biblioteca.db   
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desactiva el seguimiento de modificaciones (reduce el consumo de memoria)