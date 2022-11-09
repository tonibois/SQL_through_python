# SQL_db_through_python

Two examples of accessing to a database are provided. The first one shows how to access to **MySQL** database *sakila* and make data analysis from actor and film tables.
This example are further developed in the notebook "MySQL_from_python.ipynb".

The second example shows how to access to *dellstore* **PostgreSQL** database. In that case, it is shown how to analyze products and order tables. This work is performed on file: "PostgreSQL_from_python.ipynb"

Here detailed instructions on how to access to MySQL database sakila using python connector, that are also described in *MySQL_from_python.ipynb*:

Previous steps for initial requirements are described in the main code in catalan. Step by step translation to english is provided here.

1. install the python-mysql connector library using the CLI terminal (if we don't already have it installed)

```bash
pip install mysql-connector-python
```

2. If you are on Linux and we do not yet have the sakila database imported into mysql, you must download it. You can do this by wget command executed in a bash terminal of a Linux system (for instance, Ubuntu). If you use Windows, you can try the Linux Subsystem for Windows (WSL) and carry out the work from there. The WGET command is also in the Cygwin package designed for Windows. Also, you can alternatively use a virtual machine with Ubuntu (for instance 20.04 LTS) as a guest system. Another solution is using docker. However, the database can also be downloaded directly from the URL of the page specified next to wget command. Rembember that using Jupyter notebook, the exclamation mark allows us to interact with interpretable commands from the SHELL. After download decompress the ZIP file.
```bash
wget https://downloads.mysql.com/docs/sakila-db.zip 
unzip sakila-db.zip
```
3. If you haven't done it yet, you must install the MySQL Server. This in Ubuntu can be done directly with apt install command. Send errors to /dev/null:
```bash
apt install mysql-server 2> /dev/null
```
4. Next, we now import the sakila DB into MySQL. First the schema, finally, the data. We use a login without a password to speed up, but in a real case you should always have a good password.

```bash
mysql -u root -p '' -e "CREATE DATABASE IF NOT EXISTS sakila;"
mysql -u root -p '' sakila < sakila-db/sakila-schema.sql 
mysql -u root -p '' sakila < sakila-db/sakila-data.sql
```

5. Now, open python prompt and import the python-mysql plugin library that we installed in step 1. We take the opportunity to connect to the sakila database, which has already been imported in the previous step.

```python
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sakila"
)
```
6. Save the query for the actors table in a list called "myresult" and print the data using a loop.

```python
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM actor")
myresult = mycursor.fetchall()

for x in myresult:
    print(x)
```

7. Show only the first 10 tuples-rows-records
```python
myresult[:10]
```
8. Show tuple 1 (it's actually the second tuple, since python counts from zero)
```python
myresult[1]
```
9. Show attribute 2 (3): actor's last name of the 5th tuple 
```python
myresult[5][2]
```

10. Import the Pandas library as pd and save the result obtained in the query in a Dataframe by specification the field labels by hand:
```python
import pandas as pd
df = pd.DataFrame(myresult, columns=['actor_id','first_name','last_name','timestamp'])
```
11. Get the first 5 lines of the dataframe (df) using head function:
```python
df.head()
```
12. Import the names of the rows and save them in labels using the query "desc film"
```python
labels=[]
mycursor = mydb.cursor()
mycursor.execute("desc film")
myresult2 = mycursor.fetchall()
for x in myresult2:
    print(x[0])
    labels.append(x[0])
```

13. Now,  define the movie dataframe taking advantage of the information saved in labels to automatically assign the row of column names to the data. We also save the query on the table of films (films)

```python
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM film")
myresult = mycursor.fetchall()
df = pd.DataFrame(myresult, columns=labels)
```

14. Let's look at the first 5 tuples of the DATAFRAME result with the head function
```python
df.head()
```
15. Get statistics summary of the duration of the movies (length) in the sakila database using describe funcion.
```python
df['length'].describe()
```
16. We can see that the results indicate an average of 115 minutes of duration for about 1000 movies. The typical deviation is 40 minutes and the duration is between 46 minutes and 185 minutes as a maximum.

17. Let's see more details of this distribution by generating a histogram. First of all we import matplotlib. Making a histogram is as simple as this:
```python
import matplotlib.pyplot as plt
plt.hist(df['length'])
```
18. If titles on the axes, specific width of the bars, and saving the result in a figure is required, then we must specify.
```python
plt.figure(figsize=[10,8])
plt.title('Histograma duracion peliculas - sakila (min)') 
plt.xlabel('Duracion (min)')
plt.ylabel('Numero de peliculas (min)')
plt.hist(df['length'],bins=20);
plt.savefig("histograma_duracion_peliculas_sakila.png",dpi=200)
```
