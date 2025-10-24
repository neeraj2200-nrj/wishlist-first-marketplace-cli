from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal,User,Wishlist,Product,Order,Payment,Auction,Bid
from datetime import datetime,timezone,timedelta
from tabulate import tabulate
from sqlalchemy import or_,func
from . artisan import update_auction_status

#------------------------ Register User -----------------#
def register_user():
    db: Session=SessionLocal()
    print("📝---- User Sign Up ----📝")
    username = input("Enter the username: ")
    email = input("Enter the email ID: ")
    password = input("Enter the password: ")
    phone_no = input("Enter the phone number: ")
    aadhar_no = input("Enter the aadhar number: ")
    full_name = input("Enter the full name: ")
    address = input("Enter the address: ")
    dob = input("Enter the date of birth (YYYY-MM-DD): ")

    if not email.endswith(".com"):
        print("⚠️  Enter Valied Email ID ⚠️")
        return
    
    if not (phone_no.isdigit() and len(phone_no)==10):
        print("⚠️  Enter Valied Phone Number ⚠️")
        return
    
    if not (aadhar_no.isdigit() and len(aadhar_no)==12):
        print("⚠️  Enter Valied Aadhar Number ⚠️")
        return
    
    try:
        dob = datetime.strptime(dob, "%Y-%m-%d").date()
    except ValueError:
        print("⚠️  Date of Birth must be in YYYY-MM-DD format ⚠️")
        return
    existing_user = db.query(User).filter(
        or_(
            User.username == username,
            User.email == email,
            User.phone_no == phone_no,
            User.aadhar_no == aadhar_no
        )
    ).first()

    if existing_user:
        if existing_user.username == username:
            print("⚠️  Username already exists! ⚠️")
        elif existing_user.email == email:
            print("⚠️  Email already exists! ⚠️")
        elif existing_user.phone_no == phone_no:
            print("⚠️  Phone number already exists! ⚠️")
        elif existing_user.aadhar_no == aadhar_no:
            print("⚠️  Aadhar number already exists! ⚠️")
        db.close()
        return

    try:
        new_user=User(username=username,email=email,password=password,phone_no=phone_no,aadhar_no=aadhar_no,full_name=full_name,address=address,date_of_birth=dob)
        db.add(new_user)
        db.commit()
        print("✅ User Signup Successfull ✅")
    except Exception as e:
        print("❌  Can't add the user. Error:",str(e))
    finally:
        db.close()

    

#------------------------ Login User -----------------#
def login_user():
    db:Session=SessionLocal()
    print("🗝️  User Sign In 🗝️")
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    user = db.query(User).filter_by(username=username,password=password).first()
    if user:
        print("\n🙏 Welcome ",user.username)
        user_menu(user)
    else:
        print("❌ Invalid Credentials ❌")

#------------------------ User Dashboard -----------------#
def user_menu(user):
    while True:
        print("\n--- User Dashboard ---")
        print("[1]  View Profile")
        print("[2]  Buy Products")
        print("[3]  Order Management ")
        print("[4]  Live Auctions")
        print("[5]  Edit Profile")
        print("[0]  Logout")
        choice = input("Choose an option: ")

        
        if choice == "1":
            view_profle(user.id)
        elif choice == "2":
            products_menu(user)
        elif choice == "3":
            db = SessionLocal()
            order_management(db,user)
        elif choice == "4":
            live_auctions(user.id)  
        elif choice == "5":
            db = SessionLocal()
            edit_profile(db=db,user_id=user.id)
        elif choice == "0":
            print("Logged out.")
            break
        else:
            print("❌ Invalid option.")

#------------------------ Products Menu -----------------#
def products_menu(user):
    while True:
        print("\n🛒 ---- Products Menu ---- 🛒")
        print("[1]  Browse Products")
        print("[2]  Add to Wishlist")
        print("[3]  View Wishlist")
        print("[4]  Track Wishlisted Items")
        print("[5]  Delete Wishlisted Items")
        print("[0]  Back to User Menu")

        ch=input("Enter the choice: ")
        if ch=="1":
            browse_product()
        elif ch=="2":
            add_to_wishlist(user)
        elif ch=="3":
            view_wishlist(user)
        elif ch=="4":
            track_wishlist_status(user.id)
        elif ch=="5":
            delete_wishlist_item(user.id)
        elif ch=="0":
            break
        else:
            print("❌ Invalid choice")

