import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Boolean, DateTime , Date,Float,Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, timezone 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_USER = "postgres"  
DB_PASSWORD = "123456"  
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "wishlist_db"

Base=declarative_base()
default=lambda: datetime.now(timezone.utc)

# Engine and session setup
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=False
)

SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

#---------------------- User Table ---------------------#
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50),unique=True)
    password = Column(String(50))
    email = Column(String(100),unique=True)
    aadhar_no = Column(String(12),unique=True,nullable=False)
    phone_no = Column(String(10),unique=True,nullable=False)
    full_name = Column(String,nullable=False)
    address = Column(String,nullable=False)
    date_of_birth = Column(Date,nullable=True)
    joined_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    wishlists = relationship("Wishlist",back_populates="user")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")
    bids = relationship("Bid", back_populates="user")


#---------------------- Artisan Table ---------------------#
class Artisan(Base):
    __tablename__ = "artisans"
    id = Column(Integer, primary_key=True)
    artisan_name = Column(String(50),unique=True)
    password = Column(String(50))
    email = Column(String(100),unique=True)
    aadhar_no = Column(String(12),unique=True,nullable=False)
    phone_no = Column(String(10),unique=True,nullable=False)
    address = Column(String,nullable=False)
    date_of_birth = Column(Date,nullable=True)
    location = Column(String(100))
    ward_number = Column(String)
    joined_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    products = relationship("Product", back_populates="artisan")
    requests = relationship("RawMaterialRequest", back_populates="artisan")
    auctions = relationship("Auction", back_populates="artisan")


#---------------------- Admin Table ---------------------#
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # hashed later
    phone_no = Column(String, nullable=True)
    aadhar_no = Column(String(12),unique=True,nullable=False)
    role = Column(String, default="superadmin")  # could allow multiple roles in future
    joined_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

#---------------------- Product Table ---------------------#
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    artisan_id = Column(Integer, ForeignKey("artisans.id"))
    product_name = Column(String(100))
    description = Column(Text)
    category = Column(String(50))
    base_price = Column(Float, nullable=False)
    fallback_price = Column(Float,nullable=False)
    final_price = Column(Float, nullable=False)
    listing_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(Enum("ACTIVE", "PRODUCTION_STARTED", "EXPIRED", "NOT_PRODUCED", name="product_status"),default="ACTIVE")
    threshold = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)
    delivery_days = Column(Integer, nullable=False)
    allow_fallback = Column(Boolean, default=False)


    wishlists = relationship("Wishlist", back_populates="product")
    artisan = relationship("Artisan", back_populates="products")
    orders = relationship("Order", back_populates="product")
#---------------------- Wishlist Table ---------------------#
class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    converted_to_order = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="wishlists")
    product = relationship("Product", back_populates="wishlists")

#---------------------- RawMaterialRequest Table ---------------------#
class RawMaterialRequest(Base):
    __tablename__ = "raw_material_request"
    id = Column(Integer, primary_key=True)
    artisan_id = Column(Integer, ForeignKey("artisans.id"))
    material = Column(String(100))
    quantity = Column(String(50))
    status = Column(String(50),default="pending")

    artisan = relationship("Artisan", back_populates="requests")

#---------------------- Orders Table ---------------------#
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer,primary_key=True,index=True)
    user_id  = Column(Integer,ForeignKey("users.id"))
    product_id = Column(Integer,ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    final_price = Column(Float)
    shipping_address = Column(String, nullable=False)
    status = Column(String,default="Pending Payment")
    order_date = Column(DateTime,default=lambda: datetime.now(timezone.utc))

    payment = relationship("Payment", back_populates="order", uselist=False)
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    
#---------------------- Payments Table ---------------------#
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float)
    upi_id = Column(String, nullable=False)
    status = Column(Enum("Pending","Successfull","Failed",name="payment_status"), default="Pending")
    paid_at = Column(DateTime,default=lambda: datetime.now(timezone.utc))

    order = relationship("Order", back_populates="payment")
    user = relationship("User", back_populates="payments")

#---------------------- Auction Table ---------------------#
class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    artisan_id = Column(Integer, ForeignKey("artisans.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    starting_bid = Column(Float, nullable=False)
    current_highest_bid = Column(Float, nullable=True)
    current_highest_bidder_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    start_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    end_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum("ACTIVE", "ENDED", "SOLD", name="auction_status"), default="ACTIVE")

    artisan = relationship("Artisan", back_populates="auctions")
    highest_bidder = relationship("User",foreign_keys=[current_highest_bidder_id])
    bids = relationship("Bid", back_populates="auction", cascade="all, delete-orphan")

#---------------------- Bid Table ---------------------#

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, autoincrement=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bid_amount = Column(Float, nullable=False)
    bid_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="bids")
    auction = relationship("Auction", back_populates="bids")





