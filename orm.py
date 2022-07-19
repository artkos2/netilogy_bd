
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import json

LOGIN = 'postgres'
PASS = 'postgres'
BD_NAME = 'postgres'

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40))

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="book")

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)


class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref="sale")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def load_from_json(path_file):
    with open(path_file, encoding="utf-8") as f:
            json_data = json.load(f)
            for record in json_data:
                model = {
                    'publisher': Publisher,
                    'shop': Shop,
                    'book': Book,
                    'stock': Stock,
                    'sale': Sale,
                }[record.get('model')]
                session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

def find_publisher(publ):
    subq = session.query(Stock).join(Book.stock).join(Book.publisher).filter(Publisher.name.like(publ)).subquery("id_shop")
    q = session.query(Shop).join(subq, Shop.id == subq.c.id_shop)
    for s in q.all():
        print(s.name)

DSN = 'postgresql://'+LOGIN+':'+PASS+'@localhost:5432/'+BD_NAME
engine = sq.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    load_from_json('files/test.json')
    publisher = input('Введите имя издателя')
    find_publisher(publisher)