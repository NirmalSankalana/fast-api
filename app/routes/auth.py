from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database
from ..schemas import user_schema
from ..models import User
from ..utils.hash_password import verify_password
from .. import oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=user_schema.Token)
def login(user_credentials: user_schema.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid user credentials")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user credentials")
    access_token = oauth2.create_access_token(data={'user_id': user.id})
    return {"access_token": access_token, "token_type":'bearer'}
