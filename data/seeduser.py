import sys, os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal, User
from db.database import init_db

init_db()
db = SessionLocal()

# List of users to seed
user_data = [
    {
        "username": "aa",
        "password": "1234",
        "email": "aa.com",
        "aadhar_no": "123456789012",
        "phone_no": "1234567890",
        "full_name":"aabb",
        "address": "parappur,thrissur",
        "date_of_birth": "2005-08-03",
    },
    {
        "username": "bb",
        "password": "1234",
        "email": "bb.com",
        "aadhar_no": "112233445566",
        "phone_no": "1122334455",
        "full_name":"bbcc",
        "address": "chavakkad,guruvayoor",
        "date_of_birth": "2005-09-05",
    },
    # Add more users here
]

try:
    for data in user_data:
        # Convert DOB string to date object
        dob = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()
        data["date_of_birth"] = dob

        # Check if artisan already exists
        existing_user = db.query(User).filter_by(username=data["username"]).first()
        if existing_user is None:
            new_user = User(**data)
            db.add(new_user)
            print(f"Adding new user: {data['username']}")
        else:
            print(f"User {data['username']} already exists. Skipping.")

    db.commit()
    print("✅ Seeding complete.")
except Exception as e:
    db.rollback()
    print("❌ Error during seeding:", e)
finally:
    db.close()
