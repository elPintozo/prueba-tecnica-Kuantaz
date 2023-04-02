from models.modelos import Usuario
from flask import Blueprint, jsonify, request
from config import db

usuario_endpoint = Blueprint('usuario', __name__)

# CREATE
@usuario_endpoint.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.json
    new_usuario = Usuario(**data)
    db.session.add(new_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario creado correctamente', 'id': new_usuario.id})

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
            'edad': usuario.edad
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
            'edad': usuario.edad
        }
        return jsonify(usuario_dict)
    else:
        return jsonify({'message': 'Usuario no encontrado'})

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