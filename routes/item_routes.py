from fastapi import Depends, status, APIRouter, UploadFile, File, Form, HTTPException, Response
from sqlalchemy.orm import Session
from model import foodibizz_models
from schema import foodibizz_schemas
from db_conn import get_db
import shutil
import datetime
import time
import os

approute = APIRouter(
    prefix='/item',
    tags=['Food Item']
    )

# add new food item
@approute.post("/add-fooditem", status_code = status.HTTP_201_CREATED)
async def createItem(
    name: str = Form(...),
    desc:  str = Form(...),
    price: float = Form(...),
    creationDate: datetime.datetime = Form(...),
    foodImage: UploadFile = File(None),
    db: Session = Depends(get_db)):
    
    milliseconds = int(round(time.time() * 1000))
    date = time.strftime("%Y%m%d %H%M%S", time.gmtime()).split(' ')[0]
    currenttime = time.strftime("%Y%m%d %H%M%S", time.gmtime()).split(' ')[1]
    
    # save file
    file_location = ''
    if foodImage is not None:
        file_location = f"images/{milliseconds}{date}{currenttime}{foodImage.filename}"
        with open(file_location, 'wb') as buffer:
            shutil.copyfileobj(foodImage.file, buffer)
        
    # assign data to insert
    new_food_item = foodibizz_schemas.Item(name=name, desc = desc, price = price, 
                                      image = file_location, creationDate = creationDate, 
                                      lastModifiedDate = creationDate)
    # insert
    db.add(new_food_item)
    db.commit()
    db.refresh(new_food_item)
    
    return new_food_item

# get all food item
@approute.get("/all-fooditems")
def allFoodItems(db: Session = Depends(get_db)):
    foodItems = db.query(foodibizz_schemas.Item).all()
    
    return {"foodItems": foodItems}

# update food item
@approute.put("/update-fooditem/{id}", status_code= status.HTTP_202_ACCEPTED)
def updateFoodItem(
    id: int, 
    name: str = Form(...),
    desc:  str = Form(...),
    price: float = Form(...),    
    lastModifiedDate: datetime.datetime = Form(...),
    foodImage: UploadFile = File(None),
    db: Session = Depends(get_db)
    ):
    foodItem = db.query(foodibizz_schemas.Item).filter(foodibizz_schemas.Item.id == id)
    
    if foodItem.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Food item with {id} not found")
    
    # update and save file
    # also delete previous image if exist and
    # update with new image
    file_location = ""
    if foodImage is not None:
        existFoodItem = foodItem.first()
        if existFoodItem.image != '':
            if os.path.exists(existFoodItem.image):
                os.remove(existFoodItem.image)
    
        milliseconds = int(round(time.time() * 1000))
        date = time.strftime("%Y%m%d %H%M%S", time.gmtime()).split(' ')[0]
        currenttime = time.strftime("%Y%m%d %H%M%S", time.gmtime()).split(' ')[1]
        file_location = f"images/{milliseconds}{date}{currenttime}{foodImage.filename}"
    else:
        existFoodItem = foodItem.first()
        file_location = existFoodItem.image
    
    if foodImage is not None:
        with open(file_location, 'wb') as buffer:
            shutil.copyfileobj(foodImage.file, buffer)
        
    # assign new data to update
    newFoodItem = foodibizz_models.ItemModel(id = id, name=name, desc = desc, price = price, 
                                      image = file_location, creationDate = existFoodItem.creationDate, 
                                      lastModifiedDate = lastModifiedDate)
    
    # update
    foodItem.update(newFoodItem.dict())
    db.commit()
    
    return {"detail": f"Food item {id} updated"}

# delete food item
@approute.delete("/delete-fooditem/{id}" , status_code = status.HTTP_204_NO_CONTENT)
def deleteFoodItem(id: int, db: Session = Depends(get_db)):
    foodItem = db.query(foodibizz_schemas.Item).filter(foodibizz_schemas.Item.id == id)
    
    if foodItem.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Food item with {id} not found")
    
    # delete file
    fooditemfirst = foodItem.first()
    if os.path.exists(fooditemfirst.image):
        os.remove(fooditemfirst.image)
    
    # delete 
    foodItem.delete(synchronize_session = False) 
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

