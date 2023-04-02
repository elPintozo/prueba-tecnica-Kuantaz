from flask import Blueprint, jsonify, request
from config import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models.modelos import Proyecto

proyecto_endpoint = Blueprint('proyecto', __name__)

# CREATE
@proyecto_endpoint.route('/proyectos', methods=['POST'])
def create_proyecto():
    data = request.json
    proyecto = Proyecto(**data)
    try:
        if len(proyecto.validate())!=0:
             return jsonify({'message': 'Error al crear el proyecto', 'error:': proyecto.validate()})
        db.session.add(proyecto)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al crear el proyecto: {}'.format(str(e.orig))})
    return jsonify({'message': 'Proyecto creado correctamente', 'id': proyecto.id})

# READ ALL
@proyecto_endpoint.route('/proyectos', methods=['GET'])
def get_proyectos():
    proyectos = Proyecto.query.all()
    if proyectos:
        return jsonify([{
            'id': proyecto.id, 
            'nombre': proyecto.nombre, 
            'descripcion': proyecto.descripcion,
            'fecha_inicio': str(proyecto.fecha_inicio),
            'fecha_termino': str(proyecto.fecha_termino),
            'responsable_id': proyecto.responsable_id,
            'institucion_id': proyecto.institucion_id
            } for proyecto in proyectos]
        )
    return jsonify([])

# READ ONE
@proyecto_endpoint.route('/proyectos/<int:id>', methods=['GET'])
def get_proyecto(id):
    proyecto = Proyecto.query.get(id)
    if proyecto:
        return jsonify({
            'id': proyecto.id, 
            'nombre': proyecto.nombre, 
            'descripcion': proyecto.descripcion,
            'fecha_inicio': str(proyecto.fecha_inicio),
            'fecha_termino': str(proyecto.fecha_termino),
            'responsable_id': proyecto.responsable_id,
            'institucion_id': proyecto.institucion_id
            })
    else:
        return jsonify({'message': 'Proyecto no encontrado'})

# UPDATE
@proyecto_endpoint.route('/proyectos/<int:id>', methods=['PUT'])
def update_proyecto(id):
    data = request.json
    proyecto = Proyecto.query.get(id)
    if proyecto:
        proyecto.nombre = data['nombre']
        proyecto.descripcion = data['descripcion']
        proyecto.fecha_inicio = data['fecha_inicio']
        proyecto.fecha_termino = data['fecha_termino']
        db.session.add(proyecto)
        db.session.commit()
        return jsonify({'message': 'Proyecto actualizado correctamente.', 'id': proyecto.id, 'nombre': proyecto.nombre, 'descripcion': proyecto.descripcion})
    else:
        return jsonify({'message': 'Proyecto no encontrado'})

# DELETE
@proyecto_endpoint.route('/proyectos/<int:id>', methods=['DELETE'])
def delete_proyecto(id):
    proyecto = Proyecto.query.get(id)
    if proyecto:
        db.session.delete(proyecto)
        db.session.commit()
        return jsonify({'message': 'Proyecto eliminado correctamente'})
    else:
        return jsonify({'message': 'Proyecto no encontrado'})

# READ ALL WITH REMAINING DAYS
@proyecto_endpoint.route('/proyectos/tiempo-restante', methods=['GET'])
def get_proyectos_tiempo_restante():
    proyectos = Proyecto.query.all()
    if proyectos:
        proyectos_list = []
        for proyecto in proyectos:
            tiempo_restante = proyecto.fecha_termino - datetime.today().date()
            proyectos_list.append({'nombre': proyecto.nombre, 'tiempo_restante': tiempo_restante.days})
        return jsonify(proyectos_list)

    return jsonify([])