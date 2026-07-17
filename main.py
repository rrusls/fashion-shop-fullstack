from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel
from typing import Optional, List, Literal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#CORS to link backend to frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"]
)
URL_DATABASE = "sqlite:///./mara.db"

engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    img = Column(String)
    price = Column(Integer, index=True)
    category = Column(String(50), index=True)
    amount = Column(Integer, index=True)

Base.metadata.create_all(engine)

# Pydantic Model
class ItemCreate(BaseModel): # data format while enter / exit API (for checking)
    name : str
    img : str
    price: int
    category : str
    amount : int

class ItemResponse(BaseModel): 
    id : int
    name : str
    img : str
    price: int
    category : str
    amount : int

    class ConfigDict:
        from_attributes = True

# Cart
class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    size = Column(String(50),index=True)
    amount = Column(Integer, default=1)

class ItemSize(Base):
    __tablename__ = "item_sizes"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    size = Column(String(10))
# creating a table cart_items 
Base.metadata.create_all(engine)

class CartItemCreate(BaseModel):
    item_id : int
    size : str
    amount : int = 1

class CartItemUpdate(BaseModel): # what are we gonna update store here
    amount : int

class CartItemResponse(BaseModel):
    id : int
    item_id : int
    size : str
    amount : int
    name : str
    price : int
    img : str

class ItemSizeResponse(BaseModel):
    id : int
    item_id : int
    size : str


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.get("/items/{category}",response_model=List[ItemResponse])
def get_category_items(category: str, db:Session=Depends(get_db)):
    db_category_items = db.query(Item).filter(Item.category == category)
    db_items = db_category_items.all()
    if category == "all":
        return db.query(Item).all()
    elif (category !="all" and category not in ["shoes", "clothes"]):
        raise HTTPException(status_code=404, detail='No such category')
    
    if not db_items:
        raise HTTPException(status_code=404, detail='Out of stock')
    else:
        return db_items
# Get Item By ID
#@app.get("/items/{category}/{item_id}", response_model=ItemResponse)
#def get_item(item_id: int, db: Session = Depends(get_db)):
 #   item = db.query(Item).filter(Item.id == item_id).first()
  #  if not item:
  # raise HTTPException(status_code=404, detail='dslgn') #if there is no item
   ##return item

@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    if db.query(Item).filter(Item.name == item.name).first():
        raise HTTPException(status_code=404, detail="Item already exists")

    # Create a new item
    new_item = Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item: ItemCreate, item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item does not exist")
    
    for field, value in item.dict().items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item does not exist")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}


@app.get("/cart", response_model=List[CartItemResponse])
def get_cart(db:Session=Depends(get_db)):
    cart_rows = db.query(CartItem, Item).join(Item, CartItem.item_id == Item.id).all()

    result = []
    for cart_i, product in cart_rows:
        cart_dict = {
            "id": cart_i.id,
            "item_id": cart_i.item_id,
            "size": cart_i.size,
            "amount": cart_i.amount,
            "name": product.name,
            "price": product.price,
            "img": product.img
        }
        result.append(cart_dict)
    
    return result

@app.post("/cart", response_model=CartItemResponse)
def add_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == cart_item.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    existing = db.query(CartItem).filter(
        CartItem.item_id == cart_item.item_id,
        CartItem.size == cart_item.size
    ).first()

    if existing:
        existing.amount += cart_item.amount
        db.commit()
        db.refresh(existing)
        db_cart_item = existing
    else:
        db_cart_item = CartItem(item_id=cart_item.item_id, size=cart_item.size, amount=cart_item.amount)
        db.add(db_cart_item)
        db.commit()
        db.refresh(db_cart_item)

    return {
        "id": db_cart_item.id,
        "item_id": db_cart_item.item_id,
        "size": db_cart_item.size,
        "amount": db_cart_item.amount,
        "name": item.name,
        "price": item.price,
        "img": item.img
    }


@app.put("/cart/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(cart_item_id: int, update: CartItemUpdate, db: Session = Depends(get_db)):
    db_cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db_cart_item.amount = update.amount
    db.commit()
    db.refresh(db_cart_item)

    item = db.query(Item).filter(Item.id == db_cart_item.item_id).first()

    return {
        "id": db_cart_item.id,
        "item_id": db_cart_item.item_id,
        "size": db_cart_item.size,
        "amount": db_cart_item.amount,
        "name": item.name,
        "price": item.price,
        "img": item.img
    }


@app.delete("/cart/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db)):
    db_cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(db_cart_item)
    db.commit()
    return {"message": "Removed from cart"}

#Get size for an item 
@app.get("/items/{item_id}/sizes", response_model=List[str])
def get_item_sizes(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    sizes = db.query(ItemSize).filter(ItemSize.item_id == item_id).all()
    result = []
    for i in sizes:
        result.append(i.size)
    return result
