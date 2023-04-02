import unittest
from app import get_db_conn

class TestDbConnection(unittest.TestCase):

    def test_db_connection(self):
        conn, cursor = get_db_conn()
        self.assertIsNotNone(conn, "La conexión a la base de datos falló")
        self.assertIsNotNone(cursor, "No se pudo obtener un cursor de la base de datos")
        conn.close()

if __name__ == '__main__':
    unittest.main()

# To test: python -m unittest discover -s tests