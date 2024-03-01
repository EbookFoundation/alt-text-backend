import dotenv
from books import addBook, getBooks, getBook, updateBook
from images import (
    addImage,
    getImagesByBook,
    getImageByBook,
    getImagesByHash,
    updateImage,
)
from config import Database

dotenv.load_dotenv()

"""
createBookTable = "CREATE TABLE books (id varchar(255) NOT NULL PRIMARY KEY, title varchar(255), size varchar(255), status varchar(255), numImages int, coverExt varchar(255));"
createImageTable = "CREATE TABLE images (bookid varchar(255) NOT NULL, src varchar(255) NOT NULL, hash varchar(255), status varchar(255), alt varchar(255), originalAlt varchar(255), genAlt varchar(255), genImageCaption varchar(255), ocr varchar(255), beforeContext varchar(255), afterContext varchar(255), additionalContext varchar(255), CONSTRAINT PK_Image PRIMARY KEY (bookid, src), FOREIGN KEY (bookid) REFERENCES books(id) ON DELETE CASCADE);"
"""

# db.sendQuery("SELECT * FROM books")
# print(db.fetchOne())

# addBook(title="Harry Potter", size="300kb", numImages=25)
"""
addBook(title="Harry Potter", size="300kb", numImages=25)
addBook(title="Harraoeu", size="300kb", numImages=25)
addBook(title="Hartter", size="300kb", numImages=25)
"""

# getBooks(titleQ="Harry Potter", limit=1, skip=2)

"""
addImage(
    bookid="f1ac43cc-9f6d-4dc8-ac4f-aea0c4af5198",
    src="sampleSrcMEOW",
    hash="brown",
    status="available",
)
"""

# getImagesByBook("fa47d830-586a-485f-a579-67b33fd3eae3")

# print(getImagesByHash("brown"))

updateImage(
    bookid="f1ac43cc-9f6d-4dc8-ac4f-aea0c4af5198",
    src="sampleSrcMEOW",
    status="bruh2",
    beforeContext="before context be like",
)


# updateBook(id="72950", title="Test Title Two", status="available")

db = Database()
# db.sendQuery("SELECT * FROM images;")
# print(db.fetchAll())
db.close()
