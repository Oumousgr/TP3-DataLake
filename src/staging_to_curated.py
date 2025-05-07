import pymysql
import pymongo
from transformers import AutoTokenizer
from datetime import datetime

mysql_conn = pymysql.connect(
    host="localhost",
    port=3307,  
    user="root",
    password="root",
    database="staging",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = mysql_conn.cursor()
cursor.execute("SELECT * FROM texts")
rows = cursor.fetchall()

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["curated"]
mongo_collection = mongo_db["wikitext"]
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

for row in rows:
    tokens = tokenizer(row["text"], truncation=True, padding=True, max_length=128)["input_ids"]
    document = {
        "id": str(row["id"]),
        "text": row["text"],
        "tokens": tokens,
        "metadata": {
            "source": "mysql",
            "processed_at": datetime.utcnow().isoformat()
        }
    }
    mongo_collection.insert_one(document)

print(f"✅ {len(rows)} documents insérés dans la collection MongoDB ‘{mongo_collection.name}’.")
cursor.close()
mysql_conn.close()
