import sys, os
from datetime import datetime


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import CATEGORIES
from db.database import SessionLocal, Product
from db.database import init_db

init_db()
db = SessionLocal()

# List of products to seed
products_data = [
    {
        "artisan_id": 1,
        "product_name": "mural painting",
        "description": "traditional kerala mural painting",
        "category": CATEGORIES[0],
        "base_price": 500.0,
        "fallback_price": 450.0,
        "final_price": 500.0,
        "status": "ACTIVE",
        "threshold": 5,
        "duration_days": 10,
        "delivery_days":12,
    },
    {
        "artisan_id": 1,
        "product_name": "bottle art",
        "description": "show piece bottle art works",
        "category": CATEGORIES[1],
        "base_price": 300.0,
        "fallback_price": 200.0,
        "final_price": 300.0,
        "status": "ACTIVE",
        "threshold": 10,
        "duration_days": 3,
        "delivery_days":7,
    },
    # Add more products here
]

try:
    for data in products_data:
        # Check if product already exists for the artisan
        existing_product = db.query(Product).filter_by(
            artisan_id=data["artisan_id"],
            product_name=data["product_name"]
        ).first()

        if existing_product is None:
            new_product = Product(**data)
            db.add(new_product)
            print(f"Adding new product: {data['product_name']}")
        else:
            print(f"Product {data['product_name']} already exists for artisan {data['artisan_id']}. Skipping.")

    db.commit()
    print("✅ Product seeding complete.")
except Exception as e:
    db.rollback()
    print("❌ Error during seeding:", e)
finally:
    db.close()
