from fastapi import Depends,HTTPException,status,APIRouter
#from fastapi.param_functions import Depends,Depends,
from .. import  models,schemas
from ..database import get_db

from sqlalchemy.orm import Session
from .. import utils


router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):


	#check if email already registered
	email = db.query(models.User).filter(models.User.email==user.email).first()
	if email:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email Already Registered")
	
	hashed_password  = utils.hash(user.password)
	user.password = hashed_password

	new_user = models.User(**user.dict())
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user 

	

@router.get("/{id}",response_model=schemas.UserOut)
def get_users(id:int, db:Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.id==id).first()

	if not user:
		raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=
		f" User with id  {id}  not Found ") 

	return user