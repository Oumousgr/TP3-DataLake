import boto3
import argparse
from pathlib import Path

def combine_files(data_dir):
    combined_path = Path(data_dir) / "combined.txt"
    with open(combined_path, "w", encoding="utf-8") as outfile:
        for split in ["train.txt", "test.txt", "validation.txt"]:
            split_path = Path(data_dir) / split
            with open(split_path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read() + "\n")
    return combined_path

def upload_to_s3(file_path, bucket_name):
    # Connexion à LocalStack (S3)
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )
    
    # Envoi du fichier dans le bucket
    s3.upload_file(str(file_path), bucket_name, "combined.txt")
    print(f"✅ Fichier '{file_path.name}' uploadé dans s3://{bucket_name}/combined.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine et upload les fichiers vers le bucket S3 raw")
    parser.add_argument("--data_dir", default="data/raw", help="Dossier contenant les fichiers à combiner")
    parser.add_argument("--bucket", default="raw", help="Nom du bucket S3")
    args = parser.parse_args()

    combined = combine_files(args.data_dir)
    upload_to_s3(combined, args.bucket)
