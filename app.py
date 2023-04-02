from flask import Flask
from apis.usuario_service import usuario_endpoint
from apis.institucion_service import institucion_endpoint
from apis.proyecto_service import proyecto_endpoint
from apis.general_service import general_endpoint
from config import Config, get_db_conn 
from flask_restful import Api

app = Flask(__name__)

# Swagger config
api = Api(app)

# Sqlalchemy config
app.config.from_object(Config)
Config.init_app(app)

app.register_blueprint(usuario_endpoint)
app.register_blueprint(institucion_endpoint)
app.register_blueprint(proyecto_endpoint)
app.register_blueprint(general_endpoint)

@app.route('/')
def hello_world():
    conn, cursor = get_db_conn()
    return 'Hola, mundo!'

if __name__ == '__main__':
    app.run(debug=True)
