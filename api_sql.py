# On importe les différents modules nécessaires pour l'exercice

from sqlalchemy import create_engine, text
from faker import Faker
from datetime import datetime
from flask import Flask, jsonify
from jinja2 import escape
from jinja2.filters import escape
import random 

db_string = "postgresql://root:root@localhost:5432/postgres" #On utilise la BDD postgres de Pgadmin

engine = create_engine(db_string)

app = Flask(__name__)

@app.route("/user", methods=["GET"]) #On va utiliser la méthode GET pour récupérer les infos de chaque ligne de la BDD
def get_users():
    users = run_sql_with_result("SELECT * FROM users")
    data = []
    for row in users:
        user = {
            "id": row[0],
            "firstname": row[1],
            "lastname": row[2],
            "age": row[3],
            "email": row[4],
            "job": row[5],
        }
        data.append(user)
    return jsonify(data) on retourne sur le web les différents lignes sous format document JSON qu'on peut ensuite télécharger
    #[
    #     {
    #         "id":1,
    #         "name":"Jean",
    #         "job":"Software Engineer"
    #     },
    #     { 
    #         "id":2,
    #         "name":"Jen",
    #         "job":"Data Analyst"
    #     }

    # ]
    # return users

fake = Faker() # Faker va nous servir à créer de la data pour les différetes colonnes


# On va maintenant créer les 2 tables users et Application
create_user_table_sql = """ 
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    age INT,
    email VARCHAR(200),
    job VARCHAR(100)
);
"""
create_application_table_sql = """
CREATE TABLE IF NOT EXISTS Application (
    id SERIAL PRIMARY KEY,
    appname VARCHAR(100),
    username VARCHAR(100),
    lastconnection TIMESTAMP WITH TIME ZONE,
    user_id INTEGER REFERENCES users(id)
);
"""
def run_sql(query: str):     # la fonction pour créer les tables
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(text(query))
        trans.commit()


def run_sql_with_result(query: str): 
    with engine.connect() as connection:
        trans = connection.begin()
        result = connection.execute(text(query))
        trans.commit()
        return result 


def populate_tables(): # la fonction pour créer les lignes pour les tables
    apps = ["Facebook","Instagram","TikTok","Twitter"] # les différentes applications des utilisateurs
    for _ in range(100):
        firstname = fake.first_name() #on utilise faker pour les différentes colonnes de users
        lastname = fake.last_name()
        age = random.randrange(18, 50)
        email = fake.email()
        job = fake.job().replace("'","")
        print(firstname, lastname, age, email, job)
    
        insert_user_query = f"""
            INSERT INTO users (firstname, lastname, age, email, job)
            VALUES ('{firstname}','{lastname}','{age}','{email}','{job}')
            RETURNING id
        """
        user_id = run_sql_with_result(insert_user_query).scalar() 


        num_apps = random.randint(1,5)
        for i in range(num_apps):
            username = fake.user_name()
            lastconnection = datetime.now()
            app_name = random.choice(apps)

            sql_insert_app = f"""
                INSERT INTO applications (appname, username, lastconnection, user_id)
                VALUES ('{app_name}','{username}','{lastconnection}','{user_id}') #user_id est la foreign key de users
                RETURNING id
            """
        
            run_sql(insert_user_query)

if __name__ == '__main__': # Enfin on print les fonctions avec la définition du port qu'on va utiliser pour l'affichage de la page web avec les colonnes
    with app.app_context():
        run_sql(create_user_table_sql)
        run_sql(create_application_table_sql)
        #populate_tables()

    app.run(host="0.0.0.0", port=8081, debug=True)
    
