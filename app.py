from crypt import methods
import os
from audioop import avg#Ir probando e importar el resto
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Ingredient, I_details_pantry, Ingredient_recipe, Recipe, User, Favorite, Pantry, Step, Comment_Value
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.utils import secure_filename #borrar si no funca
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import re


app = Flask(__name__)
db.init_app(app)
CORS(app) 
Migrate(app,db) 
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

UPLOAD_FOLDER = '/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresql@localhost:5432/finalProyect'


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|APP CONFIG|
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresql@localhost:5432/dev_j'
app.config['SECRET_KEY'] = 'super-secreta' #bccypt
app.config['JWT_SECRET_KEY'] = 'mas-secreta-aun' #jwt


# #Funcion que revisa si la extension es valida
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#post de image
@app.route('/upload_img_recipe', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify("Guardado")
    return jsonify('Archivo no permitido')  


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)


############################################ TABLA USERS #####################################

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|GET|
#get all users
@app.route('/users',methods=['GET']) #todos los users
def users_todos():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(),users))
    return jsonify(users),200 


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|POST|
#create a user
email_reg = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
password_reg = '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'

@app.route('/user', methods=['POST'])
def create_user():

    email = request.json.get('email')
    password = request.json.get('password')
    last_name = request.json.get('last_name')
    name = request.json.get("name")
    country = request.json.get("country")
    allergy = request.json.get("allergy")
    user_name = request.json.get("user_name") 

    if email != '' and re.search(email_reg, email):
        user = User.query.filter_by(email = email).first()
        if user is not None:
          
            return jsonify({
                'msg':'user already exists'
           }), 400

        else:
            if password != '' and re.search(password_reg, password):
                user = User()
                user.email = email
                user.name = name
                user.last_name = last_name
                user.country = country
                user.allergy = allergy
                user.user_name = user_name
               
                
                password_hash = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')
                user.password = password_hash


                db.session.add(user) 
                db.session.commit()

                access_token = create_access_token(identity = email)

                return  jsonify({
                    "msg":"succes user created",
                    'user': user.serialize(),
                    'access_token': access_token
                }),200
            else:
                return jsonify({
                    "msg":"wrong password format"
                }), 400 
    else:
        return jsonify({
              "msg":"wrong password format"
        }), 400   


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|POST|
#login user with autentication

@app.route('/login', methods=['POST'])
def login():     

    email = request.json.get('email')
    password = request.json.get('password')
    
    if password  == '' and email == '':
        return jsonify({
            "msg": 'email or password empty'
        }),400
    else: 
        user = User.query.filter_by( email = email ).first()
        if user is not  None:
            user_password = user.password
            check_password = bcrypt.check_password_hash(user_password, password)

            if check_password:
                access_token = create_access_token(identity = email)
                return jsonify({
                    'user': user.serialize(),
                    'access_token': access_token
                }), 200
            else:
                return jsonify ({
                    'msg': 'email or password is invalid'
                }), 400  

        else:
            return jsonify({
                "msg": "user not found, go to register"
            }), 400  

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|GET|
#get data of a user

@app.route('/me', methods=['GET'])
@jwt_required
def me():
    user = get_jwt_identity()
    return jsonify(user),200



############################################ TABLA FAVORITE #####################################


@app.route('/favorites',methods=['GET']) #todos los users
def favorites_todos():
    favorites=Favorite.query.all()
    favorites=list(map(lambda favorite: favorite.serialize(),favorites))
    return jsonify(favorites),200 

@app.route('/create_favorite',methods=['POST'])
def crea_favorite():
    favorite = Favorite()
    favorite.id_user = request.json.get("id_user")
    favorite.id_recipe = request.json.get("id_recipe")

    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()),200