#------------------------ Browse Product -----------------#
def browse_product():
    db: Session=SessionLocal()
    products = db.query(Product).filter(Product.status == "ACTIVE").all()
    if not products:
        print("⛔  No Products Available ⛔")
    else:
        print("🛍️ Available Products: ")
        data = [[p.id,p.product_name,p.description]for p in products]
        print(tabulate(data,headers=["ID","Name","Description"],tablefmt="fancy_grid"))

#------------------------ Adding to Wishlist -----------------#
def add_to_wishlist(user):
    db: Session = SessionLocal()
    product_id = int(input("Enter the Product ID to add to wishlist: "))
    quantity = int(input("Enter the quantity: "))
    product = db.query(Product).filter_by(id=product_id).first()
    
    if not product:
        print("⚠️  No Such Product Linked With That ID ⚠️")
        db.close()
        return
    
    existing = db.query(Wishlist).filter_by(user_id=user.id, product_id=product_id).first()
    if existing:
        print("✅ Already in Wishlist")
        db.close()
        return
    
    print(f"\n⏳ If production starts, the product '{product.product_name}' "
          f"will be delivered within {product.delivery_days} days.")

    confirm = input("Do you still want to add this product to your wishlist? (y/n): ").lower()
    if confirm != "y":
        print("❌ Wishlist cancelled.")
        db.close()
        return

    wishlist_item = Wishlist(
        user_id=user.id,
        product_id=product_id,
        quantity=quantity,
        timestamp=datetime.now()
    )
    db.add(wishlist_item)
    db.commit()
    print("✅ Added to Wishlist")

    db.close()
            

#------------------------ Viewing Wishlist -----------------#
def view_wishlist(user):
    db: Session = SessionLocal()

    process_wishlists_to_orders()

    items = (
        db.query(Wishlist)
        .join(Product, Product.id == Wishlist.product_id)
        .filter(Wishlist.user_id == user.id, Product.status == "ACTIVE")
        .all()
    )

    if not items:
        print("⛔ You Have No Active Wishlisted Items ⛔")
    else:
        print("📋 Your Wishlist 📋")
        data = []
        for i in items:
            product = db.query(Product).filter_by(id=i.product_id).first()
            if product:
                data.append([
                    product.product_name,
                    i.quantity,
                    i.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                ])

        print(tabulate(data, headers=["Name", "Quantity", "Added On"], tablefmt="fancy_grid"))

    db.close()

#------------------------ View Profile -----------------#
def view_profle(user_id):
    db=SessionLocal()
    try:
        user=db.query(User).filter(User.id==user_id).first()
        if user:
            data = [
                ["Username",user.username],
                ["Email ID",user.email],
                ["Password",user.password],
                ["Aadhar Number",user.aadhar_no],
                ["Phone Number",user.phone_no],
                ["Full Name",user.full_name],
                ["Address",user.address],
                ["Date Of Birth",user.date_of_birth],
                ["Joined On",user.joined_at.strftime('%Y-%m-%d %H:%M:%S')],

            ]
            print("🪪  Your Profile 🪪")
            print(tabulate(data, headers=["Field","Value"],tablefmt="fancy_grid"))
        else:
            print("⛔ Sorry User not found ⛔")
    finally:
        db.close()

#------------------------ Delete Wishlist -----------------#
def delete_wishlist_item(user_id):
    db: Session=SessionLocal()
    wishlist_items = db.query(Wishlist).filter_by(user_id=user_id).all()
    if not wishlist_items:
        print("⛔  Your Wishlist is Empty. Nothing to Delete  ⛔")
        db.close()
        return
    table_data = []
    for x in wishlist_items:
        product = db.query(Product).filter_by(id=x.product_id).first()
        table_data.append([
            product.id,
            product.product_name,
            x.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])

    print("\n📋 Your Wishlist 📋\n")
    print(tabulate(
        table_data,
        headers=["Product ID", "Product Name", "Added On"],
        tablefmt="fancy_grid"
    ))
    try:
        pid=int(input("Enter the Product ID to Remove From Wishlist: "))
    except ValueError:
        print("❌  Invalid Input.Enter a Valied Number  ❌")
        db.close()
        return
    
    wishlist_entry = db.query(Wishlist).filter_by(user_id=user_id,product_id=pid).first()

    if wishlist_entry:
        product = db.query(Product).filter_by(id=wishlist_entry.product_id).first()
        listing_date = product.listing_date
        if listing_date.tzinfo is None:
            listing_date = listing_date.replace(tzinfo=timezone.utc)

        deadline = listing_date + timedelta(days=product.duration_days)
        total_demand = db.query(func.sum(Wishlist.quantity)) \
                         .filter_by(product_id=product.id).scalar() or 0

        if total_demand >= product.threshold or datetime.now(timezone.utc) > deadline:
            print("⛔ This wishlist is frozen (production started or expired). You cannot delete it.")
            db.close()
            return
        db.delete(wishlist_entry)
        db.commit()
        print("✅ product removed from your Wishlist")
    else:
        print("⛔  No such product in your Wishlist  ⛔")

    db.close()


