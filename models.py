from enum import unique
import mailbox
from flask_sqlalchemy import SQLAlchemy

#instacia de sqlalchemy
db = SQLAlchemy()


class User(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False, unique=True)
    country = db.Column(db.String(50),nullable=False)
    allergy = db.Column(db.String(50),nullable=False)
    user_name = db.Column(db.String(50),nullable=False, unique=True)
    password = db.Column(db.String(50),nullable=False)

    favorites = db.relationship('Favorite',backref="user", lazy=True)
    recipe = db.relationship('Recipe',backref="user", lazy=True)
    pantry = db.relationship('Pantry',backref="user", lazy=True)
    comment_value=db.relationship('Comment_Value',backref="user", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.email

    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "country": self.country,
            "allergy": self.allergy,
            "user_name": self.user_name,
            "password": self.password
        }


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°FAVORITE
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


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°INGREDINT
class Ingredient(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(50),nullable=False, unique=True)
    ingredient_portion = db.Column(db.String(20), nullable=False)
    # calorias = db.Column(db.Integer,nullable=False)
    # carbohidratos = db.Column(db.Integer,nullable=False)
    # grasa = db.Column(db.Integer,nullable=False)
    # proteinas = db.Column(db.Integer,nullable=False)
    # categoria = db.Column(db.String(250),nullable=False)
    pantry = db.relationship('Pantry', backref='ingredient', lazy=True)
    recipe = db.relationship('Recipe', backref='ingredient', lazy=True) 

    def __repr__(self):
        return "<Ingredient %r>" % self.ingredient_name 

    def serialize(self):
        return {
            "id":self.id,
            "ingredient_name": self.ingredient_name,
            "ingredient_portion": self.ingredient_portion,
            # "calories": self.calories,
            # "carbs": self.carbs,
            # "grease": self.grease,
            # "proteins": self.proteins,
            # "category": self.category
        }


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°COMMIT AND VALUE
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


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°PANTRY
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