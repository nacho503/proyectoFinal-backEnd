import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Ingrediente, Receta, db, Usuario, Favorito #Ir probando e importar el resto
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.utils import secure_filename #borrar si no funca
import os

app = Flask(__name__)
db.init_app(app)
CORS(app) 
Migrate(app,db) 

# UPLOAD_FOLDER = '/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tapi1740@localhost:5432/proyectoFinal'


#Funcion que revisa si la eztension es valida
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#post de imagen
@app.route('/upload_img_receta', methods=['POST'])
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
################# TABLA USUARIOS ##########################

@app.route('/usuarios',methods=['GET']) #todos los usuarios
def usuarios_todos():
    usuarios=Usuario.query.all()
    usuarios=list(map(lambda usuario: usuario.serialize(),usuarios))
    return jsonify(usuarios),200 

@app.route('/crear_usuario',methods=['POST'])
def crea_usuario():
    usuario = Usuario()
    usuario.nombre = request.json.get("nombre")
    usuario.password = request.json.get("password")
    usuario.mail = request.json.get("mail")

    db.session.add(usuario)
    db.session.commit()

    return jsonify(usuario.serialize()),200

################# TABLA FAVORITO ##########################

@app.route('/favoritos',methods=['GET']) #todos los usuarios
def favoritos_todos():
    favoritos=Favorito.query.all()
    favoritos=list(map(lambda favorito: favorito.serialize(),favoritos))
    return jsonify(favoritos),200 

@app.route('/crear_favorito',methods=['POST'])
def crea_favorito():
    favorito = Favorito()
    favorito.id_usuario = request.json.get("id_usuario")
    favorito.id_receta = request.json.get("id_receta")

    db.session.add(favorito)
    db.session.commit()

    return jsonify(favorito.serialize()),200

################# TABLA IGREDIENTE ##########################

@app.route('/ingredientes',methods=['GET']) #todos los usuarios
def ingredientes_todos():
    ingredientes=Ingrediente.query.all()
    ingredientes=list(map(lambda ingrediente: ingrediente.serialize(),ingredientes))
    return jsonify(ingredientes),200 

@app.route('/crear_ingrediente',methods=['POST'])
def crea_ingrediente():
    ingrediente = Ingrediente()
    ingrediente.nombre_ingrediente = request.json.get("nombre_ingrediente")
    ingrediente.calorias = request.json.get("calorias")
    ingrediente.carbohidratos = request.json.get("carbohidratos")
    ingrediente.grasa = request.json.get("grasa")
    ingrediente.proteinas = request.json.get("proteinas")
    ingrediente.categoria = request.json.get("categoria")

    db.session.add(ingrediente)
    db.session.commit()

    return jsonify(ingrediente.serialize()),200


################# TABLA RECETA ##########################


@app.route('/recetas',methods=['GET']) #todos los usuarios
def recetas_todos():
    recetas=Receta.query.all()
    recetas=list(map(lambda receta: receta.serialize(),recetas))
    return jsonify(recetas),200 

@app.route('/crear_receta',methods=['POST'])
def crea_receta():
    receta = Receta()
    receta.id_usuario = request.json.get("id_usuario")
    receta.id_ingrediente = request.json.get("id_ingrediente")
    receta.nombre_receta = request.json.get("nombre_receta")
    receta.imagen_receta=request.files['pic'] #borrar si no funca
    receta.fecha_creacion = request.json.get("fecha_creacion")
    receta.paso_a_paso = request.json.get("paso_a_paso")

    filename=secure_filename(pic.filename) #borrar si no funca
    mimetype=pic.mimetype #borrar si no funca
    img = Img(img=pic.read(),mimetype=mimetype, name=filename)#borrar si no funca

    db.session.add(receta)
    db.session.commit()

    return jsonify(receta.serialize()),200



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