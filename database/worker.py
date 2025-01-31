from sqlalchemy import create_engine, insert, select

from database.creator import UsersTable


class UserWorker:
    def __init__(self, database_path: str):
        database_url = "sqlite:///" + database_path
        engine = create_engine(database_url)
        self.__connect = engine.connect()

    def add_user(self, user_id: int, api_key: str):
        request = insert(UsersTable).values(id=user_id, api_key=api_key)
        self.__connect.execute(request)
        self.__connect.commit()

    def is_user(self, user_id: int) -> bool:
        response = self.__connect.execute(select(UsersTable).where(UsersTable.id == user_id)).all()
        return len(response) == 1

    def get_api_key(self, user_id: int) -> str:
        response = self.__connect.execute(select(UsersTable.api_key).where(UsersTable.id == user_id)).fetchone()
        return response[0]