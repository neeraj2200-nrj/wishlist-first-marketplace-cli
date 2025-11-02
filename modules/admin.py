from sqlalchemy.orm import Session
from db.database import SessionLocal,User, Artisan, Product, Order, Wishlist, Admin
#from datetime import datetime, timezone
from tabulate import tabulate
from sqlalchemy import or_
from . user import process_wishlists_to_orders


#------------------------ Admin Register -----------------#

def register_admin():
    db: Session=SessionLocal()
    print("📝---- Admin Sign Up ----📝")
    name = input("Enter the username: ")
    email = input("Enter the email ID: ")
    password = input("Enter the password: ")
    phone_no = input("Enter the phone number: ")
    aadhar_no = input("Enter the aadhar number: ")
    role = input("Enter the role : ")

    if not email.endswith(".com"):
        print("⚠️  Enter Valied Email ID ⚠️")
        return
    
    if not (phone_no.isdigit() and len(phone_no)==10):
        print("⚠️  Enter Valied Phone Number ⚠️")
        return
    
    if not (aadhar_no.isdigit() and len(aadhar_no)==12):
        print("⚠️  Enter Valied Aadhar Number ⚠️")
        return
    
    existing_admin = db.query(Admin).filter(
        or_(
            Admin.name == name,
            Admin.email == email,
            Admin.phone_no == phone_no,
            Admin.aadhar_no == aadhar_no
        )
    ).first()

    if existing_admin:
        if existing_admin.name == name:
            print("⚠️  Admin name already exists! ⚠️")
        elif existing_admin.email == email:
            print("⚠️  Email already exists! ⚠️")
        elif existing_admin.phone_no == phone_no:
            print("⚠️  Phone number already exists! ⚠️")
        elif existing_admin.aadhar_no == aadhar_no:
            print("⚠️  Aadhar number already exists! ⚠️")
        db.close()
        return

    try:
        new_admin=Admin(name=name,email=email,password=password,phone_no=phone_no,aadhar_no=aadhar_no,role=role,)
        db.add(new_admin)
        db.commit()
        print("✅ Admin Signup Successfull ✅")
    except Exception as e:
        print("❌  Can't add the Admin. Error:",str(e))
    finally:
        db.close()

#------------------------ Login User -----------------#
def login_admin():
    db:Session=SessionLocal()
    print("🗝️  Admin Sign In 🗝️")
    name = input("Enter the admin name: ")
    password = input("Enter the password: ")

    admin = db.query(Admin).filter_by(name=name,password=password).first()
    if admin:
        print("\n🙏 Welcome ",admin.name)
        admin_menu()
    else:
        print("❌ Invalid Credentials ❌")

#------------------------ Admin Menu -----------------#

