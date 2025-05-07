import sqlite3

# Connexion (crée le fichier test.db s'il n'existe pas)
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Création d'une table
cursor.execute('CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, value TEXT)')

# Insertion de données
cursor.execute('INSERT INTO test_table (value) VALUES ("Hello, SQLite!")')
conn.commit()

# Lecture de la table
cursor.execute('SELECT * FROM test_table')
rows = cursor.fetchall()
print(rows)

# Fermeture
conn.close()