#------------------------ Edit Profile -----------------#
def edit_profile(db: Session, user_id: int):
    print("✏️  Edit Profile (leave blank inorder to Skip a field)  ✏️")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        print("❌  User not found.")
        return
    new_username = input('Enter new username: ').strip()
    new_email = input("Enter new Email ID: ").strip()
    new_password = input("Enter new password: ").strip()
    new_phone_no = input("Enter the new phone no: ").strip()
    new_full_name = input("Enter the new full name: ").strip()
    new_address = input("Enter the new Address: ").strip()

    if new_username:
        user.username = new_username
    if new_email:
        user.email = new_email
    if new_password:
        user.password = new_password
    if new_phone_no:
        user.phone_no = new_phone_no
    if new_full_name:
        user.full_name = new_full_name
    if new_address:
        user.address = new_address
    
    try:
        db.commit()
        db.refresh(user)
        print("✅  Profile updated Successfully !")
    except IntegrityError:
        db.rollback()
        print("❌ Update failed due to unique constraint violation.")

#------------------------ Order Management -----------------#
def order_management(db: Session, user: User):
    while True:
        print("\n🛒 Order Management Menu")
        print("[1]  View My Orders")
        print("[2]  Pay Pending Order")
        print("[3]  View Order History")
        print("[0]  Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_orders(user.id)
        elif choice == "2":
            pending_payment(db, user)
        elif choice == "3":
            order_history(db, user)
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice. Try again.")

#------------------------ View Order -----------------#
def view_orders(user_id):
    process_wishlists_to_orders()
    db = SessionLocal()
    orders = (
        db.query(Order)
        .filter_by(user_id=user_id)
        .order_by(Order.order_date.desc())
        .all()
    )

    if not orders:
        print("\n📭 You have no confirmed orders yet.\n")
        db.close()
        return

    table = []
    for o in orders:
        product = db.query(Product).filter_by(id=o.product_id).first()
        if not product:
            product_name = "❌ Deleted Product"
        else:
            product_name = product.product_name

        table.append([
            o.id,
            product_name,
            o.quantity,
            f"₹{o.final_price:.2f}",
            f"₹{o.quantity * o.final_price:.2f}",
            o.status,
            o.order_date.strftime('%Y-%m-%d %H:%M:%S')
        ])

    print("\n🛒 Your Orders 🛒\n")
    print(tabulate(
        table,
        headers=["Order ID", "Product", "Quantity", "Unit Price", "Total Price", "Status", "Order Date"],
        tablefmt="fancy_grid"
    ))
    db.close()

#------------------------ Pay Order -----------------#

def pending_payment(db: Session, user: User):
    orders = db.query(Order).filter(
        Order.user_id == user.id,
        Order.status == "Pending"
    ).all()

    if not orders:
        print("\n✅ No pending payments. All orders are paid.\n")
        return
    
    data = [[
        o.id,
        o.product.product_name,
        o.quantity,
        f"₹{o.final_price}",
        f"₹{o.quantity * o.final_price}",
        o.status
    ] for o in orders]

    print(tabulate(
        data,
        headers=["Order ID", "Product", "Qty", "Unit Price", "Total Price", "Status"],
        tablefmt="fancy_grid"
    ))

    try:
        order_id = int(input("\nEnter Order ID to pay: ").strip())
    except ValueError:
        print("❌ Invalid input.")
        return
    
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user.id
    ).first()

    if not order or order.status != "Pending":
        print("❌ Invalid Order ID or already paid.")
        return
    
    if not order.shipping_address or order.shipping_address.strip() == "":
        new_address = input("📦 No shipping address found. Please enter your shipping address: ").strip()
        if not new_address:
            print("❌ Shipping address cannot be empty.")
            return
        order.shipping_address = new_address
    else:
        print(f"\n📍 Current shipping address: {order.shipping_address}")
        choice = input("Do you want to use this address? (y/n): ").strip().lower()
        if choice == "n":
            new_address = input("Enter new shipping address: ").strip()
            if new_address:
                order.shipping_address = new_address
            else:
                print("❌ Shipping address cannot be empty.")
                return
    
    total_amount = order.quantity * order.final_price
    print(f"\n💰 You have to pay: ₹{total_amount} for {order.quantity} x {order.product.product_name}")

    upi_id = input("Enter your UPI ID: ").strip()
    if not upi_id:
        print("❌ UPI ID cannot be empty.")
        return

    order.status = "Successfull" 

    payment = Payment(
        user_id=user.id,
        order_id=order.id,
        amount=total_amount,
        upi_id=upi_id,
        status="Successfull",
        paid_at=datetime.now(timezone.utc)
    )
    db.add(payment)
    db.commit()

    print(f"\n✅ Payment Successful via UPI ({upi_id})! Order {order.id} marked as Paid.\n")

