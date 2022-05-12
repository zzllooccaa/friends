from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from utils import auth_user, get_user_from_header
from starlette.requests import Request
from model import User, db
import errors
import schemas
from uuid import uuid4
from background import get_api
from validate_email_address import validate_email

user_router = APIRouter()


@user_router.post("/register")
async def register(item: schemas.RegisterUser, request: Request, background_task: BackgroundTasks):
    '''izvlaci ip od onog ko se registruje'''
    ip = request.client.host
    print(ip)
    check_email = item.email
    validate_email(check_email, verify=True)
    if not validate_email:
        return HTTPException(status_code=400, detail=errors.ERR_MAIL_NOT_EXIST)
    # save_mail = item.email
    if User.get_user_by_email(email=item.email):
        return HTTPException(status_code=400, detail=errors.ERR_MAIL_ALREADY_EXIST)

    try:
        user = User(
            email=item.email,
            password=item.password,
            name=item.name,
            phone=item.phone,
            address=item.address,
            date_of_birth=item.date_of_birth,
        )
        db.add(user)
        db.commit()
        background_task.add_task(get_api)
        print("User is register, backgroundtask will start in 15 sec")
        return user

    except Exception as e:
        db.rollback()
        db.refresh()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


def _update_user_session(user, session_id):
    """Update user session_id"""
    user.session_id = session_id
    db.add(user)
    db.commit()
    return {'message:' 'Welcome to  our social network ' \
            + user.name + ' your user-id is ' + str(user.id)} \
        , user.session_id


###############
# LOGIN USER #
###############


@user_router.post("/login")
async def login(item: schemas.UserLogin):
    user = User.get_user_by_email_and_password(email=item.email, password=item.password)
    if not user:
        raise HTTPException(status_code=400, detail=errors.WRONG_CREDENTIALS)

    return _update_user_session(user=user, session_id='{}:{}'.format(user.id, uuid4()))


###############
# LOGOUT USER #
###############

@user_router.put('/logout')
def del_session(current_user: User = Depends(get_user_from_header)):
    _update_user_session(user=current_user, session_id=None)
    return {}


###############
# BLOCK USER  #
###############

@user_router.patch("/block/{user_id}", status_code=200)
def block_user(user_id: int, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    user = User.get_by_id(id=user_id)
    if not user:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    user.block = True
    db.add(user)
    db.commit()

    return {}


###################
# DELETE ACCOUNT  #
###################

@user_router.patch("/{user_id}", status_code=200)
def delete_account(user_id: int, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    user_num = User.get_by_id(id=user_id)
    if not user_num:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    user_num.deleted = True
    db.add(user_num)
    db.commit()

    return {}


@user_router.patch("/turnoff_account", status_code=200)
def turnoff_account(current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    current_user.deleted = True
    db.add(current_user)
    db.commit()

    return {}


@user_router.patch("/rollback_account", status_code=200)
def rollback_account(current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    current_user.deleted = False
    db.add(current_user)
    db.commit()

    return {}


########################
# CHANGE USER PASSWORD #
########################


@user_router.post("/change_password", status_code=200)
def change_password(user_pass: schemas.ChangePassword, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    if user_pass.password != user_pass.retype_password:
        return HTTPException(status_code=400, detail=errors.ERR_PASSWORD_RETYPE)
    auth_user.password = user_pass.password
    db.add(auth_user)
    db.commit()
    return auth_user


################
# UPDATE USER  #
################

@user_router.patch("/user/{user_id}", status_code=200)
def edit(user_id: int, user_data: schemas.UserUpdate, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    user_db = User.get_by_id(id=user_id)
    if not user_db:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    user_data_dic = user_data.dict(exclude_none=True)
    check_email = user_data_dic['email']
    is_valid = validate_email(check_email, verify=True)
    if not is_valid:
        return HTTPException(status_code=400, detail=errors.ERR_MAIL_NOT_EXIST)
    if user_data_dic['email'] == User.email:
        return HTTPException(status_code=400, detail=errors.ERR_MAIL_ALREADY_EXIST)
    User.edit_user(user_id=user_id, user_data=user_data_dic)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db
