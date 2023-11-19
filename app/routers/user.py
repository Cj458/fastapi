from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from dotenv import load_dotenv


from sqlalchemy.orm import Session
from celery import Celery

from app.api.external_api_calls import *
from ..worker import generate_pdf_report_async
from ..utils import *
from ..database import get_db
from .. import models, schemas

load_dotenv()


router =APIRouter(
    prefix='/users',
    tags=['Users']
)

token =os.environ.get('VK_ACCESS_TOKEN')

output_directory = os.environ.get('OUTPUT_DIRECTORY')


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    queryset = db.query(models.User).all()
    return queryset


@router.get("/{user_id}",)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {user_id} was not found')
    user_data = get_user_data_from_vk(user.id, token)

    generate_pdf_report_async(user_data, output_directory)


    # this is a workaround for excluding password in the response
    user={
        'id': user.id,
        'username': user.username,
    }

    return {'user': user, 'vk data': user_data}


# delete endpoint


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_pwd=hash_password(user.password)
    user.password=hashed_pwd
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# as i am unable to get apis keys for telegram and instagram, this is a shorter version just for the endpoint to be functional
@router.put("/connect_user/{user_id}", status_code=status.HTTP_200_OK)
def connect_user(user_id: int, updated_user: schemas.UserBase, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter_by(id=user_id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {user_id} was not found')
    
    user_query.update(updated_user.model_dump(), synchronize_session=False)
    db.commit()

    return {'data': user_query.first()}



#@router.put("/connect_user/{user_id}", status_code=status.HTTP_200_OK)
#def connect_user(user_id: int, updated_user: schemas.UserBase, db: Session = Depends(get_db)):
#     existing_user = session.query(User).filter_by(id=user_id).first()
#     if existing_user:
#         telegram_user_info = get_telegram_user_info(telegram_user_id)

#         existing_user.telegram_user_id = telegram_user_id
#         existing_user.telegram_first_name = telegram_user_info.get('first_name', '')
#         existing_user.telegram_last_name = telegram_user_info.get('last_name', '')

#         session.commit()
#     else:
#         return {'error':f"User with ID {user_id} not found."}