#------------------------ View Order History -----------------#
def order_history(db: Session,user:User):
    orders = db.query(Order).filter(Order.user_id == user.id,Order.status == "Paid").all()

    if not orders:
        print("⛔ You have no order history yet.")
        return
    data = [
        [o.id, o.product.product_name, f"₹{o.final_price}", o.status, o.order_date.strftime("%Y-%m-%d")]
        for o in orders
    ]

    print("\n📦 Your Order History 📦")
    print(tabulate(data, headers=["Order ID", "Product", "Price", "Status", "Date"], tablefmt="fancy_grid"))


#------------------------ Track Wishlist Status -----------------#

def track_wishlist_status(user_id):
    db = SessionLocal()
    wishlist_items = db.query(Wishlist).filter_by(user_id=user_id).all()
    
    if not wishlist_items:
        print("\n⛔ You have no items in your wishlist.\n")
        db.close()
        return

    table = []
    for x in wishlist_items:
        product = db.query(Product).filter_by(id=x.product_id).first()
        if not product:
            continue

        total_demand = db.query(func.sum(Wishlist.quantity)).filter_by(product_id=product.id).scalar() or 0

        if product.status == "ACTIVE":
            status = f"⌛ Waiting (Demand {total_demand}/{product.threshold})"
        elif product.status == "COMPLETED":
            status = "✅ Production Started"
        elif product.status == "INACTIVE":
            status = "❌ Expired / Not Produced"
        elif product.status == "PRODUCTION_STARTED": 
            status = "📦 Converted to Order"
        else:
            status = product.status  # fallback, in case of new enum values

        table.append([product.id, product.product_name, x.quantity, status])

    print("\n📌 Wishlist Status 📌\n")
    print(tabulate(table, headers=["Product ID", "Product Name", "Quantity", "Status"], tablefmt="fancy_grid"))
    db.close()

#------------------------ Process Wishlist To Orders -----------------#
def process_wishlists_to_orders():
    db = SessionLocal()
    now = datetime.now(timezone.utc)
    products = db.query(Product).filter(Product.status != "PRODUCTION_STARTED").all()

    for product in products:
        listing_date = product.listing_date
        if listing_date.tzinfo is None:
            listing_date = listing_date.replace(tzinfo=timezone.utc)

        deadline = listing_date + timedelta(days=product.duration_days)

        total_demand = db.query(func.sum(Wishlist.quantity)) \
                         .filter_by(product_id=product.id).scalar() or 0


        if total_demand >= product.threshold and now <= deadline:
            product.status = "PRODUCTION_STARTED"
            product.final_price = product.base_price

 
        elif now > deadline and total_demand < product.threshold:

            if product.allow_fallback:  
                product.status = "PRODUCTION_STARTED"
                product.final_price = product.fallback_price
            else:
                product.status = "NOT_PRODUCED"
                db.commit()
                continue  

        else:
            continue  

        db.commit()  

        wishlists = db.query(Wishlist).filter_by(product_id=product.id).all()
        for w in wishlists:
            existing_order = db.query(Order).filter_by(user_id=w.user_id, product_id=product.id).first()
            if existing_order:
                continue


            user = db.query(User).filter_by(id=w.user_id).first()

            shipping_address = user.address if user and user.address else ""
            if not shipping_address:
                shipping_address = "⚠️ Address not provided (update during payment)"

            new_order = Order(
                user_id=w.user_id,
                product_id=product.id,
                quantity=w.quantity,
                final_price=product.final_price ,
                shipping_address=shipping_address,
                status="Pending",
                order_date=datetime.now(timezone.utc)
            )
            db.add(new_order)
            w.converted_to_order = True
        db.commit()
    db.close()


