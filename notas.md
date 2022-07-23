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

Esta pendiente:
Hacer post de otras tablas y probrar relaciones en el postgre

Relaciones probadas en SQL:
Usuario-Receta-Ingrediente
SELECT nombre, fecha_creacion, paso_a_paso FROM usuario JOIN receta ON usuario.id = receta.id_usuario OK

'postgresql://postgres:tapi1740@localhost:5432/proyectoFinal'
