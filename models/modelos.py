from config import db

class Institucion(db.Model):
    __tablename__ = 'instituciones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    direccion = db.Column(db.String(255))
    fecha_creacion = db.Column(db.Date)
    proyectos = db.relationship('Proyecto', backref='institucion', lazy=True)

class Proyecto(db.Model):
    __tablename__ = 'proyectos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date)
    fecha_termino = db.Column(db.Date)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    institucion_id = db.Column(db.Integer, db.ForeignKey('instituciones.id'), nullable=False)

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