################# TABLA IGREDIENTE AND PANTRY ##########################

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|GET|
@app.route('/ingredient',methods=['GET']) 
def ingredient_todos():
    ingredient=Ingredient.query.all()
    ingredient=list(map(lambda ingredient: ingredient.serialize(),ingredient))
    return jsonify(ingredient),200 


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|POST|
#create ingredients
@app.route('/create_ingredient' , methods=['POST'])
def create_ingredient():
    ingredient = Ingredient()
    new_ingredient = request.json.get('ingredient_name')
    ingredient.ingredient_name = new_ingredient

    db.session.add(ingredient)
    db.session.commit()
    return jsonify({
        "msg":"succes ingredient created",
        'ingredient': ingredient.serialize(),
    }),200 


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|POST|
@app.route('/create_details_ingredient_pantry', methods=['POST'])
def create_details_ingredient_pantry():
    details_pantry = I_details_pantry()
    details_pantry.i_details_portion = request.json.get("i_details_portion")
    details_pantry.i_details_measure = request.json.get("i_details_measure")
    
    #ingredient
    ingredient = Ingredient.query.filter_by( ingredient_name = request.json.get("ingredient_name") ).first()
    if ingredient is not None:
        details_pantry.ingredient_id = ingredient.id
    else:    
        ingredient = Ingredient()
        ingredient.ingredient_name = request.json.get('ingredient_name')

        db.session.add(ingredient)
        db.session.commit()
          
        details_pantry.ingredient_id = ingredient.id

    #pantry
    pantry = Pantry.query.filter_by( user_id = request.json.get("user_id") ).first()
    if pantry is not None:
            details_pantry.pantry_id = pantry.id
    else: 
        return jsonify(request.json.get('user_id'))



    db.session.add(details_pantry)
    db.session.commit()

    return jsonify(details_pantry.serialize()),200       

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|GET|  
# all pantrys  
@app.route('/get_pantry',methods=['GET']) 
def get_pantry():
    pantry=Pantry.query.all()
    pantry =list(map(lambda pantry: pantry.serialize(),pantry))
    return jsonify(pantry),200 

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|POST|
#create pantry
@app.route("/create_my_pantry", methods=['POST'])
@jwt_required()
def create_my_pantry():
    #pantry
    pantry = Pantry()

    #user
    user = User.query.filter_by( id = request.json.get("user_id") ).first()
    if user is None:
        return jsonify({
            "msg": 'error, user not exist'
        })

    pantry.user_id = request.json.get("user_id")


    db.session.add(pantry)
    db.session.commit()

    return jsonify(pantry.serialize()),200


############################## TABLA RECIPE ##################################

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|GET|
#all recipes   
@app.route('/recipes',methods=['GET'])
def recipes_todos():
    recipes = Recipe.query.all()
    recipes = list(map(lambda recipe: recipe.serialize(),recipes))
    return jsonify(recipes.serialize()),200 


# @app.route('/recipe_by_id/<int:id>',methods=['GET']) #usar para usuario activo
# def recipes_id(id):
#     recipes = Recipe.query.filter_by(id=id).all()
#     recipes = list(map(lambda recipe: recipe.serialize(),recipes))
#     return jsonify(recipes),200 

# ######## INTENTO DE QUERY 
# @app.route('/recipe_by_id_get_author/<int:id>',methods=['GET']) #usar para usuario activo
# def recipes_id_user_name(id):
#     recipe=Recipe.query.filter_by(id=id).first()
#     recipe_author=User.query.filter_by(id=recipe.id_user).first() 

#     return jsonify(recipe_author.serialize()),200 

