from flask import Blueprint, request, jsonify                   # Importa herramientas para rutas, petición y respuesta JSON
from .models import Libro, ESTADOS_LIBRO                        # Importa el modelo Libro y la lista de estados válidos
from . import db                                                # Importa la instancia global de la base de datos

libros_bp = Blueprint('libros', __name__)                       # Crea un Blueprint llamado 'libros' para agrupar todas las rutas relacionadas

@libros_bp.route('/libros', methods=['GET'])                    # Define la ruta GET /libros para obtener todos los libros
def obtener_libros():
    libros = Libro.query.all()                                  # Consulta todos los libros de la base de datos
    return jsonify([libro.to_dict() for libro in libros])       # Convierte cada libro a diccionario y lo devuelve como JSON

@libros_bp.route('/libros/<int:id>', methods=['GET'])           # Define la ruta GET /libros/<id> para obtener un libro específico por ID
def obtener_libro(id):
    libro = Libro.query.get_or_404(id)                          # Busca el libro por ID o devuelve error 404 si no existe
    return jsonify(libro.to_dict())                             # Devuelve el libro encontrado en formato JSON

@libros_bp.route('/libros', methods=['POST'])                   # Define la ruta POST /libros para crear un nuevo libro
def crear_libro():
    data = request.get_json()                                   # Obtiene los datos del cuerpo del request en formato JSON
    error_estado = validar_libro(data)                          # Valida si el estado del libro es válido
    if error_estado:
        return jsonify({'error': error_estado}), 403            # Si el estado no es válido, responde con error 403

    nuevo_libro = Libro(                                        # Crea una nueva instancia del modelo Libro con los datos recibidos
        titulo=data['titulo'],                                  # Asigna el título desde el JSON
        autor=data['autor'],                                    # Asigna el autor
        isbn=data['isbn'],                                      # Asigna el ISBN
        categoria=data['categoria'],                            # Asigna la categoría
        estado=data.get('estado', 'disponible')                 # Asigna el estado o 'disponible' por defecto si no se envió
    )
    db.session.add(nuevo_libro)                                 # Agrega el nuevo libro a la sesión de base de datos
    db.session.commit()                                         # Guarda los cambios en la base de datos
    return jsonify(nuevo_libro.to_dict()), 201                  # Devuelve el libro creado con código HTTP 201 (creado)

@libros_bp.route('/libros/<int:id>', methods=['PUT'])          # Define la ruta PUT /libros/<id> para actualizar un libro existente
def actualizar_libro(id):
    libro = Libro.query.get_or_404(id)                          # Busca el libro por ID o devuelve error 404
    data = request.get_json()                                   # Obtiene los datos nuevos en formato JSON

    error_estado = validar_libro(data)                          # Valida el estado recibido
    if error_estado:
        return jsonify({'error': error_estado}), 403            # Si es inválido, devuelve error 403

    libro.titulo = data.get('titulo', libro.titulo)            # Actualiza el título si se envió; si no, lo deja igual
    libro.autor = data.get('autor', libro.autor)                # Igual para el autor
    libro.isbn = data.get('isbn', libro.isbn)                   # Igual para el ISBN
    libro.categoria = data.get('categoria', libro.categoria)   # Igual para la categoría
    libro.estado = data.get('estado', libro.estado)            # Igual para el estado

    db.session.commit()                                         # Guarda los cambios en la base de datos
    return jsonify(libro.to_dict())                             # Devuelve el libro actualizado como JSON

@libros_bp.route('/libros/<int:id>', methods=['DELETE'])       # Define la ruta DELETE /libros/<id> para eliminar un libro
def eliminar_libro(id):
    libro = Libro.query.get_or_404(id)                          # Busca el libro por ID o devuelve error 404
    db.session.delete(libro)                                    # Marca el libro para eliminarlo
    db.session.commit()                                         # Confirma la eliminación en la base de datos
    return jsonify({'mensaje': 'Libro eliminado correctamente'})# Devuelve un mensaje de éxito como JSON

@libros_bp.route('/libros/buscar', methods=['GET'])            # Define la ruta GET /libros/buscar para buscar libros con filtros
def buscar_libros():
    titulo = request.args.get('titulo')                         # Obtiene el valor del parámetro 'titulo' desde la URL
    autor = request.args.get('autor')                           # Obtiene el valor de 'autor'
    categoria = request.args.get('categoria')                   # Obtiene el valor de 'categoria'

    query = Libro.query                                         # Inicia la consulta sobre todos los libros
    if titulo:
        query = query.filter(Libro.titulo.ilike(f'%{titulo}%'))# Si se pasó un título, filtra los que lo contienen (insensible a mayúsculas)
    if autor:
        query = query.filter(Libro.autor.ilike(f'%{autor}%'))  # Filtra por autor si se pasó
    if categoria:
        query = query.filter(Libro.categoria.ilike(f'%{categoria}%')) # Filtra por categoría si se pasó

    libros = query.all()                                        # Ejecuta la consulta y obtiene los libros filtrados
    return jsonify([libro.to_dict() for libro in libros])       # Devuelve la lista de libros como JSON

def validar_libro(data):                                        # Función auxiliar para validar el estado de un libro
    estado = data.get('estado', 'disponible')                   # Obtiene el estado del libro o 'disponible' si no está
    if estado not in ESTADOS_LIBRO:
        return f'Estado inválido: "{estado}". Debe ser uno de {ESTADOS_LIBRO}' # Devuelve un mensaje de error si el estado no es válido
    return None                                                 # Si el estado es válido, devuelve None