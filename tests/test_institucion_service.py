import datetime
import unittest
from flask import Flask
from apis.institucion_service import institucion_endpoint
from config import get_database_uri_test, db
from models.modelos import Institucion


class TestInstitucion(unittest.TestCase):

    def setUp(self):
        self.institucion_data = {
                'nombre': 'Institucion maderera',
                'descripcion': 'Expertos en madera.',
                'direccion': 'El bosque #111, Santiago, Chile.',
                'fecha_creacion': '2010-01-01'
            }
        self.institucion_2_data = {
                'nombre': 'Institucion acerera',
                'descripcion': 'Expertos en metales.',
                'direccion': 'El pilar #222, Las condes, Chile.',
                'fecha_creacion': '2011-01-01'
            }
        self.institucion_update_data = {
                'nombre': 'Institucion maderera',
                'descripcion': 'Expertos en madera y planchas de melamina.',
                'direccion': 'El bosque #333, Santiago, Chile.',
                'fecha_creacion': '2019-01-01'
            }
        self.app = Flask('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri_test()
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        self.app.register_blueprint(institucion_endpoint)

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
    
    def test_create_institucion(self):
        with self.app.test_client() as client:
            
            response = client.post('/instituciones', json=self.institucion_data)
            institucion = Institucion.query.filter_by(nombre=self.institucion_data['nombre']).first()

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(institucion)
            self.assertEqual(institucion.nombre, self.institucion_data['nombre'])
            self.assertEqual(institucion.direccion, self.institucion_data['direccion'])
    
    def test_get_instituciones(self):
        with self.app.test_client() as client:

            # Creamos dos instancias de Institucion
            institucion1 = Institucion(**self.institucion_data)
            institucion2 = Institucion(**self.institucion_2_data)

            # Agregamos las instancias a la base de datos
            with self.app.app_context():
                db.session.add(institucion1)
                db.session.add(institucion2)
                db.session.commit()

            # Hacemos una solicitud GET al endpoint para obtener todas las instituciones
            response = client.get('/instituciones')

            # Comprobamos que se hayan recibido ambas instituciones
            data = response.json
            self.assertEqual(len(data), 2)

            # Comprobamos que las instituciones recibidas sean las que agregamos previamente
            self.assertEqual(data[0]['nombre'], self.institucion_data['nombre'])
            self.assertEqual(data[1]['nombre'], self.institucion_2_data['nombre'])

    def test_get_institucion(self):
        with self.app.test_client() as client:
            # Creamos una institución de prueba
            institucion = Institucion(**self.institucion_data)

            with self.app.app_context():
                db.session.add(institucion)
                db.session.commit()

                # Hacemos una petición GET para obtener la institución creada
                response = client.get(f"/instituciones/{institucion.id}")
        
            # Comprobamos que la petición se hizo con éxito
            self.assertEqual(response.status_code, 200)

            # Comprobamos que los datos de la institución obtenida son correctos
            self.assertEqual(response.json["id"], institucion.id)
            self.assertEqual(response.json["nombre"], institucion.nombre)
            self.assertEqual(response.json["descripcion"], institucion.descripcion)
    
    def test_update_institucion(self):
        with self.app.test_client() as client:

            # Creamos una institución para actualizar
            institucion = Institucion(**self.institucion_data)
            with self.app.app_context():
                db.session.add(institucion)
                db.session.commit()

                # Enviamos la petición PUT para actualizar la institución
                response = client.put(f'/instituciones/{institucion.id}', json=self.institucion_update_data)

            # Verificamos que la petición se haya procesado correctamente
            self.assertEqual(response.status_code, 200)

            # Verificamos que la institución haya sido actualizada correctamente en la base de datos
            updated_institucion = Institucion.query.get(institucion.id)
            self.assertEqual(updated_institucion.descripcion, self.institucion_update_data['descripcion'])

    def test_delete_institucion(self):
        with self.app.test_client() as client:

            # Crear una institución
            institucion = Institucion(**self.institucion_data)

            with self.app.app_context():
                db.session.add(institucion)
                db.session.commit()

                # Realizar la petición DELETE para borrar la institución creada
                response = client.delete(f'/instituciones/{institucion.id}')
            data = response.get_json()
            
            # Verificar que se eliminó la institución correctamente
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Institucion eliminada exitosamente')

            # Verificar que la institución ya no existe en la base de datos
            institucion_eliminada = Institucion.query.filter_by(id=institucion.id).first()
            self.assertIsNone(institucion_eliminada)
    
    def test_get_proyectos_tiempo_restante(self):
        with self.app.test_client() as client:
            institucion = Institucion(**self.institucion_data)

            with self.app.app_context():
                db.session.add(institucion)
                db.session.commit()
                institucion = Institucion.query.get(institucion.id)

            with self.app.app_context():
                response = client.get(f'/instituciones/detalle-proyecto-y-responsables/{institucion.id}')

            self.assertEqual(response.status_code, 200)
            self.assertIn('proyectos', response.json)
            self.assertIsInstance(response.json['proyectos'], list)
    
    def test_get_instituciones_con_direccion(self):
        with self.app.test_client() as client:
            address_google = 'https://www.google.com/maps/search/'
            # Creamos una institución de prueba
            institucion = Institucion(**self.institucion_data)

            with self.app.app_context():
                db.session.add(institucion)
                db.session.commit()

            response = client.get(f'/instituciones/con-direccion')

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json, list)
            self.assertIn(address_google, response.json[0]['direccion'])
            