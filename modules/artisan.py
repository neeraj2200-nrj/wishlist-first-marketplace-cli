from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal,User,Wishlist,Product,Order,Artisan,Auction
from datetime import datetime,timezone,timedelta
from tabulate import tabulate
from sqlalchemy import or_
from constants import CATEGORIES


#------------------------ Register Artisan -----------------#

def register_artisan():
    db: Session = SessionLocal()
    print("\n--- Artisan Sign Up ---")
    artisan_name = input("Enter your name: ")
    password = input("Enter a password: ")
    email = input("Enter the email ID: ")
    aadhar_no = input("Enter the aadhar number: ")
    phone_no = input("Enter the phone number: ")
    address = input("Enter the address: ")
    date_of_birth = input("Enter the date of birth (YYYY-MM-DD): ")
    location = input("Enter your location: ")
    ward_number = input("Enter your ward number: ")

    if not email.endswith(".com"):
        print("⚠️ Enter a valid email ID ⚠️")
        db.close()
        return

    if not (phone_no.isdigit() and len(phone_no) == 10):
        print("⚠️ Enter a valid 10-digit phone number ⚠️")
        db.close()
        return

    if not (aadhar_no.isdigit() and len(aadhar_no) == 12):
        print("⚠️ Enter a valid 12-digit Aadhar number ⚠️")
        db.close()
        return

    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    except ValueError:
        print("⚠️ Date of Birth must be in YYYY-MM-DD format ⚠️")
        db.close()
        return
    
    existing = db.query(Artisan).filter(
        or_(
            Artisan.artisan_name == artisan_name,
            Artisan.email == email,
            Artisan.phone_no == phone_no,
            Artisan.aadhar_no == aadhar_no,
            Artisan.ward_number == ward_number
        )
    ).first()

    if existing :
        if existing.artisan_name == artisan_name:
            print("⚠️ Artisan name already exists ⚠️")
        elif existing.email == email:
            print("⚠️ Email already exists ⚠️")
        elif existing.phone_no == phone_no:
            print("⚠️ Phone number already exists ⚠️")
        elif existing.aadhar_no == aadhar_no:
            print("⚠️ Aadhar number already exists ⚠️")
        db.close()
        return
    
    try:
        new_artisan = Artisan(
            artisan_name=artisan_name,
            location=location,
            ward_number=ward_number,
            password=password,
            email=email,
            aadhar_no=aadhar_no,
            phone_no=phone_no,
            address=address,
            date_of_birth=dob
        )
        db.add(new_artisan)
        db.commit()
        print("✅ Artisan Sign Up Successfull ✅")
    except Exception as e:
        print("❌ Can't add the artisan. Error:", str(e))
        db.rollback()
    finally:
        db.close()
    

#------------------------ Login Artisan -----------------#
def login_artisan():
    db:Session=SessionLocal()
    print("🗝️  Artisan Sign In 🗝️")
    artisan_name = input("Enter the username: ")
    password = input("Enter the password: ")

    artisan = db.query(Artisan).filter_by(artisan_name=artisan_name,password=password).first()
    if artisan:
        print("🙏 Welcome ",artisan.artisan_name)
        artisan_menu(artisan)
    else:
        print("❌ Invalid Credentials ❌")

#------------------------ Artisan Menu -----------------#

