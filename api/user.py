from fastapi import APIRouter, Depends, HTTPException
from utils import auth_user, get_user_from_header


from examples import user_example
from model import User, db



user_router = APIRouter()


@user_router.post("/create_user")
def create_user(item: schemas.RegisterUser = user_example,current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    if User.check_user_by_email(email=item.email):
        return HTTPException(status_code=400, detail=errors.ERR_MAIL_ALREADY_EXIST)
    if User.check_user_by_jmbg(jmbg=item.jmbg):
        return HTTPException(status_code=400, detail=errors.ERR_USER_JMBG_ALREADY_EXIST)

    try:
        user = User(
            email=item.email,
            password=item.password,
            name=item.name,
            role=item.role,
            jmbg=item.jmbg,
            phone=item.phone,
            address=item.address
        )
        db.add(user)
        db.commit()
        return user

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}