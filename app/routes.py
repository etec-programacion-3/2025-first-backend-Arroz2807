from flask import Blueprint, request, jsonify
from .models import Libro
from . import db

libros_bp = Blueprint('libros', __name__)

@libros_bp.route('/libros', methods=['GET'])
def obtener_libros():
    libros = Libro.query.all()
    return jsonify([libro.to_dict() for libro in libros])

@libros_bp.route('/libros/buscar', methods=['GET'])
def buscar_libros():
    titulo = request.args.get('titulo')
    autor = request.args.get('autor')
    categoria = request.args.get('categoria')

    query = Libro.query

    if titulo:
        query = query.filter(Libro.titulo.ilike(f'%{titulo}%'))
    if autor:
        query = query.filter(Libro.autor.ilike(f'%{autor}%'))
    if categoria:
        query = query.filter(Libro.categoria.ilike(f'%{categoria}%'))

    libros = query.all()

    return jsonify([libro.to_dict() for libro in libros])

@libros_bp.route('/libros/<int:id>', methods=['GET'])
def obtener_libro(id):
    libro = Libro.query.get_or_404(id)
    return jsonify(libro.to_dict())

@libros_bp.route('/libros', methods=['POST'])
def crear_libro():
    data = request.get_json()
    errores = validar_libro(data)
    if errores:
        return jsonify({'error': errores}), 400

    nuevo_libro = Libro(
        titulo=data['titulo'],
        autor=data['autor'],
        isbn=data['isbn'],
        categoria=data['categoria'],
        estado=data.get('estado', 'disponible')
    )
    db.session.add(nuevo_libro)
    db.session.commit()
    return jsonify(nuevo_libro.to_dict()), 201

@libros_bp.route('/libros/<int:id>', methods=['PUT'])
def actualizar_libro(id):
    libro = Libro.query.get_or_404(id)
    data = request.get_json()

    errores = validar_libro(data, update=True)
    if errores:
        return jsonify({'error': errores}), 400

    libro.titulo = data.get('titulo', libro.titulo)
    libro.autor = data.get('autor', libro.autor)
    libro.isbn = data.get('isbn', libro.isbn)
    libro.categoria = data.get('categoria', libro.categoria)
    libro.estado = data.get('estado', libro.estado)

    db.session.commit()
    return jsonify(libro.to_dict())

@libros_bp.route('/libros/<int:id>', methods=['DELETE'])
def eliminar_libro(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    return jsonify({'mensaje': 'Libro eliminado correctamente'})

def validar_libro(data, update=False):
    errores = []
    campos_obligatorios = ['titulo', 'autor', 'isbn', 'categoria']
    for campo in campos_obligatorios:
        if not update and campo not in data:
            errores.append(f'El campo "{campo}" es obligatorio')
    return errores
