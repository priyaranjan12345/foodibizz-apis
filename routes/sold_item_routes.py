from fastapi import Depends, status, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from model import foodibizz_models
from schema import foodibizz_schemas
from db_conn import get_db

approute = APIRouter(
    prefix='/sold',
    tags=['Sold']
    )

# add sold items
@approute.post("/add-solditem", status_code = status.HTTP_201_CREATED)
async def addOrder(solditems: foodibizz_models.SoldItemModels, db: Session = Depends(get_db)):
    
    for solditem in solditems.soldItemModels:
        newSoldItem = foodibizz_schemas.Sold(id = solditem.id, itemQty = solditem.itemQty, 
                                             orderId = solditem.orderId, itemId = solditem.itemId, 
                                             itemUnitPrice = solditem.itemUnitPrice)
        db.add(newSoldItem)
        db.commit()
     
    return solditems

# get items according to order number
# join item table with sold table 
@approute.get("/all-solditems/{orderId}")
def getSoldItems(orderId: int, db: Session = Depends(get_db)):
    datas = db.query(foodibizz_schemas.Item, 
                     foodibizz_schemas.Sold).select_from(foodibizz_schemas.Item).join(foodibizz_schemas.Sold).filter(foodibizz_schemas.Sold.orderId == orderId).all()
    
    soldWithItemList = []
    for data in datas:
        item = data[0]
        sold = data[1]
        soldWithItem = foodibizz_models.ItemWithSold(
            name = item.name,
            image = item.image,
            itemId = sold.itemId,
            orderId = sold.orderId,
            itemQty = sold.itemQty,
            price = sold.itemUnitPrice,
            totalAmount = sold.itemQty * item.price
        )
        
        soldWithItemList.append(soldWithItem)
    return {"allSoldItems": soldWithItemList}

# delete according to order number
@approute.delete("/delete-sold-by-orderid/{orderId}" , status_code = status.HTTP_204_NO_CONTENT)
def deleteOrder(orderId: int, db: Session = Depends(get_db)):
    orderItem = db.query(foodibizz_schemas.Sold).filter(foodibizz_schemas.Sold.orderId == orderId)
    
    if orderItem.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with {orderId} not found")
    
    # delete data
    orderItem.delete(synchronize_session = False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
