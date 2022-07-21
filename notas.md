Instalaciones: (usar gitbash) y BORRAR EL ARCHIVO MIGRATION ANTES
pipenv shell
pipenv install flask-sqlalchemy
pipenv install flask
pipenv install flask-migrate flask-cors
pipenv install psycopg2-binary

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

post para Receta
{
"id_user": 1,
"id_ingredient": [1,2,3],
"ingredient_quantity": [20,2,3],
"name_recipe": "Postre 1",
"date_creation": "2-2-2022",
"step_by_step": "Agrega... despues... y... final..."
}
