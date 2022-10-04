from sqlalchemy import Column, TEXT, INT, VARCHAR, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class FileList(Base):
    __tablename__ = "file_list"
    id = Column(INT,primary_key=True,autoincrement=True)
    file_name = Column(VARCHAR(256))
    user = Column(VARCHAR(20))
    created_at = Column(TIMESTAMP)

    def __init__(
            self,
            id,
            file_name,
            user,
            created_at
    ):
        self.id = id
        self.file_name = file_name
        self.user = user
        self.created_at = created_at
    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
