import datetime
from config import db

class Institucion(db.Model):
    __tablename__ = 'instituciones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    direccion = db.Column(db.String(255))
    fecha_creacion = db.Column(db.Date)
    proyectos = db.relationship('Proyecto', backref='institucion', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'direccion': self.direccion,
            'fecha_creacion': str(self.fecha_creacion)
        }
    
    def validate(self):
        errors = []
        
        # Validar tipo de datos del campo 'nombre'
        if not isinstance(self.nombre, str):
            errors.append("El campo 'nombre' debe ser de tipo cadena de texto.")

        # Validar tipo de datos del campo 'descripcion'
        if not isinstance(self.descripcion, str):
            errors.append("El campo 'descripcion' debe ser de tipo cadena de texto.")
        
        # Validar tipo de datos del campo 'direccion'
        if not isinstance(self.direccion, str):
            errors.append("El campo 'direccion' debe ser de tipo cadena de texto.")

        # Validar tipo de datos del campo 'fecha_creacion'
        try:
            datetime.datetime.strptime(str(self.fecha_creacion), '%Y-%m-%d')
        except ValueError:
            errors.append("El campo 'fecha_creacion' debe estar en el formato YYYY-MM-DD")

        return errors
    
class Proyecto(db.Model):
    __tablename__ = 'proyectos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date)
    fecha_termino = db.Column(db.Date)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    institucion_id = db.Column(db.Integer, db.ForeignKey('instituciones.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_inicio': str(self.fecha_inicio),
            'fecha_termino': str(self.fecha_termino),
            'responsable_id': self.responsable_id,
            'institucion_id': self.institucion_id
        }
    
    def get_detalles_con_responsable(self):
        return {
            'Nombre proyecto': self.nombre,
            'Id proyecto': self.id,
            'Nombre responsable': Usuario.query.get(self.responsable_id).nombre,
            'Id responsable': self.responsable_id,
        }
    
    def validate(self):
        errors = []

        # Validar tipo de datos del campo 'nombre'
        if not isinstance(self.nombre, str):
            errors.append("El campo 'nombre' debe ser de tipo cadena de texto.")

        # Validar tipo de datos del campo 'descripcion'
        if not isinstance(self.descripcion, str):
            errors.append("El campo 'descripcion' debe ser de tipo cadena de texto.")

        # Validar tipo de datos del campo 'fecha_inicio'
        try:
            datetime.datetime.strptime(str(self.fecha_inicio), '%Y-%m-%d')
        except ValueError:
            errors.append("El campo 'fecha_inicio' debe estar en el formato YYYY-MM-DD")

        # Validar tipo de datos del campo 'fecha_termino'
        try:
            datetime.datetime.strptime(str(self.fecha_termino), '%Y-%m-%d')
        except ValueError:
            errors.append("El campo 'fecha_termino' debe estar en el formato YYYY-MM-DD")

        # Validar tipo de datos del campo 'responsable_id'
        if not isinstance(self.responsable_id, int):
            errors.append("El campo 'responsable_id' debe ser de tipo entero.")

        # Validar tipo de datos del campo 'institucion_id'
        if not isinstance(self.institucion_id, int):
            errors.append("El campo 'institucion_id' debe ser de tipo entero.")
        

        return errors

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellidos = db.Column(db.String(255))
    rut = db.Column(db.String(20), unique=True)
    fecha_nacimiento = db.Column(db.Date)
    cargo = db.Column(db.String(255))
    edad = db.Column(db.Integer)
    proyectos = db.relationship('Proyecto', backref='responsable', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'rut': self.rut,
            'fecha_nacimiento': str(self.fecha_nacimiento),
            'cargo': self.cargo,
            'edad': self.edad
        }

    def validate(self):
        errors = []

        # Validar tipo de datos del campo 'nombre'
        if not isinstance(self.nombre, str):
            errors.append("El campo 'nombre' debe ser de tipo cadena de texto.")

        # Validar tipo de datos del campo 'apellidos'
        if not isinstance(self.apellidos, str):
            errors.append("El campo 'apellidos' debe ser de tipo cadena de texto.")

        # Validar tipo de datos del campo 'rut'
        if not isinstance(self.rut, str):
            errors.append("El campo 'rut' debe ser de tipo cadena de texto.")

        # Validar tipo de datos del campo 'fecha_nacimiento'
        try:
            datetime.datetime.strptime(str(self.fecha_nacimiento), '%Y-%m-%d')
        except ValueError:
            errors.append("El campo 'fecha_nacimiento' debe estar en el formato YYYY-MM-DD")

        # Validar tipo de datos del campo 'cargo'
        if not isinstance(self.cargo, str):
            errors.append("El campo 'cargo' debe ser de tipo cadena de texto.")

        # Validar tipo de datos del campo 'edad'
        if not isinstance(self.edad, int):
            errors.append("El campo 'edad' debe ser de tipo entero.")

        return errors

