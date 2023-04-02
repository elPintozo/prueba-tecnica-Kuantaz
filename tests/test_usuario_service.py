import datetime
import unittest
from flask import Flask
from apis.usuario_service import usuario_endpoint
from models.modelos import Usuario
from config import get_database_uri_test, db


class TestUsuario(unittest.TestCase):

    def setUp(self):
        self.usuario_data = {
                'nombre': 'Juan',
                'apellidos': 'Perez',
                'rut': '12345678-9',
                'fecha_nacimiento': '1990-01-01',
                'cargo': 'Gerente',
                'edad': 30
            }
        self.usuario_2_data = {
                'nombre': 'Pedro',
                'apellidos': 'Alvi',
                'rut': '13345678-9',
                'fecha_nacimiento': '1991-01-01',
                'cargo': 'Operador',
                'edad': 33
            }
        self.usuario_update_data = {
                'nombre': 'Juan',
                'apellidos': 'Arce',
                'rut': '13345678-9',
                'fecha_nacimiento': '1990-01-01',
                'cargo': 'Gerente',
                'edad': 33
            }
        
        self.app = Flask('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri_test()
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        self.app.register_blueprint(usuario_endpoint)

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_create_usuario(self):
        with self.app.test_client() as client:
            response = client.post('/usuarios', json=self.usuario_data)

            # Comprueba que el usuario fue creado con éxito
            self.assertEqual(response.status_code, 200)
            self.assertIn('id', response.json)

            # Obtiene el usuario creado
            usuario = Usuario.query.get(response.json['id'])

            # Comprueba que los campos del usuario son correctos
            self.assertEqual(usuario.nombre, 'Juan')
            self.assertEqual(usuario.apellidos, 'Perez')
            self.assertEqual(usuario.rut, '12345678-9')
            self.assertEqual(usuario.fecha_nacimiento, datetime.date(1990,1,1))
            self.assertEqual(usuario.cargo, 'Gerente')
            self.assertEqual(usuario.edad, 30)

    def test_get_usuarios(self):
        with self.app.test_client() as client:

            # Crear una tabla de prueba
            usuario1 = Usuario(**self.usuario_data)
            usuario2 = Usuario(**self.usuario_2_data)

            with self.app.app_context():
                db.session.add(usuario1)
                db.session.add(usuario2)
                db.session.commit()

            # Hacer una petición GET al endpoint /usuarios
            response = client.get('/usuarios')

            # Verificar que la respuesta fue exitosa
            self.assertEqual(response.status_code, 200)
            self.assertIn('usuarios', response.json)

            # Verificar que la respuesta contiene los datos de los usuarios creados en el setUp
            data = response.json['usuarios']
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['nombre'], self.usuario_data['nombre'])
            self.assertEqual(data[0]['cargo'], self.usuario_data['cargo'])
            self.assertEqual(data[1]['apellidos'], self.usuario_2_data['apellidos'])
            self.assertEqual(data[1]['edad'], self.usuario_2_data['edad'])
    
    def test_get_usuario(self):
        with self.app.test_client() as client:

            usuario1 = Usuario(**self.usuario_data)

            with self.app.app_context():
                db.session.add(usuario1)
                db.session.commit()

                # Hacer una petición GET al endpoint /usuarios
                response = client.get(f'/usuarios/{usuario1.id}')

            # Verificar que la respuesta fue exitosa
            self.assertEqual(response.status_code, 200)
            
            data = response.json
            self.assertEqual(data['nombre'], self.usuario_data['nombre'])
            self.assertEqual(data['cargo'], self.usuario_data['cargo'])
            self.assertEqual(data['apellidos'], self.usuario_data['apellidos'])
            self.assertEqual(data['edad'], self.usuario_data['edad'])
    
    def test_update_usuario(self):
        with self.app.test_client() as client:

            usuario1 = Usuario(**self.usuario_data)
            with self.app.app_context():
                db.session.add(usuario1)
                db.session.commit()

                # Actualizar usuario
                response = client.put(f'/usuarios/{usuario1.id}', json=self.usuario_update_data)

            # Verificar respuesta del servidor
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Usuario actualizado correctamente')

            # Verificar que el usuario fue actualizado en la base de datos
            usuario_actualizado = Usuario.query.get(usuario1.id)
            self.assertEqual(usuario_actualizado.rut, self.usuario_update_data['rut'])
            self.assertEqual(usuario_actualizado.apellidos, self.usuario_update_data['apellidos'])
            self.assertEqual(usuario_actualizado.edad, self.usuario_update_data['edad'])
    
    def test_delete_usuario(self):
        with self.app.test_client() as client:
            usuario1 = Usuario(**self.usuario_data)

            with self.app.app_context():
                db.session.add(usuario1)
                db.session.commit()

                # Hacer una petición para borrar el usuario
                response = client.delete(f'/usuarios/{usuario1.id}')

            # Verificar que se haya eliminado el usuario
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Usuario eliminado correctamente')
            self.assertIsNone(Usuario.query.get(usuario1.id))
