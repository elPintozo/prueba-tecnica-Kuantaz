from flask import Blueprint, request, jsonify
from config import db
from sqlalchemy.exc import IntegrityError
from models.modelos import Institucion

institucion_endpoint = Blueprint('institucion', __name__)

# CREATE
@institucion_endpoint.route('/instituciones', methods=['POST'])
def create_institucion():
    data = request.json
    institucion = Institucion(**data)
    try:
        if len(institucion.validate())!=0:
             return jsonify({'message': 'Error al crear la institución', 'error:': institucion.validate()})
        db.session.add(institucion)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al crear la institución: {}'.format(str(e.orig))})
    return jsonify({'message': 'Institución creada correctamente', 'id': institucion.id})

# READ ALL
@institucion_endpoint.route('/instituciones', methods=['GET'])
def get_instituciones():
    instituciones = Institucion.query.all()
    return jsonify([{
        'id': inst.id,
        'nombre': inst.nombre,
        'descripcion': inst.descripcion,
        'direccion': inst.direccion,
        'fecha_creacion': str(inst.fecha_creacion),
        'proyectos': [proyecto.id for proyecto in inst.proyectos]

    } for inst in instituciones])

# READ ALL WITH ADDRESS
@institucion_endpoint.route('/instituciones/con-direccion', methods=['GET'])
def get_instituciones_con_direccion():
    address_google = 'https://www.google.com/maps/search/'
    instituciones = Institucion.query.all()
    return jsonify([{
        'id': inst.id,
        'nombre': inst.nombre,
        'descripcion': inst.descripcion,
        'direccion': f"{address_google}{inst.direccion}{inst.nombre[:3]}",
        'fecha_creacion': str(inst.fecha_creacion),
        'proyectos': [proyecto.id for proyecto in inst.proyectos]

    } for inst in instituciones])

# READ ONE
@institucion_endpoint.route('/instituciones/<int:id>', methods=['GET'])
def get_institucion(id):
    institucion = Institucion.query.get(id)
    if institucion:
        return jsonify({
            'id': institucion.id,
            'nombre': institucion.nombre,
            'descripcion': institucion.descripcion,
            'direccion': institucion.direccion,
            'fecha_creacion': str(institucion.fecha_creacion),
            'proyectos': institucion.proyectos,
        })
    else:
        return jsonify({'message': 'Institución no encontrada'})

# READ ONE WITH DETAILS
@institucion_endpoint.route('/instituciones/detalle-proyecto-y-responsables/<int:id>', methods=['GET'])
def get_institucion_con_proyectos_y_responsables(id):
    institucion = Institucion.query.get(id)
    if institucion:
        return jsonify({
            'id': institucion.id,
            'nombre': institucion.nombre,
            'descripcion': institucion.descripcion,
            'direccion': institucion.direccion,
            'fecha_creacion': str(institucion.fecha_creacion),
            'proyectos': [proyecto.get_detalles_con_responsable() for proyecto in institucion.proyectos],
        })
    else:
        return jsonify({'message': 'Institución no encontrada'})

# UPDATE
@institucion_endpoint.route('/instituciones/<int:id>', methods=['PUT'])
def update_institucion(id):
    institucion = Institucion.query.get(id)
    if institucion:
        data = request.json
        for key, value in data.items():
            setattr(institucion, key, value)
        db.session.commit()
        return jsonify({'message': 'Institución actualizada correctamente'})
    else:
        return jsonify({'message': 'Institución no encontrada'})

# DELETE
@institucion_endpoint.route('/instituciones/<int:id>', methods=['DELETE'])
def delete_institucion(id):
    institucion = Institucion.query.get(id)
    if not institucion:
        return jsonify({'error': 'Institucion no encontrada'})
    db.session.delete(institucion)
    db.session.commit()
    return jsonify({'message': 'Institucion eliminada exitosamente'})
