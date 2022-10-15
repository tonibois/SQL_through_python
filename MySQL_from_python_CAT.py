# instalam la llibreria del connector python-mysql emprant la terminal CLI (si no la tenim ja instalada). Tambe necessitarem pandas i matplotlib.
# pip install mysql-connector-python
# pip install pandas
# pip install matplotlib

# Si estem en Linux, i encara no tenim la base de dades sakila importada a mysql, l'haurem de descarregar. Podem fer-ho amb wget a la terminal bash d'un sistema Linux (per exemple, Ubuntu)
# wget https://downloads.mysql.com/docs/sakila-db.zip

# Descomprimim la base de dades, ja que es descarrega en format comprimit ZIP 
# unzip sakila-db.zip

# Abans d'importarla, si no ho hem fet, hem de tenir Instalat el servidor Mysql a Ubuntu
# apt install mysql-server 2> /dev/null

# Tot seguit importam ara ja la BBDD sakila a MySQL. Primer l'esquema, llavors les dades. Fem servir un inici de sessio sense password per agilitzar, pero en un cas real sempre s'ha de tenir un bon password

# mysql -u root -p '' sakila < sakila-db/sakila-schema.sql
# mysql -u root -p '' sakila < sakila-db/sakila-data.sql

# Importem la llibreria del connector python-mysql
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sakila"
)

# Feim una consulta sobre tots els registres de la taula actor
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM actor")
myresult = mycursor.fetchall()

# Mostram tots els resultats de la consulta salvada dins myresult amb un bucle
for x in myresult:
    print(x)

# Mostram nomes les 10 primeres tuples (o files, registres, instancies,...)
myresult[:10]

# Mostrem nomes la tupla 1
myresult[1]

# Mostrem l'atribut 2 (en realitat es el 3r perque python sempre compta el 0 com a 1r. Per tant, cognom de l'actor) de la tupla 5
myresult[5][2]

# Mostrem tots els cognoms
for x in myresult:
    print(x[2])

# Importam la llibreria Pandas com a pd i guardam el resultat obtingut en la consulta dins un Dataframe per poder treure grafics
import pandas as pd
df = pd.DataFrame(myresult, columns=['actor_id','first_name','last_name','timestamp'])

# Obtenim les 5 primeres linies del dataframe:
df.head()

# A mysql llencam una sentencia: "desc film" per obtenir el nom de les columnes i l'aprofitam per emmagatzemar els noms de columnes en una llista anomenada "labels"
labels=[]
mycursor = mydb.cursor()
mycursor.execute("desc film")
myresult2 = mycursor.fetchall()
for x in myresult2:
    print(x[0])
    labels.append(x[0])

# Ara, definim el dataframe de pelicules aprofitant la informacio salvada en labels per ja assignar automaticament la fila de noms de columnes a les dades

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM film")
myresult = mycursor.fetchall()
df = pd.DataFrame(myresult, columns=labels)

# Importem la llibreria matplotlib per generar histogrames
import matplotlib.pyplot as plt

# dibuixam l'histograma de la durada de les pelicules emmagatzamades a sakila i el salvam en una figura en format PNG - CAT 
plt.figure(figsize=[10,8])
plt.title('Histograma duracion peliculas - sakila (min)') 
plt.xlabel('Duracion (min)')
plt.ylabel('Numero de peliculas (min)')
plt.hist(df['length'],bins=20);
plt.savefig("histograma_duracion_peliculas_sakila.png",dpi=200)
