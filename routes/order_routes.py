from fastapi import Depends, status, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from model import foodibizz_models
from schema import foodibizz_schemas
from db_conn import get_db

approute = APIRouter(
    prefix='/Order',
    tags=['Orders']
    )

# add order
@approute.post("/add-order", status_code = status.HTTP_201_CREATED)
def addOrder(order: foodibizz_models.OrderModel, db: Session = Depends(get_db)):
    new_order = foodibizz_schemas.Order(
        billingDate = order.billingDate,
        invNum = order.invNum,
        noOfItems = order.noOfItems,
        discount = order.discount,
        gst = order.gst,
        grandTotal = order.grandTotal
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return new_order

# get all orders
@approute.get("/all-orders")
def allOrders(db: Session = Depends(get_db)):
    allOrders = db.query(foodibizz_schemas.Order).all()
    
    return {"allOrders": allOrders}

# delete order
@approute.delete("/delete-order/{id}" , status_code = status.HTTP_204_NO_CONTENT)
def deleteOrder(id: int, db: Session = Depends(get_db)):
    order = db.query(foodibizz_schemas.Order).filter(foodibizz_schemas.Order.id == id)
    
    if order.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with {id} not found")
    
    # delete data
    order.delete(synchronize_session = False) 
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)