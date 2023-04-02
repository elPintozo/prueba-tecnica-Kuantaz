import datetime
import unittest
from flask import Flask
from apis.proyecto_service import proyecto_endpoint
from config import get_database_uri_test, db
from models.modelos import Institucion, Proyecto, Usuario


class TestUsuario(unittest.TestCase):

    def setUp(self):
        # Data complementaria para los proyectos
        self.usuario_data = {
                'nombre': 'Juan',
                'apellidos': 'Perez',
                'rut': '15345678-9',
                'fecha_nacimiento': '1990-01-01',
                'cargo': 'Gerente',
                'edad': 30
            }
        # Se crea un registro de usuario para las pruebas
        self.usuario1 = Usuario(**self.usuario_data)
        self.institucion_data = {
                'nombre': 'Institucion maderera',
                'descripcion': 'Expertos en madera.',
                'direccion': 'El bosque #111, Santiago, Chile.',
                'fecha_creacion': '2010-01-01'
            }
        # Se crea un registro de instituto para las pruebas
        self.institucion1 = Institucion(**self.institucion_data)

        self.app = Flask('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri_test()
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        self.app.register_blueprint(proyecto_endpoint)

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()
            db.session.add(self.usuario1)
            db.session.add(self.institucion1)
            db.session.commit()

            # Data para test de proyectos
            self.proyecto_data = {
                    'nombre': 'Proyecto uno',
                    'descripcion': 'Empieza con retrasos',
                    'fecha_inicio': '2023-01-01',
                    'fecha_termino': '2024-01-01',
                    'responsable_id': self.usuario1.id,
                    'institucion_id': self.institucion1.id
                }
            self.proyecto_2_data = {
                    'nombre': 'Proyecto dos',
                    'descripcion': 'Proyecto inmobiliario',
                    'fecha_inicio': '2024-01-01',
                    'fecha_termino': '2024-09-01',
                    'responsable_id': self.usuario1.id,
                    'institucion_id': self.institucion1.id
                }
            self.proyecto_update_data = {
                    'nombre': 'Proyecto uno',
                    'descripcion': 'Proyecto con retrasos y con falta de presupuestos',
                    'fecha_inicio': '2022-01-01',
                    'fecha_termino': '2025-01-01',
                    'responsable_id': self.usuario1.id,
                    'institucion_id': self.institucion1.id
                }
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
    
    def test_create_proyecto(self):
        with self.app.test_client() as client:

            response = client.post('/proyectos', json=self.proyecto_data)
            data = response.get_json()

            # Verificamos que el proyecto fue creado correctamente
            self.assertEqual(response.status_code, 200)
            self.assertIn('id', response.json)

            # Obtengo el proyecto creado
            proyecto = Proyecto.query.get(response.json['id'])

            self.assertEqual(proyecto.nombre, self.proyecto_data['nombre'])
            self.assertEqual(proyecto.descripcion, self.proyecto_data['descripcion'])
            self.assertEqual(proyecto.fecha_inicio, datetime.date(2023,1,1))
            self.assertEqual(proyecto.fecha_termino, datetime.date(2024,1,1))
    
    def test_get_proyectos(self):
        with self.app.test_client() as client:
            proyecto1 = Proyecto(**self.proyecto_data)
            proyecto2 = Proyecto(**self.proyecto_2_data)

            with self.app.app_context():
                db.session.add(proyecto1)
                db.session.add(proyecto2)
                db.session.commit()

            response = client.get('/proyectos')
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 2)

            # Verificamos que la información de cada proyecto sea correcta
            self.assertEqual(data[0]['nombre'], self.proyecto_data['nombre'])
            self.assertEqual(data[0]['descripcion'], self.proyecto_data['descripcion'])
            self.assertEqual(data[1]['nombre'], self.proyecto_2_data['nombre'])
            self.assertEqual(data[1]['descripcion'], self.proyecto_2_data['descripcion'])
    
    def test_get_proyecto(self):
        with self.app.test_client() as client:
            proyecto = Proyecto(**self.proyecto_data)

            with self.app.app_context():
                db.session.add(proyecto)
                db.session.commit()
            
                response = client.get(f'/proyectos/{proyecto.id}')

            data = response.get_json()
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['id'], proyecto.id)
            self.assertEqual(data['nombre'], proyecto.nombre)
            self.assertEqual(data['descripcion'], proyecto.descripcion)
            self.assertEqual(data['fecha_inicio'], str(proyecto.fecha_inicio))
    
    def test_update_proyecto(self):
        with self.app.test_client() as client:

            proyecto = Proyecto(**self.proyecto_data)
            with self.app.app_context():
                db.session.add(proyecto)
                db.session.commit()

                # Actualizar usuario
                response = client.put(f'/proyectos/{proyecto.id}', json=self.proyecto_update_data)

            # Verificar respuesta del servidor
            self.assertEqual(response.status_code, 200)
            self.assertIn('id', response.json)
            self.assertIn('nombre', response.json)

            # Verificar que el usuario fue actualizado en la base de datos
            proyecto_actualizado = Proyecto.query.get(proyecto.id)
            self.assertEqual(proyecto_actualizado.nombre, self.proyecto_update_data['nombre'])
            self.assertEqual(proyecto_actualizado.descripcion, self.proyecto_update_data['descripcion'])
        
    def test_delete_proyecto(self):
        with self.app.test_client() as client:

            # Crear un proyecto de prueba
            proyecto = Proyecto(**self.proyecto_data)
            with self.app.app_context():
                db.session.add(proyecto)
                db.session.commit()

                # Enviar la solicitud de eliminación
                response = self.client.delete(f'/proyectos/{proyecto.id}')

                # Verificar que el proyecto fue eliminado
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json['message'], 'Proyecto eliminado correctamente')
                self.assertIsNone(Proyecto.query.get(proyecto.id))

    def test_get_proyectos_tiempo_restante(self):
        with self.app.test_client() as client:
            response = client.get(f'/proyectos/tiempo-restante')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)



