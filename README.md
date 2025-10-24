# Wishlist-First Marketplace CLI

A console-based e-commerce platform that empowers local artisans to produce and sell products **based on user demand**, promoting ethical, on-demand production and a **hyperlocal circular economy**.

---

## Overview

This project allows artisans to list handmade products which are only produced once a wishlist threshold is reached. Users can wishlist products, and the system can automatically convert wishlists into orders. It integrates features such as:

- Artisan management
- Product listing with threshold and time-bound conditions
- Auctions for special items
- Admin oversight of users, artisans, products, and orders
- Relisting of products as new batches
- Optional integration with local material recovery units for raw materials

This model reduces overproduction, supports sustainable manufacturing, and promotes local economy empowerment.

---

## Features

### User Module
- Signup/Login  
- Add products to wishlist  
- Track wishlists and orders  
- View profile  

### Artisan Module
- Signup/Login  
- View and edit profile  
- List new products with:
  - Wishlist threshold  
  - Time-bound listing  
  - Base & fallback price  
  - Delivery days  
- Relist products as new batches  
- View orders and auction hub  
- Auction management:
  - List auction items  
  - View & close auctions  
  - Automatic auction status updates  

### Admin Module
- Signup/Login  
- User management:
  - View, edit, delete users  
  - View user wishlists & orders  
- Artisan management:
  - View artisans & their products  
  - Edit/delete artisan details  
- Product management:
  - View all products  
  - Edit product details  
- Order & wishlist oversight:
  - View all orders  
  - Manual trigger to convert wishlists into orders  
- Payment & revenue reports (planned)  

---

## Usage

1. Run the main script to see the menu options.  
2. Choose a role: **User**, **Artisan**, or **Admin**.  
3. Follow prompts to sign up, login, and access role-specific features.  
4. Artisans can list products with thresholds and durations.  
5. Users can wishlist products and track orders.  
6. Admins can manage users, artisans, products, and process wishlists manually.  

---

## Project Structure

WishlistFirst_Marketplace/
│
├── main.py
├── modules/
│ ├── user.py
│ ├── artisan.py
│ └── admin.py
│
├── db/
│ ├── database.py
│ ├── init_db.py
│ └── reset_db.py
│
├── constants.py
├── requirements.txt
└── README.md


---

## Future Improvements
- Automated payment and revenue tracking  
- UI version of the platform  
- Enhanced auction rules and notifications  
- Integration with **Haritha Karma Sena (HKS)** for raw material collection and delivery to artisans

