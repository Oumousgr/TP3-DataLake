from datasets import load_dataset
from pathlib import Path

def download_and_save():
    # Télécharge le dataset wikitext-2-raw-v1
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1")

    # Crée le dossier s'il n'existe pas
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Sauvegarde chaque split (train, test, validation)
    for split in ["train", "test", "validation"]:
        data = dataset[split]
        output_path = output_dir / f"{split}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            for line in data["text"]:
                f.write(line + "\n")

    print("✅ Téléchargement et sauvegarde terminés.")

if __name__ == "__main__":
    download_and_save()
