from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Union

class Image(BaseModel):
    url: HttpUrl
    name: str

# item
# request json type
class ItemModel(BaseModel):
    id: int
    name: str
    desc:  str
    price: float
    image: str
    creationDate: datetime
    lastModifiedDate: datetime

# response json type
class ShowItem(BaseModel): 
    id: int
    name: str
    desc:  str
    price: float
    image: str
    creationDate: datetime
    lastModifiedDate: datetime
    
    class Config:
        orm_mode = True
        
# Order
# request model
class OrderModel(BaseModel):
    id: int
    billingDate: datetime
    invNum: Union[str, None] = Field(
        default=None, title="invoice number is required", max_length=300, min_length=10
    )
    noOfItems: int
    discount: float
    gst: float
    grandTotal: float
    
# response model
class ShowOrder(BaseModel):
    id: int
    billingDate: datetime
    invNum: str
    noOfItems: int
    discount: float
    gst: float
    grandTotal: float
    
    class Config:
        orm_mode = True

# Sold
# request Model
class SoldItemModel(BaseModel):
    id: int
    itemQty: int
    orderId: int
    itemId: int
    itemUnitPrice: float
    
class SoldItemModels(BaseModel):
    soldItemModels: List[SoldItemModel]
    
# response model
class ShowSoldItem(BaseModel):
    id: int
    itemQty: int
    orderId: int
    itemId: int
    
    
    class Config:
        orm_mode = True
        
class ItemWithSold(BaseModel):
    name: str
    image: str
    orderId: int
    itemId: int
    itemQty: int
    price: float
    totalAmount: float
    
    class Config:
        orm_mode = True