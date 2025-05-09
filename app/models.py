from . import db                            # Importa la instancia de SQLAlchemy
from datetime import datetime               # Para manejar fechas

# Lista de estados válidos de un libro
ESTADOS_LIBRO = ['disponible', 'prestado', 'no devuelto', 'roto']

class Libro(db.Model):                      # Define el modelo Libro (tabla en la base de datos)
    __tablename__ = 'libros'                # Nombre explícito de la tabla

    id = db.Column(db.Integer, primary_key=True)                 # ID autoincremental
    titulo = db.Column(db.String(255), nullable=False)          # Título obligatorio
    autor = db.Column(db.String(255), nullable=False)           # Autor obligatorio
    isbn = db.Column(db.String(13), unique=True, nullable=False)# ISBN único y obligatorio
    categoria = db.Column(db.String(100), nullable=False)       # Categoría obligatoria
    estado = db.Column(db.String(50), default="disponible")     # Estado opcional (default)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de creación (automática)

    def to_dict(self):
        # Convierte el objeto a un diccionario para devolverlo como JSON
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'isbn': self.isbn,
            'categoria': self.categoria,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }