import uuid

try:
    from .config import Database
except ImportError:
    from config import Database

"""
BOOKS DATABASE ATTRIBUTES
    *id: str
    title: str
    size: str
    status: str
    numImages: int
    coverExt: str
"""


def createBookTable():
    db = Database()
    query = "CREATE TABLE books (id varchar(255) NOT NULL PRIMARY KEY, title varchar(255), size varchar(255), status varchar(255), numImages int, coverExt varchar(255));"
    db.sendQuery(query)
    db.commit()
    db.close()


def jsonifyBook(book: tuple):
    return {
        "id": book[0],
        "title": book[1],
        "size": book[2],
        "status": book[3],
        "numImages": book[4],
        "coverExt": book[5],
    }


def getBook(id: str):
    db = Database()
    query = "SELECT * FROM books WHERE id = %s"
    params = (id,)
    db.sendQuery(query, params)
    book = db.fetchOne()
    db.close()
    return book


def getBooks(titleQ: str = None, limit: int = None, skip: int = None):
    db = Database()
    params = []
    query = "SELECT * FROM books"

    if titleQ:
        lowerTitleQ = f"%{titleQ.lower()}%"
        query += " WHERE LOWER(title) LIKE %s"
        params.append(lowerTitleQ)

    if limit is not None:
        query += " LIMIT %s"
        params.append(limit)

    if skip is not None:
        query += " OFFSET %s"
        params.append(skip)

    db.sendQuery(query, params)
    books = db.fetchAll()
    db.close()
    return books


def addBook(
    title: str,
    size: str,
    numImages: int,
    id: str = None,
    status: str = "available",
    coverExt: str = None,
):
    if id == None:
        id = str(uuid.uuid4())

    db = Database()
    query = "INSERT INTO books (id, title, status, numimages, size, coverext) VALUES (%s, %s, %s, %s, %s, %s);"
    params = (id, title, status, numImages, size, coverExt)
    db.sendQuery(query, params)
    db.commit()
    db.close()
    return getBook(id)


def deleteBook(id: str):
    db = Database()
    query = "DELETE FROM books WHERE id = %s"
    params = (id,)
    db.sendQuery(query, params)
    db.commit()
    db.close()


def updateBook(id: str, title: str = None, status: str = None, coverExt: str = None):
    db = Database()

    if title or status or coverExt:
        params = []
        query = "UPDATE books SET"

        if title:
            query += " title = %s,"
            params.append(title)

        if status:
            query += " status = %s,"
            params.append(status)

        if coverExt:
            query += " coverext = %s,"
            params.append(coverExt)

        query = query[:-1]

        query += " WHERE id = %s"
        params.append(id)
        db.sendQuery(query, params)
        db.commit()

    db.close()
