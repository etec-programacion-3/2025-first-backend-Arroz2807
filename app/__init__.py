from flask import Flask                      # Crea la app Flask
from flask_sqlalchemy import SQLAlchemy      # ORM para manejar la base de datos relacional (SQLAlchemy)
from flask_migrate import Migrate            # Permite crear y aplicar migraciones de base de datos (Flask-Migrate)
from config import Config                    # Importa la configuración desde config.py
from flask_cors import CORS

# Instancias globales
db = SQLAlchemy()     # Instancia global del ORM SQLAlchemy (se usa en modelos y para interactuar con la DB)
                      # No se asocia aún a ninguna app, lo hará con db.init_app(app)
                      # Permite definir modelos como clases Python (como Libro)

migrate = Migrate()   # Instancia global del gestor de migraciones (Flask-Migrate)
                      # Se conecta con la app y el ORM más adelante con migrate.init_app(app, db)
                      # Permite generar scripts para crear/modificar tablas con `flask db migrate/upgrade`

def create_app():
    app = Flask(__name__)                   # Crea la instancia de la aplicación Flask
    app.config.from_object(Config)          # Carga configuración (como la URI de la base de datos)

    # Habilitar CORS para todos los endpoints
    CORS(app)

    db.init_app(app)                        # Inicializa SQLAlchemy con la app (vincula ORM con Flask)
    migrate.init_app(app, db)               # Inicializa Flask-Migrate (conecta app + ORM para usar migraciones)

    from .models import Libro               # Importa el modelo para que Migrate lo reconozca
    from .routes import libros_bp           # Importa el Blueprint con las rutas relacionadas a libros
    app.register_blueprint(libros_bp)       # Registra el Blueprint: ahora las rutas /libros existen en la app

    return app                              # Devuelve la aplicación ya configurada