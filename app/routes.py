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
    ordenar_por = request.args.get('ordenar_por', 'id')  # campo por defecto
    orden = request.args.get('orden', 'asc')             # ascendente por defecto
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    query = Libro.query

    # Búsqueda
    if titulo:
        query = query.filter(Libro.titulo.ilike(f'%{titulo}%'))
    if autor:
        query = query.filter(Libro.autor.ilike(f'%{autor}%'))
    if categoria:
        query = query.filter(Libro.categoria.ilike(f'%{categoria}%'))

    # Ordenamiento dinámico
    if hasattr(Libro, ordenar_por):
        campo = getattr(Libro, ordenar_por)
        if orden == 'desc':
            campo = campo.desc()
        else:
            campo = campo.asc()
        query = query.order_by(campo)

    # Paginación
    libros_paginados = query.paginate(page=page, per_page=limit, error_out=False)
    libros = [libro.to_dict() for libro in libros_paginados.items]

    return jsonify({
        'libros': libros,
        'pagina_actual': page,
        'total_paginas': libros_paginados.pages,
        'total_libros': libros_paginados.total
    })

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
