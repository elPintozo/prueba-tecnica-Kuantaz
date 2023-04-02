import datetime
import unittest
from flask import Flask
from models.modelos import Usuario
from apis.general_service import general_endpoint
from config import get_database_uri_test, db


class TestUsuario(unittest.TestCase):

    def setUp(self):
        self.app = Flask('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri_test()
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        self.app.register_blueprint(general_endpoint)

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_usuarios(self):
        with self.app.test_client() as client:

            response = client.get('/todo')

            # Verificar que la respuesta fue exitosa
            self.assertEqual(response.status_code, 200)
            self.assertIn('usuarios', response.json)
            self.assertIn('proyectos', response.json)
            self.assertIn('instituciones', response.json)
    