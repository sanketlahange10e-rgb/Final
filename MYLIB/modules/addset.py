import csv
from pathlib import Path
def change(prno,name,latitude,longitude):
    
  
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    csv_path = data_dir / "stdcood3.csv"
    file_exists = csv_path.exists()
    with open(csv_path, mode="a", newline='', encoding='utf-8') as out_csvfile:
        writer = csv.DictWriter(out_csvfile, fieldnames=["prn_no", "name", "latitude", "longitude"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"prn_no": prno, "name": name, "latitude": latitude, "longitude": longitude})