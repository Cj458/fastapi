from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from dotenv import load_dotenv


from sqlalchemy.orm import Session
from celery import Celery

from app.api.vk_api import *
from ..worker import generate_pdf_report_async
from ..utils import *
from ..database import get_db
from .. import models, schemas

load_dotenv()



# celery = Celery(__name__)
# celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
# celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
# celery = Celery('tasks', broker='redis://localhost:6379/0')
# # celery.config_from_object('celeryconfig')
# celery.conf.task_routes = {"app.routers.user.generate_pdf_report_async": "main-queue"}
# celery.autodiscover_tasks()

router =APIRouter(
    prefix='/users',
    tags=['Users']
)

token =os.environ.get('VK_ACCESS_TOKEN')

output_directory = os.environ.get('OUTPUT_DIRECTORY')

# @celery.task
# def generate_pdf_report_async(user_data, output_dir):
#     return generate_pdf_report(user_data, output_dir)

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