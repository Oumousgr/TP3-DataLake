import boto3
import mysql.connector
import argparse
from pathlib import Path

def download_raw_file(bucket, output_path):
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )
    s3.download_file(bucket, "combined.txt", output_path)
    print(f"✅ Fichier téléchargé depuis S3 vers {output_path}")

def clean_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    cleaned = list(set(line.strip() for line in lines if line.strip()))
    return cleaned

def insert_into_mysql(lines, host, port, user, password, db_name):
    conn = mysql.connector.connect(
        host=host,
        port=port,  
        user=user,
        password=password,
        database=db_name
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS texts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text TEXT
        )
    """)

    for line in lines:
        cursor.execute("INSERT INTO texts (text) VALUES (%s)", (line,))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {len(lines)} lignes insérées dans la base MySQL.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket_raw", default="raw")
    parser.add_argument("--db_host", default="localhost")
    parser.add_argument("--db_port", type=int, default=3307)  # 👈 port 3307 ici
    parser.add_argument("--db_user", default="root")
    parser.add_argument("--db_password", default="root")
    parser.add_argument("--db_name", default="staging")
    args = parser.parse_args()

    file_path = "combined.txt"
    download_raw_file(args.bucket_raw, file_path)
    cleaned_lines = clean_data(file_path)
    insert_into_mysql(cleaned_lines, args.db_host, args.db_port, args.db_user, args.db_password, args.db_name)
