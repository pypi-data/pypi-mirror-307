from typing import Optional, List

from poetry_fastapi_demo.models import User

user_list = [
    User(
        id=1,
        name="Chris",
        email="chris@gmail.com",
        password="pso3sd5xv",
        role="admin"
    ),
    User(
        id=2,
        name="Jon",
        email="jon@gmail.com",
        password="rthdfwe5sdf",
        role="user"
    ),
    User(
        id=3,
        name="Arya",
        email="arya@gmail.com",
        password="ndddrwe42",
        role="user"
    )

]


class UserTable:

    def get_all_users(self) -> List[User]:
        return user_list

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        for user in user_list:
            if user.id == user_id:
                return user
        return None

    def update_user(self, user: User) -> bool:
        for u in user_list:
            if u.id == user.id:
                u.name = user.name
                u.email = user.email
                u.password = user.password
                u.role = user.role
                return True
        return False

    def delete_user(self, user_id: int) -> bool:
        for i, u in enumerate(user_list):
            if u.id == user_id:
                del user_list[i]
                return True
        return False

    def add_user(self, user: User) -> bool:
        for u in user_list:
            if u.id == user.id:
                return False
        user_list.append(user)
        return True


user_table = UserTable()
