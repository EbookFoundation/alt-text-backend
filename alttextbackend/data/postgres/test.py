import dotenv
from books import addBook, getBooks, getBook, updateBook, deleteBook
from images import (
    addImage,
    getImagesByBook,
    getImageByBook,
    getImagesByHash,
    updateImage,
    deleteImage,
)
from config import Database
import os
import django
import sys

dotenv.load_dotenv()


#project_root = "/SeniorD/alt-text-backend"
#sys.path.insert(0, project_root)

# Set the Django settings module
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alttextbackend.settings')

# Prepare the Django project for use
#django.setup()


"""
createBookTable = "CREATE TABLE books (id varchar(255) NOT NULL PRIMARY KEY, title varchar(255), size varchar(255), status varchar(255), numImages int, coverExt varchar(255));"
createImageTable = "CREATE TABLE images (bookid varchar(255) NOT NULL, src varchar(255) NOT NULL, hash varchar(255), status varchar(255), alt varchar(255), originalAlt varchar(255), genAlt varchar(255), genImageCaption varchar(255), ocr varchar(255), beforeContext varchar(255), afterContext varchar(255), additionalContext varchar(255), CONSTRAINT PK_Image PRIMARY KEY (bookid, src), FOREIGN KEY (bookid) REFERENCES books(id) ON DELETE CASCADE);"
"""

# db.sendQuery("SELECT * FROM books")
# print(db.fetchOne())

#addBook(title="Harry Potter", size="300kb", numImages=25)
"""
addBook(title="Harry Potter", size="300kb", numImages=25)
addBook(title="Harraoeu", size="300kb", numImages=25)
addBook(title="Hartter", size="300kb", numImages=25)
"""

#print(getBooks())

#deleteBook('43198a6e-73ad-4e57-a2df-a7c9c7f8ce9a')

"""
addImage(
    bookid="845e7e66-860c-4df1-b64e-82c805c5cc3c",
    src="sampleSrcMEOW2222",
    hash="brown",
    status="available",
    genAlt="yeahhhh"
)
"""

print(getImageByBook(bookid="845e7e66-860c-4df1-b64e-82c805c5cc3c", src="sampleSrcMEOW"))

#print(getBook("845e7e66-860c-4df1-b64e-82c805c5cc3c"))

#print(getImagesByBook("845e7e66-860c-4df1-b64e-82c805c5cc3c"))

#print(getImagesByHash("brown"))
"""
updateImage(
    bookid="845e7e66-860c-4df1-b64e-82c805c5cc3c",
    src="sampleSrcMEOW",
    status="bruh2234234",
    beforeContext="before context be like",
)
"""

#deleteImage(bookid="845e7e66-860c-4df1-b64e-82c805c5cc3c", src="sampleSrcMEOW2222")

#updateBook(id="845e7e66-860c-4df1-b64e-82c805c5cc3c", coverExt="your mother")
#print(getBooks())

db = Database()
# db.sendQuery("SELECT * FROM images;")
# print(db.fetchAll())
db.close()
