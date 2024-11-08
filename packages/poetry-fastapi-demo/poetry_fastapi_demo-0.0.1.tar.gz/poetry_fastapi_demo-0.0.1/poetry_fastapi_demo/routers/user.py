import logging

from fastapi import APIRouter

from poetry_fastapi_demo.models import User
from poetry_fastapi_demo.tables import user_table

log = logging.getLogger(__name__)
router = APIRouter()


@router.get("")
def get_all_users():
    return user_table.get_all_users()


@router.get("/{user_id}")
def get_user(user_id: int):
    return user_table.get_user_by_id(user_id)


@router.post("")
def create_user(user: User):
    log.info(f"Creating user: {user}")
    return user_table.add_user(user)


@router.delete("/{user_id}")
def delete_user(user_id: int):
    log.warning(f"Deleting user with id: {user_id}")
    return user_table.delete_user(user_id)


@router.put("")
def update_user(user: User):
    log.warning(f"Updating user: {user}")
    return user_table.update_user(user)
