Instalaciones: (usar gitbash) y BORRAR EL ARCHIVO MIGRATION ANTES
pipenv shell
pipenv install flask-sqlalchemy
pipenv install flask
pipenv install flask-migrate flask-cors
pipenv install psycopg2-binary

pip install Werkzeug==2.0.0
pip install jinja2==3.0.3
pip install pyjwt==v1.7.1

flask db init
flask db migrate
flask db upgrade

comandos para hacer andar la bbdd:
pipenv shell y seleccionar interprete
python app.py

'postgresql://postgres:tapi1740@localhost:5432/proyectoFinal'

users: id3  
{
"name": "Felipe",
"last_name": "Tapia",
"email":"asdasdasd@asdads.com",
"country": "chl",
"allergy":"no",
"user_name":"pipeT",
"password":"456abcA!@@"
}
loggedUser.email = "asdasdasd@asdads.com";
loggedUser.password = "456abcA!@@";

id2
loggedUser.email = "user2@mail.com";
loggedUser.password = "123abcA!";

id4
{
"name": "Andrea",
"last_name": "Gonzalez",
"email":"AG@asdads.com",
"country": "chl",
"allergy":"no",
"user_name":"andreaG",
"password":"789abcA!@@"
}

id5
{
"email":"FG@asdads.com",
"password":"789abcA!@@@"
}
