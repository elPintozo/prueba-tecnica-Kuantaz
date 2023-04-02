from flask import Blueprint, jsonify
from models.modelos import Institucion, Proyecto, Usuario

general_endpoint = Blueprint('general', __name__)

# READ ALL DATA 
@general_endpoint.route('/todo', methods=['GET'])
def get_todo():
    instituciones = Institucion.query.all()
    proyectos = Proyecto.query.all()
    usuarios = Usuario.query.all()

    return jsonify({
        'usuarios': [usuario.to_dict() for usuario in usuarios],
        'proyectos': [proyecto.to_dict() for proyecto in proyectos],
        'instituciones': [institucion.to_dict() for institucion in instituciones]
    })