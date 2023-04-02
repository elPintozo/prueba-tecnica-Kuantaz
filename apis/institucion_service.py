from flask import Blueprint, request, jsonify
from config import db
from models.modelos import Institucion

institucion_endpoint = Blueprint('institucion', __name__)

# CREATE
@institucion_endpoint.route('/instituciones', methods=['POST'])
def create_institucion():
    data = request.json
    institucion = Institucion(**data)
    db.session.add(institucion)
    db.session.commit()
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
        'proyectos': inst.proyectos,

    } for inst in instituciones])

# READ ONE
@institucion_endpoint.route('/instituciones/<int:id>', methods=['GET'])
def get_institucion(id):
    institucion = Institucion.query.get_or_404(id)
    return jsonify({
        'id': institucion.id,
        'nombre': institucion.nombre,
        'descripcion': institucion.descripcion,
        'direccion': institucion.direccion,
        'fecha_creacion': str(institucion.fecha_creacion),
        'proyectos': institucion.proyectos,
    })

# UPDATE
@institucion_endpoint.route('/instituciones/<int:id>', methods=['PUT'])
def update_institucion(id):
    institucion = Institucion.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(institucion, key, value)
    db.session.commit()
    return jsonify({'message': 'Institución actualizada correctamente'})

# DELETE
@institucion_endpoint.route('/instituciones/<int:id>', methods=['DELETE'])
def delete_institucion(id):
    institucion = Institucion.query.get(id)
    if not institucion:
        return jsonify({'error': 'Institucion no encontrada'}), 404
    db.session.delete(institucion)
    db.session.commit()
    return jsonify({'message': 'Institucion eliminada exitosamente'})
