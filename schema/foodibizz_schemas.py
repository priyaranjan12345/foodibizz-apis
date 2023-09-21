from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from db_conn import base

class Item(base):
    __tablename__ = 'Items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    desc = Column(String(400))
    price = Column(Float(4,2))
    image = Column(String(400))
    creationDate = Column(DateTime)
    lastModifiedDate = Column(DateTime)
    
class Order(base):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True, index=True)
    billingDate = Column(DateTime)
    invNum = Column(String(60))
    noOfItems = Column(Integer)
    discount = Column(Float(6, 2))
    gst = Column(Float(6, 2))
    grandTotal = Column(Float(6, 2))
    

class Sold(base):
    __tablename__ = 'Solds'

    id = Column(Integer, primary_key=True, index=True)
    itemQty = Column(Integer)
    orderId = Column(Integer, ForeignKey('Orders.id'))
    itemId = Column(Integer, ForeignKey('Items.id'))
    itemUnitPrice = Column(Float(6, 2))
    