#!/usr/bin/env python
# coding: utf-8

# # Connectar una base de dades  MySQL desde Python
# 
# ------
# 
# 
# *Prof. Antoni Oliver Gelabert - Administracio de Sistemes Gestors de Bases de Dades (CIFP Pau Casesnoves, Curs 2022/2023)*
# 
# Modificat de la versio anterior
# 
# Prof. Antoni Oliver Gelabert - Sistemes de Gestio Empresarial (CIFP Pau Casesnoves, Curs 2021/2022)
# 
# 
# -----------

# 1. instalam la llibreria del connector python-mysql emprant la terminal CLI (si no la tenim ja instalada)

# In[1]:


get_ipython().system('pip install mysql-connector-python')


# 2. Si estem en Linux, i encara no tenim la base de dades sakila importada a mysql, l'haurem de descarregar. Podem fer-ho amb wget a la terminal bash d'un sistema Linux (per exemple, Ubuntu). Si estem en Windows, podem pensar en descarregar el susbsistema Linux per Windows (WSL) i dur a terme la feina des d'alla. L'ordre WGET es troba tambe en el paquet Cygwin pensat per Windows. Tambe podem emprar una maquina virtual amb Ubuntu 20.04 LTS com a sistema convidat o be podem cercar una solucio amb docker. No obstant aixo, la base de dades es pot descarregar directament tambe desde la URL de la pagina especificada a continuacio de wget. Pensem que si empram Jupyter, el simbol d'exclamacio permet interactuar amb comandes interpretables per al SHELL. Aprofitem per tambe descomprimir la base de dades, una vegada s'ha descarregat 

# In[2]:


get_ipython().system('wget https://downloads.mysql.com/docs/sakila-db.zip')
get_ipython().system('unzip sakila-db.zip')


# 3. Si encara no ho hem fet, cal instalar el Servidor MySQL. Aixo a Ubuntu es pot fer directament amb l'ordre apt install

# In[3]:


get_ipython().system('apt install mysql-server 2> /dev/null')


# 4. Tot seguit importam ara ja la BBDD sakila a MySQL. Primer l'esquema, llavors les dades. Fem servir un inici de sessio sense password per agilitzar, pero en un cas real sempre s'ha de tenir un bon password

# In[6]:


get_ipython().system("mysql -u root -p '' sakila < sakila-db/sakila-schema.sql")
get_ipython().system("mysql -u root -p '' sakila < sakila-db/sakila-data.sql")


# 5. Ara, importem la llibreria del connector python-mysql que hem instalat al pas 1. Aprofitem per connectar amb la base de dades sakila, que ja ha estat importada al pas anterior.

# In[2]:


import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sakila"
)


# 6. Salvam la consulta a la taula actors dins una llista anomenada myresult i amb un loop obtenim per pantalla les dades de la taula.

# In[47]:


mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM actor")
myresult = mycursor.fetchall()

for x in myresult:
    print(x)


# 7. Mostram nomes les 10 primeres tuples-files-registres

# In[48]:


myresult[:10]


# 8. Mostrem nomes la tupla 1 (en realitat es la segona tupla, ja que python compta a partir del zero)

# In[49]:


myresult[1]


# 9. Mostrem l'atribut 2 (en realitat es el 3r perque python sempre compta el 0 com a 1r. Per tant, cognom de l'actor) de la tupla 5

# In[50]:


myresult[5][2]


# 10. Importam la llibreria Pandas com a pd i guardam el resultat obtingut en la consulta dins un Dataframe 

# In[51]:


import pandas as pd
df =[]
df = pd.DataFrame(myresult, columns=['actor_id','first_name','last_name','timestamp'])


# 11. Obtenim les 5 primeres linies del dataframe:

# In[55]:


df.head()


# ## Part II. Ara treballam amb la taula de pelicules, film.

# 12. Primer de tot importarem el nom de files de manera automatica i els guardarem dins labels a partir de la consulta "desc film" per obtenir el nom de les columnes

# In[57]:


labels=[]
mycursor = mydb.cursor()
mycursor.execute("desc film")
myresult2 = mycursor.fetchall()
for x in myresult2:
    print(x[0])
    labels.append(x[0])


# 13. Ara, definim el dataframe de pelicules aprofitant la informacio salvada en labels per ja assignar automaticament la fila de noms de columnes a les dades. Tambe salvam la consulta sobre la taula de pelicules (films)

# In[58]:


mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM film")
myresult = mycursor.fetchall()
df = pd.DataFrame(myresult, columns=labels)


# 14. Observem les 5 primeres tuples del resutlat del DATAFRAME amb l'instruccio head

# In[59]:


df.head()


# 15. Obtinguem una estadistica de la durada de les pelicules dins la base de dades sakila

# In[67]:


df['length'].describe()


# 16. Podem veure que els resultats indiquen una mitjana de 115 minuts de durada per unes 1000 pelicules. La desviacio tipica es de 40 minuts i la durada va entre els 46 minuts i els 185 minuts com a maxim.

# 17. Anem a veure mes detalls d'aquesta distribucio generant un histograma. Primer de tot importem matplotlib. Fer un histograma es tan simple com aixo:

# In[68]:


import matplotlib.pyplot as plt
plt.hist(df['length']);


# 18. No obstant aixo, si volem caracteritzar el grafic amb titols als eixos, amb una amplada de les barres especifica diferent a la predeterminada, i a mes volem guardar el resultat en una figura dins el mateix directori d'aquest notebook, haurem de ser mes especifics:

# In[19]:


plt.figure(figsize=[10,8])
plt.title('Histograma duracion peliculas - sakila (min)') 
plt.xlabel('Duracion (min)')
plt.ylabel('Numero de peliculas (min)')
plt.hist(df['length'],bins=20);
plt.savefig("histograma_duracion_peliculas_sakila.png",dpi=200)


# #### Mes opcions:
# https://www.datacamp.com/community/tutorials/histograms-matplotlib

# Tutorial W3 sobre el maneig de SQL a traves de Python
# 
# https://www.w3schools.com/python/python_mysql_getstarted.asp 