def artisan_menu(artisan):
    db = SessionLocal()
    while True:
        print("\n--- Artisan Dashboard ---")
        print("[1]   View Profile")
        print("[2]   Edit Profile")
        print("[3]   List New Product")
        print("[4]   View My Listed Products")
        print("[5]   Auction hub")
        print("[6]   Orders")
        print("[7]   Relaunch Product Batch")
        print("[0]   Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            view_profile(artisan.id)
        elif choice == "2":
            db =SessionLocal()
            edit_profile(db=db,artisan_id=artisan.id)
        elif choice == "3":
            list_product(artisan.id)
        elif choice == "4":
            view_listing(artisan.id)
        elif choice == "5":
            auction_hub(artisan.id)
        elif choice == "6":
            view_artisan_orders(artisan.id)
        elif choice == "7":
            products = db.query(Product).filter(Product.artisan_id == artisan.id).all()
            if not products:
                print("⚠️ You don’t have any products yet.")
            else:
                table = []
                for p in products:
                    table.append([p.id,p.product_name,p.status,p.threshold,p.duration_days,p.listing_date.strftime("%Y-%m-%d")])

                print("\n📦 Your Products 📦")
                print(tabulate(table, headers=["ID", "Name", "Status", "Threshold", "Duration (days)", "Listed On"], tablefmt="fancy_grid"))
                try:
                    '''pid = int(input("Enter the Product ID to relaunch: "))
                    threshold = int(input("Enter new wishlist threshold: "))
                    duration = int(input("Enter duration (days): "))'''
                    relaunch_product(artisan.id)
                except ValueError:
                    print("⚠️ Invalid input. Please enter numeric values.")
        
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")


#------------------------ View Profile -----------------#
def view_profile(artisan_id):
    db=SessionLocal()
    try:
        artisan = db.query(Artisan).filter(Artisan.id==artisan_id).first()
        if artisan:
            data = [
                ["Artisan Name",artisan.artisan_name],
                ["Email ID",artisan.email],
                ["Password",artisan.password],
                ["Aadhar Number",artisan.aadhar_no],
                ["Phone Number",artisan.phone_no],
                ["Address",artisan.address],
                ["Date Of Birth",artisan.date_of_birth],
                ["Joined On",artisan.joined_at.strftime('%Y-%m-%d %H:%M:%S')],

            ]
            print("🪪  Your Profile 🪪")
            print(tabulate(data, headers=["Field","Value"],tablefmt="fancy_grid"))
        else:
            print("⛔ Sorry Artisan not found ⛔")
    finally:
        db.close()

#------------------------ Edit Profile -----------------#
def edit_profile(db: Session, artisan_id: int):
    print("✏️  Edit Profile (leave blank inorder to Skip a field)  ✏️")

    artisan = db.query(Artisan).filter(Artisan.id == artisan_id).first()
    if not artisan:
        print("❌  Artisan not found.")
        return
    new_artisan_name = input('Enter new artisan name: ').strip()
    new_email = input("Enter new Email ID: ").strip()
    new_password = input("Enter new password: ").strip()
    new_phone_no = input("Enter the new phone no: ").strip()
    new_ward_no = input("Enter the new full name: ").strip()
    new_address = input("Enter the new Address: ").strip()
    new_craft_type = input("Enter the new craft type: ").strip()

    if new_artisan_name:
        artisan.artisan_name = new_artisan_name
    if new_email:
        artisan.email = new_email
    if new_password:
        artisan.password = new_password
    if new_phone_no:
        artisan.phone_no = new_phone_no
    if new_ward_no:
        artisan.ward_number = new_ward_no
    if new_address:
        artisan.address = new_address
    
    try:
        db.commit()
        db.refresh(artisan)
        print("✅  Profile updated Successfully !")
    except IntegrityError:
        db.rollback()
        print("❌ Update failed due to unique constraint violation.")

#------------------------ List Product -----------------#
def list_product(artisan_id):
    db = SessionLocal()
    print("\n--- List New Product ---")

    product_name = input("Enter product name: ").strip()
    description = input("Enter product description: ").strip()

    # Category selection from predefined categories
    print("\nSelect product category:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")

    while True:
        try:
            choice = int(input("Enter the number corresponding to category: "))
            if 1 <= choice <= len(CATEGORIES):
                category = CATEGORIES[choice - 1]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(CATEGORIES)}")
        except ValueError:
            print("❌ Invalid input. Enter a number.")

    try:
        threshold = int(input("Enter wishlist threshold: "))
        duration_days = int(input("Enter duration (in days): "))
        delivery_days = int(input("Enter total delivery days (production + shipping): "))
        base_price = float(input("Enter base price: "))
        fallback_price = float(input("Enter fallback price: "))
    except ValueError:
        print("❌ Invalid numeric input. Product not added.")
        db.close()
        return

    listing_date = datetime.now(timezone.utc)
    final_price = base_price
    status = "ACTIVE"

    new_product = Product(
        artisan_id=artisan_id,
        product_name=product_name,
        description=description,
        category=category,
        threshold=threshold,
        duration_days=duration_days,
        delivery_days=delivery_days,
        listing_date=listing_date,
        base_price=base_price,
        fallback_price=fallback_price,
        final_price=final_price,
        status=status
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    product_data = [
        ["ID", new_product.id],
        ["Name", new_product.product_name],
        ["Category", new_product.category],
        ["Threshold", new_product.threshold],
        ["Duration", f"{new_product.duration_days} days"],
        ["Delivery Days", f"{new_product.delivery_days} days"],
        ["Base Price", new_product.base_price],
        ["Fallback Price", new_product.fallback_price],
        ["Final Price (initial)", new_product.final_price],
        ["Status", new_product.status],
        ["Listing Date", new_product.listing_date]
    ]

    print("\n✅ Product listed successfully!")
    print(tabulate(product_data, headers=["Field", "Value"], tablefmt="fancy_grid"))
    db.close()

#------------------------ View Product Listings -----------------#
def view_listing(artisan_id: int):
    db = SessionLocal()
    try:
        products = db.query(Product).filter(Product.artisan_id == artisan_id).all()
    
        if not products:
            print("\n⛔  No listings found for this artisan  ⛔\n")
            db.close()
            return
    
        table = []
        for product in products:
            table.append([
                product.id,
                product.product_name,
                product.category,
                product.threshold,
                product.duration_days,
                f"₹{product.base_price}",
                f"₹{product.fallback_price}",
                f"₹{product.final_price}",
                product.status,
                product.listing_date.strftime("%Y-%m-%d %H:%M")
                ])
    
        headers = [
            "ID", "Name", "Category", "Threshold", "Duration (days)", 
            "Base Price", "Fallback Price", "Final Price", "Status", "Listed On"
        ]
    
        print("\n📦 Artisan Product Listings 📦\n")
        print(tabulate(table, headers=headers, tablefmt="pretty", stralign="center"))
    finally:
        db.close()

#------------------------ View Orders for Artisan -----------------#
def view_artisan_orders(artisan_id):
    db = SessionLocal()
    print("\n📦 --- Orders for Your Products ---")
    
    orders = (
        db.query(Order)
        .join(Product, Order.product_id == Product.id)
        .filter(Product.artisan_id == artisan_id)
        .all()
    )
    
    if not orders:
        print("\n⛔  No orders found for your products  ⛔\n")
        return
    table = []
    for order in orders:
        buyer = db.query(User).filter(User.id == order.user_id).first()
        table.append([
            order.id,
            order.product.product_name,
            buyer.username if buyer else "Unknown",
            order.quantity,
            order.final_price,
            order.final_price * order.quantity,
            order.shipping_address,
            order.status,
            order.order_date.strftime("%Y-%m-%d")
        ])
    
    headers = ["Order ID", "Product", "Buyer", "Qty", " Unit Price (₹)","Total Price (₹)", "Ship To", "Status", "Date"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


#------------------------ Relaunch Product -----------------#
def get_input(prompt, old_value, cast_type=str):
    val = input(prompt)
    if not val.strip():  # blank input → keep old value
        return old_value
    try:
        return cast_type(val)  # try casting (int, float, etc.)
    except ValueError:
        print(f"⚠️ Invalid input for {prompt}, keeping old value.")
        return old_value


def relaunch_product(artisan_id):
    db = SessionLocal()
    products = db.query(Product).filter(Product.artisan_id == artisan_id).all()

    if not products:
        print("⚠️ You have no products to relaunch.")
        db.close()
        return

    print("\n📦 Your Products 📦")
    for idx, p in enumerate(products, 1):
        print(f"[{idx}] {p.product_name} (Status: {p.status})")

    choice = input("\nEnter product number to relaunch (0 to cancel): ")
    if not choice.isdigit() or int(choice) == 0:
        db.close()
        return

    choice = int(choice)
    if choice < 1 or choice > len(products):
        print("❌ Invalid choice.")
        db.close()
        return

    old_product = products[choice - 1]

    print(f"\n🔄 Relaunching product: {old_product.product_name}")
    print("Press Enter to keep old value.\n")

    # ✅ Collect new values safely
    new_name = get_input("Enter new product name: ", old_product.product_name, str)
    new_desc = get_input("Enter new description: ", old_product.description, str)
    new_base_price = get_input("Enter new base price: ", old_product.base_price, float)
    new_fallback_price = get_input("Enter new fallback price: ", old_product.fallback_price, float)
    new_final_price = get_input("Enter new final price: ", old_product.final_price, float)
    new_threshold = get_input("Enter new wishlist threshold: ", old_product.threshold, int)
    new_duration = get_input("Enter new duration (days): ", old_product.duration_days, int)
    new_delivery = get_input("Enter new delivery days: ", old_product.delivery_days, int)

    # ✅ Create new batch
    new_product = Product(
        artisan_id=artisan_id,
        product_name=new_name,
        description=new_desc,
        base_price=new_base_price,
        fallback_price=new_fallback_price,
        final_price=new_final_price,
        threshold=new_threshold,
        duration_days=new_duration,
        delivery_days=new_delivery,
        listing_date=datetime.now(),
        status="ACTIVE"
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    print(f"✅ Product '{new_product.product_name}' relaunched successfully as new batch (ID: {new_product.id})")

    db.close()

#------------------------ Auction Hub -----------------#
def auction_hub(artisan_id):
    update_auction_status()
    db = SessionLocal()
    while True:
        print("\n===== 🎨 Auction Hub =====")
        print("[1] List New Auction Item")
        print("[2] View My Auctions")
        print("[3] Close Auction Manually")
        print("[0] Back to Dashboard")

        choice = input("Enter choice: ")

        if choice == "1":
            list_new_auction(artisan_id)
        elif choice == "2":
            view_my_auctions(artisan_id)
        elif choice == "3":
            close_auction(artisan_id)
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice. Try again.")


#------------------------ List Auction -----------------#
def list_new_auction(artisan_id):
    db = SessionLocal()
    print("\n--- List New Auction Item ---")
    title = input("Enter auction item title: ")
    description = input("Enter description: ")
    try:
        starting_bid = float(input("Enter starting bid amount: "))
        duration_days = int(input("Enter auction duration (days): "))
    except ValueError:
        print("❌ Invalid number input.")
        return

    end_date = datetime.now(timezone.utc) + timedelta(days=duration_days)

    auction = Auction(
        artisan_id=artisan_id,
        title=title,
        description=description,
        starting_bid=starting_bid,
        current_highest_bid=starting_bid,
        end_date=end_date,
        status="ACTIVE"
    )
    db.add(auction)
    db.commit()
    db.refresh(auction)

    print(f"✅ Auction '{auction.title}' listed successfully until {auction.end_date}")

#------------------------ View My Auction -----------------#
def view_my_auctions(artisan_id):
    db = SessionLocal()
    auctions = db.query(Auction).filter_by(artisan_id=artisan_id).all()
    if not auctions:
        print("⚠️ No auctions found.")
        return

    table = []
    for auc in auctions:
        table.append([
            auc.id,
            auc.title,
            auc.status,
            auc.current_highest_bid,
            auc.end_date.strftime("%Y-%m-%d %H:%M")
        ])
    print("\n📢 Your Auctions 📢")
    print(tabulate(table, headers=["ID", "Title", "Status", "Highest Bid", "End Date"], tablefmt="fancy_grid"))

#------------------------ Close Auction -----------------#
def close_auction(artisan_id):
    db = SessionLocal()
    auction_id = input("Enter Auction ID to close: ")
    if not auction_id.isdigit():
        print("❌ Invalid ID.")
        return
    auction_id = int(auction_id)

    auction = db.query(Auction).filter_by(id=auction_id, artisan_id=artisan_id).first()
    if not auction:
        print("❌ Auction not found.")
        return
    if auction.status != "ACTIVE":
        print("⚠️ Auction is not active.")
        return

    auction.status = "ENDED"
    db.commit()

    if auction.current_highest_bidder_id:
        print(f"✅ Auction closed. Winner is User {auction.current_highest_bidder_id} with bid {auction.current_highest_bid}.")
    else:
        print("⚠️ Auction closed with no bids.")




def update_auction_status():
    db = SessionLocal()
    now = datetime.now(timezone.utc)

    auctions = db.query(Auction).filter(Auction.status == "ACTIVE").all()

    for auction in auctions:
        if now >= auction.end_date:
            if auction.current_highest_bid:
                auction.status = "SOLD"
            else:
                auction.status = "ENDED"
    db.commit()
    db.close()
