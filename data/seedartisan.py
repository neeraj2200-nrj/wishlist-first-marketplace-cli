import sys, os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal, Artisan
from db.database import init_db

init_db()
db = SessionLocal()

# List of artisans to seed
artisans_data = [
    {
        "artisan_name": "Neeraj",
        "password": "1234",
        "email": "neeraj@gmail.com",
        "aadhar_no": "123456789012",
        "phone_no": "1234567890",
        "address": "parappur,thrissur",
        "date_of_birth": "2005-08-03",
        "location": "Thrissur",
        "ward_number": "6"
    },
    {
        "artisan_name": "Akhil",
        "password": "5678",
        "email": "akhil@gmail.com",
        "aadhar_no": "123456789013",
        "phone_no": "9876543210",
        "address": "kochi,kerala",
        "date_of_birth": "2004-05-12",
        "location": "Kochi",
        "ward_number": "3"
    },
    # Add more artisans here
]

try:
    for data in artisans_data:
        # Convert DOB string to date object
        dob = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()
        data["date_of_birth"] = dob

        # Check if artisan already exists
        existing_artisan = db.query(Artisan).filter_by(artisan_name=data["artisan_name"]).first()
        if existing_artisan is None:
            new_artisan = Artisan(**data)
            db.add(new_artisan)
            print(f"Adding new artisan: {data['artisan_name']}")
        else:
            print(f"Artisan {data['artisan_name']} already exists. Skipping.")

    db.commit()
    print("✅ Seeding complete.")
except Exception as e:
    db.rollback()
    print("❌ Error during seeding:", e)
finally:
    db.close()
