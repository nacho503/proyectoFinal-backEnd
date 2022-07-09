import mailbox
from flask_sqlalchemy import SQLAlchemy

#instacia de sqlalchemy
db = SQLAlchemy()

#####################################
class Usuario(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(20),nullable=False)
    mail=db.Column(db.String(50),nullable=False)
    favoritos=db.relationship('Favorito',backref="usuario", lazy=True)
    receta=db.relationship('Receta',backref="usuario", lazy=True)
    despensa=db.relationship('Despensa',backref="usuario", lazy=True)
    comentario_valor=db.relationship('Comentario_Valor',backref="usuario", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.nombre

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "password": self.password,
            "mail":self.mail
        }

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False) 
    id_receta = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable=False)

    def __repr__(self):
        return "<Favorito %r>" % self.id #no se cual va aqui

    def serialize(self):
        return {
            "id":self.id,
            "id_usuario": self.id_usuario,
            "id_receta": self.id_receta
        }

class Receta(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), nullable=False)
    nombre_receta = db.Column(db.String(250),nullable=False)
    fecha_creacion = db.Column(db.DateTime(250),nullable=False)
    paso_a_paso = db.Column(db.String(250),nullable=False)
    imagen_receta=db.Column(db.Text,nullable=False)
    comentario_valor = db.relationship('Comentario_Valor', backref='receta', lazy=True)
    favorito = db.relationship('Favorito', backref='receta', lazy=True) 

    def __repr__(self):
        return "<Receta %r>" % self.nombre #no se cual va aqui

    def serialize(self):
        return {
            "id":self.id,
            "id_usuario": self.id_usuario,
            "id_ingrediente": self.id_ingrediente,
            "nombre_receta": self.nombre_receta,
            "fecha_creacion": self.fecha_creacion,
            "paso_a_paso": self.paso_a_paso
        }


class Ingrediente(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN
    id = db.Column(db.Integer, primary_key=True)
    nombre_ingrediente = db.Column(db.String(250),nullable=False)
    calorias = db.Column(db.Integer,nullable=False)
    carbohidratos = db.Column(db.Integer,nullable=False)
    grasa = db.Column(db.Integer,nullable=False)
    proteinas = db.Column(db.Integer,nullable=False)
    categoria = db.Column(db.String(250),nullable=False)
    despensa = db.relationship('Despensa', backref='ingrediente', lazy=True)
    receta = db.relationship('Receta', backref='ingrediente', lazy=True) 

    def __repr__(self):
        return "<Ingrediente %r>" % self.nombre #no se cual va aqui

    def serialize(self):
        return {
            "id":self.id,
            "nombre_ingrediente": self.nombre_ingrediente,
            "calorias": self.calorias,
            "carbohidratos": self.carbohidratos,
            "grasa": self.grasa,
            "proteinas": self.proteinas,
            "categoria": self.categoria
        }

class Comentario_Valor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_receta = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable=False)
    comentario = db.Column(db.String(250),nullable=False)
    valoracion = db.Column(db.Integer,nullable=False) 

    def __repr__(self):
        return "<Comentario_Valor %r>" % self.comentario 

    def serialize(self):
        return {
            "id":self.id,
            "id_usuario": self.id_usuario,
            "id_receta": self.id_receta,
            "id_receta": self.id_receta,
            "comentario": self.comentario,
            "valoracion": self.valoracion
        }


class Despensa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), nullable=False)
    cantidad = db.Column(db.Integer,nullable=False) 

    def __repr__(self):
        return "<Despensa %r>" % self.cantidad

    def serialize(self):
        return {
            "id":self.id,
            "id_usuario": self.id_usuario,
            "id_ingrediente": self.id_ingrediente,
            "cantidad": self.cantidad
        }