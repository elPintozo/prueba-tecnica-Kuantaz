from models.modelos import Usuario
from flask import Blueprint, jsonify, request
from config import db
from sqlalchemy.exc import IntegrityError

usuario_endpoint = Blueprint('usuario', __name__)

# CREATE
@usuario_endpoint.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.json
    new_usuario = Usuario(**data)
    try:
        if len(new_usuario.validate())!=0:
             return jsonify({'message': 'Error al crear el usuario', 'error:': new_usuario.validate()}), 400
        db.session.add(new_usuario)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'El usuario ya existe en la base de datos'}), 409
    return jsonify({'message': 'Usuario creado correctamente', 'id': new_usuario.id}), 201

# READ ALL
@usuario_endpoint.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellidos': usuario.apellidos,
            'rut': usuario.rut,
            'fecha_nacimiento': str(usuario.fecha_nacimiento),
            'cargo': usuario.cargo,
            'edad': usuario.edad,
            'proyectos': [proyecto.id for proyecto in usuario.proyectos]
        })
    return jsonify({'usuarios': usuarios_list})

# READ ONE
@usuario_endpoint.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        usuario_dict = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellidos': usuario.apellidos,
            'rut': usuario.rut,
            'fecha_nacimiento': str(usuario.fecha_nacimiento),
            'cargo': usuario.cargo,
            'edad': usuario.edad,
            'proyectos': [proyecto.id for proyecto in usuario.proyectos]
        }
        return jsonify(usuario_dict)
    else:
        return jsonify({'message': 'Usuario no encontrado'})

# READ ONE FROM RUT
@usuario_endpoint.route('/usuarios/por-rut/<string:rut>', methods=['GET'])
def get_usuario_por_rut(rut):
    usuario = Usuario.query.filter_by(rut=rut).first()
    if usuario:
        usuario_dict = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellidos': usuario.apellidos,
            'rut': usuario.rut,
            'fecha_nacimiento': str(usuario.fecha_nacimiento),
            'cargo': usuario.cargo,
            'edad': usuario.edad,
            'proyectos': [proyecto.id for proyecto in usuario.proyectos]
        }
        return jsonify(usuario_dict)
    else:
        return jsonify({'message': f'Usuario RUT:{rut} no encontrado.'})

# UPDATE
@usuario_endpoint.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        data = request.json
        usuario.nombre = data['nombre']
        usuario.apellidos = data['apellidos']
        usuario.rut = data['rut']
        usuario.fecha_nacimiento = data['fecha_nacimiento']
        usuario.cargo = data['cargo']
        usuario.edad = data['edad']
        db.session.commit()
        return jsonify({'message': 'Usuario actualizado correctamente'})
    else:
        return jsonify({'message': 'Usuario no encontrado'})

# DELETE
@usuario_endpoint.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado correctamente'})
    else:
        return jsonify({'message': 'Usuario no encontrado'})