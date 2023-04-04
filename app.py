import json
from pathlib import Path
from flask import Flask
from apis.usuario_service import usuario_endpoint
from apis.institucion_service import institucion_endpoint
from apis.proyecto_service import proyecto_endpoint
from apis.general_service import general_endpoint
from config import Config 
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger config
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    '/api/docs',  
    API_URL,
    config={ 
        'app_name': "Test application"
    }
)

app.register_blueprint(swaggerui_blueprint)

# Sqlalchemy config
app.config.from_object(Config)
Config.init_app(app)

app.register_blueprint(usuario_endpoint)
app.register_blueprint(institucion_endpoint)
app.register_blueprint(proyecto_endpoint)
app.register_blueprint(general_endpoint)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
