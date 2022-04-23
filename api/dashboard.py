from fastapi import APIRouter, Depends, HTTPException
from utils import auth_user, get_user_from_header
from model import User, db, Posts, LikeUnlike, Comments
from fastapi_pagination import Page, paginate
import errors
import schemas

dashboard_router = APIRouter()


@dashboard_router.post("/create_post", status_code=200)
def create_post(item: schemas.CreatePost, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    try:
        post = Posts(
            user_id=current_user.id,
            post_content=item.post_content,
        )
        db.add(post)
        db.commit()
        return post

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@dashboard_router.get("/all_posts", status_code=200)
def all_posts(current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    return Posts.get_all_posts()


@dashboard_router.get("/all_posts/{posts_id}", response_model=Page, status_code=200)
def all_posts(post_id: int, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    # return Posts.get_all_posts()
    return paginate(Posts.get_posts_by_id(id=post_id))


@dashboard_router.post("/like_posts", status_code=200)
def like_post(post_id: int, type: LikeUnlike, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    post = Posts.get_posts_by_id(id=post_id)
    if not post:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    if type == 'Like':
        post.numbers_of_likes = post.numbers_of_likes + 1
    if type == 'Unlike':
        post.numbers_of_likes = post.numbers_of_likes - 1
        if post.numbers_of_likes < 0:
            return post.numbers_of_likes == 0
    db.add(post)
    db.commit()
    return post


@dashboard_router.patch("/delete_post", status_code=200)
def delete_post(post_id: int, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    post_del = Posts.get_by_id(id=post_id)
    if not post_del:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    post_del.deleted = True
    db.add(post_del)
    db.commit()

    return {}


@dashboard_router.post("/comment_posts", status_code=200)
def comment_post(post_id: int, item: schemas.Comments, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    post = Posts.get_by_id(id=post_id)
    if not post:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    try:
        comments = Comments(
            post_id=post_id,
            user_id=current_user.id,
            comment_content=item.comment_content

        )
        db.add(comments)
        db.commit()
        return comments

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@dashboard_router.post("/like_comment", status_code=200)
def like_comment(comments_id: int, type: LikeUnlike, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    comm = Comments.get_by_id(id=comments_id)
    if not comm:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    if type == 'Like':
        comm.numbers_of_likes = comm.numbers_of_likes + 1
    if type == 'Unlike':
        comm.numbers_of_likes = comm.numbers_of_likes - 1
        if comm.numbers_of_likes < 0:
            return comm.numbers_of_likes == 0
    db.add(comm)
    db.commit()
    return comm


@dashboard_router.patch("/delete_comment", status_code=200)
def delete_comment(comm_id: int, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['users'])
    comm_del = Comments.get_by_id(id=comm_id)
    if not comm_del:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    comm_del.deleted = True
    db.add(comm_del)
    db.commit()

    return {}
