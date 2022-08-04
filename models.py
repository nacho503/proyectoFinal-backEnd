
from email.policy import default
from turtle import back
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY



#instacia de sqlalchemy
db = SQLAlchemy()


class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False, unique=True)
    country = db.Column(db.String(50),nullable=False)
    allergy = db.Column(db.String(50),nullable=False)
    user_name = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(200),nullable=False, unique=True)

    profile_id = db.relationship( 'Profile', backref='user', uselist=False )
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


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    name =  db.Column(db.String(50), primary_key=True)  
    last_name = db.Column(db.String(50), primary_key=True)  
    country = db.Column(db.String(50), primary_key=True)  
    allergy = db.Column(db.String(50), primary_key=True)  
    user_name = db.Column(db.String(50), primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Profile %r>" % self.user_name

    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "last_name": self.last_name,
            "country": self.country,
            "allergy": self.allergy,
            "user_name": self.user_name
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
            "id_user": self.id_user,
            "id_recipe": self.id_recipe
        }


class Recipe(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name_recipe = db.Column(db.String(250),nullable=False)
    date_creation = db.Column(db.DateTime(250),nullable=True)
    steps = db.Column(db.String(250),nullable=False)
    # image_recipe=db.Column(db.Text,nullable=True)

    comment_value = db.relationship('Comment_Value', backref='recipe', lazy=True)
    favorite = db.relationship('Favorite', backref='recipe', lazy=True) 
    ingredient = db.relationship('Ingredient', backref='recipe',lazy=True)

    def __repr__(self):
        return "<Recipe %r>" % self.name #no se cual va aqui

    def serialize(self):
        return {
            "id":self.id,
            "id_user": self.id_user,
            "name_recipe": self.name_recipe,
            "date_creation": self.date_creation,
            "steps":self.steps,
            "user_name":self.user.user_name
        }


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°INGREDINT
class Ingredient(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN
    id = db.Column(db.Integer, primary_key=True)
    id_recipe = db.Column(db.Integer,db.ForeignKey('recipe.id'), nullable=False)
    ingredient_name = db.Column(db.String(50),nullable=False, unique=True)
    ingredient_weight = db.Column(db.Integer, nullable=True)
    ingredient_volume = db.Column(db.Integer, nullable=True)
    ingredient_quantity=db.Column(db.Integer, nullable=True)
    ingredient_unit=db.Column(db.String(50), nullable=True)
   
    pantry = db.relationship('Pantry', backref='ingredient', lazy=True)
    # recipe = db.relationship('Recipe', backref='ingredient', lazy=True) 

    def __repr__(self):
        return "<Ingredient %r>" % self.ingredient_name 

    def serialize(self):
        return {
            "id":self.id,
            "id_recipe":self.id_recipe,
            "ingredient_name": self.ingredient_name,
            "ingredient_weight": self.ingredient_weight,
            "ingredient_volume": self.ingredient_volume,
            "ingredient_quantity":self.ingredient_quantity,
            "ingredient_unit":self.ingredient_unit,
            "recipe_name":self.recipe.name_recipe,
            "user_id":self.recipe.id_user
        }


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°COMMIT AND VALUE
class Comment_Value(db.Model):
    __tablename__='comment'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_recipe = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    comment = db.Column(db.String(250),nullable=True)
    value = db.Column(db.Integer,nullable=True,default=0) 


    def __repr__(self):
        return "<Comment_Value %r>" % self.comment 

    def serialize(self):
        return {
            "id":self.id,
            "id_user": self.id_user,
            "id_recipe": self.id_recipe,
            "comment": self.comment,
            "value": self.value,
            "user": self.user.user_name
        }


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°PANTRY
class Pantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_ingredient = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)

    def __repr__(self):
        return "<Pantry %r>" % self.id_

    def serialize(self):
        return {
            "id":self.id,
            "user_id": self.user_id,
            "id_ingredient": self.id_ingredient,
        }