# @app.route('/recipes_by_user/<int:id>',methods=['GET']) #usar para usuario activo
# def recipes_user_id(id):
#     recipes = Recipe.query.filter_by(id_user=id).all()
#     recipes = list(map(lambda recipe: recipe.serialize(),recipes))
#     return jsonify(recipes),200 


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|POST|
#recipe
@app.route("/create_recipe", methods=['POST'])
def create_recipe():
    create_recipe = Recipe()
    create_recipe.name_recipe = request.json.get('name_recipe')
    create_recipe.portion = request.json.get('portion')
    create_recipe.time = request.json.get('time')
    create_recipe.user_id = request.json.get("user_id")

    db.session.add(create_recipe)
    db.session.commit()

    return jsonify(create_recipe.serialize()),200 

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|POST|
#create step
@app.route('/create_step', methods=['POST'])
def create_step():
    create_step = Step()
    create_step.step = request.json.get('step')

    recipe = Recipe.query.filter_by( user_id = request.json.get("user_id") ).first()
    if recipe is not None:
            create_step.recipe_id = recipe.id
    else: 
        return jsonify(request.json.get('user_id'))

    db.session.add(create_step)
    db.session.commit()

    return jsonify(create_step.serialize()),200 

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|POST|
#ingredient recipe
@app.route('/create_details_ingredient_recipe', methods=['POST'])
def create_details_ingredient_recipe():
    details_recipe = Ingredient_recipe()
    details_recipe.i_details_portion = request.json.get("i_details_portion")
    details_recipe.i_details_measure = request.json.get("i_details_measure")
    
    #ingredient
    ingredient = Ingredient.query.filter_by( ingredient_name = request.json.get("ingredient_name") ).first()
    if ingredient is not None:
        details_recipe.ingredient_id = ingredient.id
    else:    
        ingredient = Ingredient()
        ingredient.ingredient_name = request.json.get('ingredient_name')

        db.session.add(ingredient)
        db.session.commit()
          
        details_recipe.ingredient_id = ingredient.id

    #recipe
    recipe = Recipe.query.filter_by( user_id = request.json.get("user_id") ).first()
    if recipe is not None:
            details_recipe.recipe_id = recipe.id
    else: 
        return jsonify(request.json.get('user_id'))



    db.session.add(details_recipe)
    db.session.commit()

    return jsonify(details_recipe.serialize()),200   











@app.route('/delete_recipe/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe=Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify('Recipe deleted'),200


##########TABLA COMMENT VALUE###############################################
@app.route('/get_comment_value_all', methods=['GET'])
def all_comments():
    comment_value=Comment_Value.query.all()
    comment_value=list(map(lambda comment_value_i:  comment_value_i.serialize(),  comment_value))
    return jsonify(comment_value),200


@app.route('/get_comment_value/<int:id>', methods=['GET'])####Filtra por id de receta //
def get_one_comment_value(id):

    comments=Comment_Value.query.filter_by(id_recipe=id).all()
    comments=list(map(lambda comments_i: comments_i.serialize(), comments))

    if len(comments) !=0:
        count=0
        total=0
        index=0
        while index<len(comments):
            total=comments[index]['value']+total
            count+=1
            index+=1
        avg=round(total/count)
        return jsonify(comments,avg),200
    return jsonify(comments),200

# @app.route('/get_comments_avg/<int:id>', methods=['GET'])####Filtra por id de receta /get_comments_avg/
# def get_one_comment_value(id):
#     comments=Comment_Value.query.filter_by(id_recipe=id).all()
#     comments=list(map(lambda comments_i: comments_i.serialize(), comments))
#     if len(comments) !=0:
#         count=0
#         total=0
#         index=0
#         while index<len(comments):
#             total=comments[index]['value']+total
#             count+=1
#             index+=1
#         avg=round(total/count)
#         return jsonify(avg),200
#     return jsonify('No avg to display'),200


@app.route('/comment_value', methods=['POST'])
def make_comment_value():
    comment_value=Comment_Value()
    comment_value.id_user=request.json.get("id_user")
    comment_value.id_recipe=request.json.get("id_recipe")
    comment_value.comment=request.json.get("comment")
    comment_value.value=request.json.get("value")
    
    db.session.add(comment_value)
    db.session.commit()

    return jsonify(comment_value.serialize()),200

#eliminar comment por comment id
@app.route('/delete_comment/<int:id>', methods=['DELETE']) 
def delete_comment(id):
    comment=Comment_Value.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify('Deleted'),200



    

# @app.route('/put_user/<int:id>',methods=['PUT'])
# def put_user(id):
#     user=User.query.get(id)
#     user.password = request.json.get("password")
#     user.password = request.json.get("name")
#     db.session.add(user)
#     db.session.commit()
#     return jsonify(user.serialize()),200 


# @app.route('/delete_user/<int:id>', methods=['DELETE'])
# def delete_user(id):
#     user=User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify('Borrado'),200


###### Lo mismo pero en favorite 

# @app.route('/favorites',methods=['GET']) #Get de favorites
# def all_favorites():
#     favorites=Favorite.query.all()
#     favorites=list(map(lambda user: user.serialize(),favorites))
#     return jsonify(favorites),200 






if __name__ == "__main__":
    app.run(host="localhost", port=8080)