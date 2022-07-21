import os
from click import password_option
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Ingredient, Recipe, db, User, Favorite, Profile 
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

# UPLOAD_FOLDER = '/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°|APP CONFIG|
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresql@localhost:5432/dev_j'
app.config['SECRET_KEY'] = 'super-secreta' #bccypt
app.config['JWT_SECRET_KEY'] = 'mas-secreta-aun' #jwt


#Funcion que revisa si la extension es valida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

                return  jsonify({
                    "msg":"succes user created"
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
@jwt_required()
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

################# TABLA IGREDIENTE ##########################

@app.route('/ingredient',methods=['GET']) #todos los users
def ingredient_todos():
    ingredient=Ingredient.query.all()
    ingredient=list(map(lambda ingredient: ingredient.serialize(),ingredient))
    return jsonify(ingredient),200 


@app.route('/crete_ingredient',methods=['POST'])
@jwt_required()
def crea_ingrediente():
    ingredient = Ingredient()
    ingredient.ingredient_name = request.json.get("ingredient_name")
    ingredient.ingredient_portion = request.json.get("ingredient_portion")
    ingredient.ingredient_measure = request.json.get("ingredient_measure")

    db.session.add(ingredient)
    db.session.commit()

    return jsonify(ingredient.serialize()),200


################# TABLA RECIPE ##########################


@app.route('/recipes',methods=['GET']) #todos los users
def recipes_todos():
    recipes = Recipe.query.all()
    recipes = list(map(lambda recipe: recipe.serialize(),recipes))
    return jsonify(recipes),200 

@app.route('/create_recipe',methods=['POST'])
@jwt_required()
def crea_recipe():
    recipe = Recipe()
    recipe.id_user = request.json.get("id_user")
    recipe.id_ingredient = request.json.get("id_ingredient")
    #ingredient_quantity=request.json.get("ingredient_quantity")
    recipe.name_recipe = request.json.get("name_recipe")
    recipe.image_recipe=request.files['pic'] #borrar si no funca
    recipe.date_creation = request.json.get("date_creation")
    recipe.step_by_step = request.json.get("step_by_step")

    # filename=secure_filename(pic.filename) #borrar si no funca
    # mimetype=pic.mimetype #borrar si no funca
    # img = Img(img=pic.read(),mimetype=mimetype, name=filename)#borrar si no funca

    db.session.add(recipe)
    db.session.commit()

    return jsonify(recipe.serialize()),200



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