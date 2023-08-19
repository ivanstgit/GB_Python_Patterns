from typing import List, Optional
from my_simple_app.core.db import (
    DbCommitException,
    DbDeleteException,
    DbUpdateException,
    RecordNotFoundException,
)
from my_simple_app.core.models import Student


class DBMapper:
    def __init__(self, connection, tablename):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = tablename

    def all(self):
        statement = f"SELECT * from {self.tablename}"
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def get_by_id(self, id):
        statement = f"SELECT * FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            raise RecordNotFoundException(f"record with id={id} not found")

    def get_by_name(self, name):
        statement = f"SELECT * FROM {self.tablename} WHERE name = ?"
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            raise RecordNotFoundException(f"record with name={name} not found")

    def insert(self, obj):
        raise NotImplementedError

    def update(self, obj):
        raise NotImplementedError

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class StudentMapper(DBMapper):
    def __init__(self, connection):
        super().__init__(connection, "student")

    def all(self) -> List[Student]:
        result = []
        rows = super().all()
        for item in rows:
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def get_by_id(self, id) -> Optional[Student]:
        result = super().get_by_id(id)
        if result:
            id, name = result
            res = Student(name)
            res.id = id
            return res
        return None

    def get_by_name(self, name) -> Optional[Student]:
        result = super().get_by_name(name)
        if result:
            id, name = result
            res = Student(name)
            res.id = id
            return res
        return None

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        "student": StudentMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj, connection):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        raise NotImplementedError

    @staticmethod
    def get_current_mapper(name, connection):
        return MapperRegistry.mappers[name](connection)
