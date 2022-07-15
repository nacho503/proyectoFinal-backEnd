import mailbox
from flask_sqlalchemy import SQLAlchemy

#instacia de sqlalchemy
db = SQLAlchemy()

#####################################
class User(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(20),nullable=False)
    mail=db.Column(db.String(50),nullable=False)
    favorites=db.relationship('Favorite',backref="user", lazy=True)
    recipe=db.relationship('Recipe',backref="user", lazy=True)
    pantry=db.relationship('Pantry',backref="user", lazy=True)
    comment_value=db.relationship('Comment_Value',backref="user", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.name

    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "password": self.password,
            "mail":self.mail
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    id_recipe = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return "<Favorite %r>" % self.id #no se cual va aqui

    def serialize(self):
        return {
            "id":self.id,
            "id_user": self.id_User,
            "id_recipe": self.id_recipe
        }

class Recipe(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_ingredient = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    ingredient_quantity=db.Column(db.Integer,nullable=False)
    name_recipe = db.Column(db.String(250),nullable=False)
    date_creation = db.Column(db.DateTime(250),nullable=True)
    step_by_step = db.Column(db.String(250),nullable=False)
    image_recipe=db.Column(db.Text,nullable=True)
    comment_value = db.relationship('Comment_Value', backref='recipe', lazy=True)
    favorite = db.relationship('Favorite', backref='recipe', lazy=True) 

    def __repr__(self):
        return "<Recipe %r>" % self.name #no se cual va aqui

    def serialize(self):
        return {
            "id":self.id,
            "id_user": self.id_User,
            "id_ingredient": self.id_ingredient,
            "name_recipe": self.name_recipe,
            "date_creation": self.date_creation,
            "step_by_step": self.step_by_step
        }


class Ingredient(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN
    id = db.Column(db.Integer, primary_key=True)
    name_ingredient = db.Column(db.String(250),nullable=False)
    calories = db.Column(db.Integer,nullable=True)
    carbs = db.Column(db.Integer,nullable=True)
    grease = db.Column(db.Integer,nullable=True)
    proteins = db.Column(db.Integer,nullable=True)
    category = db.Column(db.String(250),nullable=True)
    pantry = db.relationship('Pantry', backref='ingredient', lazy=True)
    recipe = db.relationship('Recipe', backref='ingredient', lazy=True) 

    def __repr__(self):
        return "<Ingredient %r>" % self.name #no se cual va aqui

    def serialize(self):
        return {
            "id":self.id,
            "name_ingredient": self.name_ingredient,
            "calories": self.calories,
            "carbs": self.carbs,
            "grease": self.grease,
            "proteins": self.proteins,
            "category": self.category
        }

class Comment_Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_recipe = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    comment = db.Column(db.String(250),nullable=True)
    value = db.Column(db.Integer,nullable=True) 

    def __repr__(self):
        return "<Comment_Value %r>" % self.comment 

    def serialize(self):
        return {
            "id":self.id,
            "id_user": self.id_User,
            "id_recipe": self.id_recipe,
            "id_recipe": self.id_recipe,
            "comment": self.comment,
            "value": self.value
        }


class Pantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_ingredient = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Integer,nullable=False) 

    def __repr__(self):
        return "<Pantry %r>" % self.quantity

    def serialize(self):
        return {
            "id":self.id,
            "id_user": self.id_User,
            "id_ingredient": self.id_ingredient,
            "quantity": self.quantity
        }