def admin_menu():
    while True:
        print("\n🛡️  Admin Dashboard 🛡️")
        print("[1]  User Management")
        print("[2]  Artisan Management")
        print("[3]  Product Management")
        print("[4]  Order & Wishlist Oversight")
        #print("[5]  Payments & Reports")
        print("[0]  Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            user_management()
        elif choice == "2":
            artisan_management()
        elif choice == "3":
            product_management()
        elif choice == "4":
            order_wishlist_management()
        #elif choice == "5":
        #    payments_reports()
        elif choice == "0":
            print("Logging out of Admin Dashboard...")
            break
        else:
            print("❌ Invalid choice. Try again.")

#------------------------ User Management -----------------#
def user_management():
    while True:
        print("\n👤 User Management")
        print("[1]  View All Users")
        print("[2]  View User Wishlists")
        print("[3]  View User Orders")
        print("[4]  Edit/Delete User")
        print("[0]  Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_all_users()
        elif choice == "2":
            view_user_wishlists()
        elif choice == "3":
            view_user_orders()
        elif choice == "4":
            edit_delete_user()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice. Try again.")

#------------------------ Artisan Management -----------------#
def artisan_management():
    while True:
        print("\n🎨 Artisan Management")
        print("[1]  View All Artisans")
        print("[2]  View Artisan Products")
        print("[3]  Edit Artisan Details")
        #print("[4]  Approve/Reject Artisan (Coming soon)")
        print("[0]  Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_all_artisans()
        elif choice == "2":
            view_artisan_products()
        elif choice == "3":
            edit_delete_artisan()
        #elif choice == "4":
            #approve_reject_artisan()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice. Try again.")

#------------------------ Product Management -----------------#
def product_management():
    while True:
        print("\n🛍️  Product Management")
        print("[1]  View All Products")
        print("[2]  Edit Product Details")
        #print("[3]  Add / Remove Category (Coming Soon)")
        #print("[4]  Expire / Approve Product (Coming Soon)")
        print("[0]  Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_all_products()
        elif choice == "2":
            edit_product()
        #elif choice == "3":
        #    manage_categories()
        #elif choice == "4":
        #    expire_approve_product()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice. Try again.")

#------------------------ Order/Wishlist Management -----------------#
def order_wishlist_management():
    while True:
        print("\n📦 Order & Wishlist Oversight")
        print("[1]  View All Orders")
        print("[2]  Convert Wishlists to Orders (Manual Trigger)")
        #print("[3]  View Pending Orders")
        print("[0]  Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_all_orders_admin()
        elif choice == "2":
            process_wishlists_to_orders()
            print("✅ Wishlists processed into orders.") 
        #elif choice == "3":
        #    view_pending_orders()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice. Try again.")

#------------------------ Payments Reports -----------------#
'''def payments_reports():
    while True:
        print("\n💰 Payments & Reports")
        print("[1]  View All Payments")
        print("[2]  View Revenue by Product / Artisan / Category")
        print("[3]  Generate Sales Reports")
        print("[0]  Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_all_payments()
        elif choice == "2":
            revenue_report()
        elif choice == "3":
            sales_report()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice. Try again.")'''

#------------------------ View All Users -----------------#

def view_all_users():
    db: Session = SessionLocal()
    users = db.query(User).all()

    if not users:
        print("\n📭 No users registered yet.\n")
        db.close()
        return

    table = []
    for user in users:
        table.append([
            user.id,
            user.username,
            user.email,
            user.phone_no,
            user.address if user.address else "❌ Not Provided",
            user.aadhar_no if user.aadhar_no else "❌ Not Provided",
            user.date_of_birth if user.date_of_birth else "❌ Not Provided"
        ])

    print("\n👥 Registered Users:\n")
    print(tabulate(table, headers=["ID", "Name", "Email", "Phone", "Address", "Aadhar", "DOB"], tablefmt="fancy_grid"))

    db.close()

#------------------------ View User Wishlists -----------------#
def view_user_wishlists():
    db: Session = SessionLocal()
    user_id = int(input("\n🔍 Enter the User ID to view wishlists: "))
    
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        print("⚠️ No such user found.")
        db.close()
        return
    
    wishlists = db.query(Wishlist).filter_by(user_id=user_id).all()
    if not wishlists:
        print(f"\n📭 User '{user.username}' has no wishlisted products.\n")
        db.close()
        return
    
    table = []
    for wl in wishlists:
        product = db.query(Product).filter_by(id=wl.product_id).first()
        table.append([
            wl.id,
            product.product_name if product else "❌ Product Deleted",
            wl.quantity,
            wl.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        ])

    print(f"\n📝 Wishlists of User: {user.username}\n")
    print(tabulate(table, headers=["Wishlist ID", "Product", "Quantity", "Timestamp"], tablefmt="fancy_grid"))
    
    db.close()

#------------------------ View User Orders -----------------#
def view_user_orders():
    db: Session = SessionLocal()
    user_id = int(input("\n🔍 Enter the User ID to view orders: "))
    
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        print("⚠️ No such user found.")
        db.close()
        return

    orders = db.query(Order).filter_by(user_id=user_id).all()
    if not orders:
        print(f"\n📭 User '{user.username}' has no orders.\n")
        db.close()
        return

    table = []
    for o in orders:
        product = db.query(Product).filter_by(id=o.product_id).first()
        table.append([
            o.id,
            product.product_name if product else "❌ Product Deleted",
            o.quantity,
            f"₹{o.final_price}",
            o.status,
            o.order_date.strftime("%Y-%m-%d %H:%M:%S"),
            o.shipping_address if o.shipping_address else "⚠️ Address not provided"
        ])

    print(f"\n🛒 Orders of User: {user.username}\n")
    print(tabulate(table, headers=["Order ID", "Product", "Quantity", "Unit Price", "Status", "Order Date", "Shipping Address"], tablefmt="fancy_grid"))
    
    db.close()

#------------------------ Edit/Delete User -----------------#
def edit_delete_user():
    db: Session = SessionLocal()
    user_id = int(input("\n🔍 Enter the User ID to edit/delete: "))
    
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        print("⚠️ No such user found.")
        db.close()
        return

    print(f"\n👤 Selected User: {user.username} (ID: {user.id})")
    print("[1]  Edit User")
    print("[2]  Delete User")
    print("[0]  Cancel")
    
    choice = input("Enter your choice: ").strip()
    
    if choice == "1":
        # Edit fields
        new_username = input(f"Enter new username (current: {user.username}): ").strip()
        new_email = input(f"Enter new email (current: {user.email}): ").strip()
        new_phone = input(f"Enter new phone (current: {user.phone_no}): ").strip()
        
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_phone:
            user.phone_no = new_phone
        
        db.commit()
        print(f"✅ User ID {user.id} updated successfully.")
    
    elif choice == "2":
        confirm = input(f"⚠️ Are you sure you want to delete user '{user.username}'? (y/n): ").lower()
        if confirm == "y":
            db.delete(user)
            db.commit()
            print(f"❌ User ID {user.id} deleted successfully.")
        else:
            print("❌ Deletion cancelled.")
    
    else:
        print("❌ Operation cancelled.")

    db.close()

#------------------------ View All Artisans -----------------#

def view_all_artisans():
    db = SessionLocal()
    artisans = db.query(Artisan).all()

    if not artisans:
        print("\n📭 No artisans registered yet.\n")
        db.close()
        return

    table = []
    for a in artisans:
        table.append([
            a.id,
            a.artisan_name,
            a.email,
            a.phone_no,
            a.location,
            a.ward_number,
            a.joined_at.strftime('%Y-%m-%d %H:%M:%S') if a.joined_at else "-"
        ])

    print("\n🎨 Registered Artisans 🎨\n")
    print(tabulate(
        table,
        headers=["ID", "Name", "Email", "Phone", "Craft Type", "Location", "Ward No", "Joined At"],
        tablefmt="fancy_grid"
    ))

    db.close()

#------------------------ View Artisan Products -----------------#

def view_artisan_products():
    db = SessionLocal()
    artisans = db.query(Artisan).all()

    if not artisans:
        print("\n📭 No artisans registered yet.\n")
        db.close()
        return

    for artisan in artisans:
        products = db.query(Product).filter_by(artisan_id=artisan.id).all()
        if not products:
            print(f"\n🎨 Artisan '{artisan.artisan_name}' has not listed any products.\n")
            continue

        table = []
        for p in products:
            table.append([
                p.id,
                p.product_name,
                p.category,
                p.threshold,
                p.duration_days,
                p.base_price,
                p.fallback_price,
                p.final_price,
                p.status
            ])

        print(f"\n🎨 Products of Artisan '{artisan.artisan_name}' 🎨\n")
        print(tabulate(
            table,
            headers=["Product ID", "Name", "Category", "Threshold", "Duration (days)",
                     "Base Price", "Fallback Price", "Final Price", "Status"],
            tablefmt="fancy_grid"
        ))

    db.close()

#------------------------ Edit/Delete Artisan -----------------#

def edit_delete_artisan():
    db = SessionLocal()
    
    # Show all artisans
    artisans = db.query(Artisan).all()
    if not artisans:
        print("\n📭 No artisans found.\n")
        db.close()
        return

    table = [[a.id, a.artisan_name, a.email, a.phone_no, a.location] for a in artisans]
    print("\n👨‍🎨 Registered Artisans 👨‍🎨\n")
    print(tabulate(table, headers=["ID", "Name", "Email", "Phone", "Location"], tablefmt="fancy_grid"))

    try:
        artisan_id = int(input("\nEnter the ID of the artisan to edit/delete: ").strip())
    except ValueError:
        print("❌ Invalid input.")
        db.close()
        return

    artisan = db.query(Artisan).filter_by(id=artisan_id).first()
    if not artisan:
        print("❌ Artisan not found.")
        db.close()
        return

    choice = input("\nDo you want to [E]dit or [D]elete this artisan? (E/D): ").strip().lower()
    
    if choice == "e":
        print("\nLeave input blank to keep current value.\n")
        new_name = input(f"Name [{artisan.artisan_name}]: ").strip()
        new_email = input(f"Email [{artisan.email}]: ").strip()
        new_phone = input(f"Phone [{artisan.phone_no}]: ").strip()
        new_address = input(f"Address [{artisan.address}]: ").strip()
        new_location = input(f"Location [{artisan.location}]: ").strip()
    
        if new_name: artisan.artisan_name = new_name
        if new_email: artisan.email = new_email
        if new_phone: artisan.phone_no = new_phone
        if new_address: artisan.address = new_address
        if new_location: artisan.location = new_location

        db.commit()
        print(f"\n✅ Artisan '{artisan.artisan_name}' updated successfully!\n")

    elif choice == "d":
        confirm = input(f"⚠️ Are you sure you want to delete '{artisan.artisan_name}'? This cannot be undone. (y/n): ").strip().lower()
        if confirm == "y":
            db.delete(artisan)
            db.commit()
            print(f"\n❌ Artisan '{artisan.artisan_name}' has been deleted.\n")
        else:
            print("\n❌ Deletion cancelled.\n")
    else:
        print("❌ Invalid choice. Please select E or D.")

    db.close()

#------------------------ View All Product -----------------#

def view_all_products():
    db = SessionLocal()
    products = db.query(Product).all()

    if not products:
        print("\n📭 No products found in the marketplace.\n")
        db.close()
        return

    table = []
    for product in products:
        table.append([
            product.id,
            product.product_name,
            product.category,
            product.threshold,
            product.base_price,
            product.fallback_price,
            product.status,
            product.artisan_id
        ])

    print("\n🛒 All Marketplace Products:\n")
    headers = ["ID", "Name", "Category", "Threshold", "Base Price", "Fallback Price", "Status", "Artisan ID"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    db.close()

#------------------------ Edit Product -----------------#
def edit_product(artisan_id: int):
    db = SessionLocal()

    # Fetch artisan's products
    products = db.query(Product).filter(Product.artisan_id == artisan_id).all()
    if not products:
        print("\n📭 You have no products listed to edit.\n")
        db.close()
        return

    print("\n🛠 Your Products:\n")
    for product in products:
        print(f"ID: {product.id} | Name: {product.product_name} | Status: {product.status}")

    try:
        product_id = int(input("\nEnter the Product ID you want to edit: "))
    except ValueError:
        print("❌ Invalid input.")
        db.close()
        return

    product = db.query(Product).filter(Product.id == product_id, Product.artisan_id == artisan_id).first()

    if not product:
        print("❌ Product not found or you don’t own it.")
        db.close()
        return

    print("\n--- Editing Product ---")
    new_name = input(f"Enter new name ({product.product_name}): ") or product.product_name
    new_category = input(f"Enter new category ({product.category}): ") or product.category
    try:
        new_threshold = int(input(f"Enter new wishlist threshold ({product.threshold}): ") or product.threshold)
    except ValueError:
        new_threshold = product.threshold
    try:
        new_base_price = float(input(f"Enter new base price ({product.base_price}): ") or product.base_price)
    except ValueError:
        new_base_price = product.base_price
    try:
        new_fallback_price = float(input(f"Enter new fallback price ({product.fallback_price}): ") or product.fallback_price)
    except ValueError:
        new_fallback_price = product.fallback_price
    new_status = input(f"Enter new status ({product.status}): ") or product.status

    product.product_name = new_name
    product.category = new_category
    product.threshold = new_threshold
    product.base_price = new_base_price
    product.fallback_price = new_fallback_price
    product.status = new_status

    db.commit()
    print("\n✅ Product updated successfully!\n")

    db.close()

#------------------------ View All Orders (Admin Version) -----------------#
def view_all_orders_admin():
    db = SessionLocal()
    orders = (
        db.query(Order, Product, Artisan)
        .join(Product, Order.product_id == Product.id)
        .join(Artisan, Product.artisan_id == Artisan.id)
        .all()
    )

    if not orders:
        print("\n📭 No orders found in the marketplace.\n")
        db.close()
        return

    table = []
    for order, product, artisan in orders:
        table.append([
            order.id,
            product.product_name,
            artisan.artisan_name,
            order.user_id,
            order.quantity,
            f"₹{order.final_price}",
            order.status,
            order.order_date.strftime("%Y-%m-%d %H:%M:%S") if order.order_date else "N/A"
        ])

    print("\n📦 All Marketplace Orders:\n")
    print(tabulate(
        table,
        headers=["Order ID", "Product", "Artisan", "User ID", "Quantity", "Total Price", "Status", "Order Date"],
        tablefmt="fancy_grid"
    ))

    db.close()

