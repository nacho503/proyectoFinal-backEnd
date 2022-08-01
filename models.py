
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, true
from sqlalchemy import Table



#instacia de sqlalchemy
db = SQLAlchemy()


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°USER

class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False, unique=True)
    country = db.Column(db.String(50),nullable=False)
    allergy = db.Column(db.String(50))
    user_name = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(200),nullable=False, unique=True)

    favorites = db.relationship('Favorite',backref="user", lazy=True)
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


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°RECIPE

class Recipe(db.Model): #FALTA AGREGAR COLUMNA DE IMAGEN
    id = db.Column(db.Integer, primary_key=True)
    name_recipe = db.Column(db.String(250),nullable=False)
    portion = db.column(db.Integer, nullable=False)
    time = db.Column(db.String, nullable=False)

    #relation
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_value = db.relationship('Comment_Value', backref='recipe', lazy=True)
    favorite = db.relationship('Favorite', backref='recipe', lazy=True) 

    def __repr__(self):
        return "<Recipe %r>" % self.id

    def serialize(self):
        return {
            "id":self.id,
            "user_id": self.user_id,
            "ingredient_id": self.ingredient_id,
            "name_recipe": self.name_recipe,
        }


class Recipe_step(db.Model):
    id = db.Column(db.Integer, primary_kay=True)

    #relation
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return '<Step %r>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'step': self.step
        }    


class I_details_recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    i_details_portion = db.Column(db.Integer, nullable=False)
    i_details_measure = db.Column(db.String(50), nullable=False)  

    #relation
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))  

    def __repr__(self):
        return "<I_details_recipe %r>" % self.id

    def serialize(self):
        return {
            "id": self.id,
            "i_details_portionn": self.i_details_portion,
            "i_details_measure": self.i_details_measure,
            "ingredient_id": self.ingredient_id
        }  


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°INGREDINT

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(50),nullable=False, unique=True)
   

    def __repr__(self):
        return "<Ingredient %r>" % self.ingredient_name 

    def serialize(self):
        return {
            "id":self.id,
            "ingredient_name": self.ingredient_name,
        }


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°PANTRY

class Pantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return "<Pantry %r>" % self.user_id

    def serialize(self):
        return {
            "id":self.id,
            "user_id": self.user_id,
        }


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°I_DETAILS_PANTRY
class I_details_pantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    i_details_portion = db.Column(db.Integer, nullable=False)
    i_details_measure = db.Column(db.String(50), nullable=False)

    #foreinkey
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    pantry_id = db.Column(db.Integer, db.ForeignKey('pantry.id'))


    def __repr__(self):
        return "<I_details_pantry %r>" % self.id

    def serialize(self):
        return {
            "id": self.id,
            "i_details_portion": self.i_details_portion,
            "i_details_measure": self.i_details_measure,
            "ingredient_id": self.ingredient_id,
            "pantry_id": self.pantry_id,
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