#------------------------ Live Auctions -----------------#
def live_auctions(user_id):
    update_auction_status()
    db = SessionLocal()
    while True:
        print("\n===== 🎯 Live Auctions =====")
        print("[1] View Active Auctions")
        print("[2] Place a Bid")
        print("[3] View My Bids")
        print("[0] Back to Dashboard")

        choice = input("Enter choice: ")

        if choice == "1":
            view_active_auctions(db)
        elif choice == "2":
            place_bid(db, user_id)
        elif choice == "3":
            view_my_bids(db, user_id)
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice. Try again.")

#------------------------ View Active Auctions -----------------#
def view_active_auctions(db):
    auctions = db.query(Auction).filter_by(status="ACTIVE").all()
    if not auctions:
        print("⚠️ No active auctions available.")
        return

    table = []
    for auc in auctions:
        table.append([
            auc.id,
            auc.title,
            auc.description,
            auc.current_highest_bid,
            auc.end_date.strftime("%Y-%m-%d %H:%M")
        ])

    print("\n📢 Active Auctions 📢\n")
    print(tabulate(table, headers=["ID", "Title", "Description", "Highest Bid", "Ends"], tablefmt="fancy_grid"))

#------------------------ Place Bid -----------------#
def place_bid(db, user_id):
    auctions = db.query(Auction).filter(Auction.status == "ACTIVE").all()
    if not auctions:
        print("⚠️ No active auctions available.")
        return

    print("\n===== 🏷️ Active Auctions 🏷️ =====")
    table = [[a.id, a.title, a.current_highest_bid, a.end_date.strftime("%Y-%m-%d %H:%M")] for a in auctions]
    print(tabulate(table, headers=["ID", "Title", "Current Highest", "Ends"], tablefmt="fancy_grid"))

    try:
        auction_id = int(input("\nEnter Auction ID to bid on: "))
        auction = db.query(Auction).filter_by(id=auction_id, status="ACTIVE").first()
        if not auction:
            print("❌ Invalid auction ID.")
            return

        existing_bid = db.query(Bid).filter_by(user_id=user_id, auction_id=auction.id).first()

        bid_amount = float(input(f"Enter your bid (current highest: {auction.current_highest_bid}): "))

        min_required = max(auction.current_highest_bid, existing_bid.bid_amount if existing_bid else 0) + 1
        if bid_amount < min_required:
            print(f"❌ Bid must be at least {min_required}.")
            return

        if existing_bid:
            existing_bid.bid_amount = bid_amount
            existing_bid.bid_time = datetime.now(timezone.utc)
            print(f"🔼 You increased your bid to {bid_amount}")
        else:
            new_bid = Bid(
                user_id=user_id,
                auction_id=auction.id,
                bid_amount=bid_amount,
                bid_time=datetime.now(timezone.utc)
            )
            db.add(new_bid)
            print(f"✅ Bid placed: {bid_amount}")

        auction.current_highest_bid = bid_amount
        auction.current_highest_bidder_id = user_id

        db.commit()
        print(f"🏆 You are now the highest bidder for '{auction.title}' at {bid_amount}!")

    except ValueError:
        print("❌ Invalid input.")

#------------------------ View My Bids -----------------#
def view_my_bids(db, user_id):
    bids = db.query(Bid).filter_by(user_id=user_id).all()
    if not bids:
        print("⚠️ You have not placed any bids yet.")
        return

    table = []
    for b in bids:
        auction = db.query(Auction).filter_by(id=b.auction_id).first()
        if not auction:
            continue  # auction deleted or missing

        status = "Winning 🏆" if b.bid_amount == auction.current_highest_bid else "Outbid ❌"
        table.append([
            b.auction_id,
            auction.title,
            b.bid_amount,
            auction.current_highest_bid,   # show latest bid in auction
            status,
            b.bid_time.strftime("%Y-%m-%d %H:%M")
        ])

    print("\n📋 Your Bids 📋\n")
    print(tabulate(
        table,
        headers=["Auction ID", "Title", "Your Bid", "Current Highest Bid", "Status", "Time"],
        tablefmt="fancy_grid"
    ))


