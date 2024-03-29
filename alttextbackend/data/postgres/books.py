import uuid
import os
import django
import sys


current_script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_script_path, '..', '..', '..')
sys.path.insert(0, os.path.abspath(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "alttextbackend.settings")
django.setup()

from alttextbackend.data.postgres.models import Book


"""
BOOKS DATABASE ATTRIBUTES
    *id: str
    title: str
    size: str
    status: str
    numImages: int
    coverExt: str
"""

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
    book_tuple = Book.objects.filter(id=id).values_list(
        'id', 'title', 'size', 'status', 'numImages', 'coverExt', named=False
    ).first()

    # Check if a book was found; if not, return None
    if book_tuple is None:
        return None

    return book_tuple


def getBooks(titleQ: str = None, limit: int = None, skip: int = None):
    books_query = Book.objects.all()
    
    # Filter by title if a title query is provided
    if titleQ:
        books_query = books_query.filter(title__icontains=titleQ)
    
    # Apply limit and skip (offset) if provided
    if skip is not None:
        books_query = books_query[skip:]  # Skip the first `skip` records
    if limit is not None:
        books_query = books_query[:limit]  # Take `limit` records from the query set
    
    # Execute the query and fetch the results
    books = books_query.values_list('id', 'title', 'size', 'status', 'numImages', 'coverExt', flat=False)
    
    return list(books)


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

    newBook = Book(
        id=id,
        title=title,
        size=size,
        numImages=numImages,
        status=status,
        coverExt=coverExt
    )
    newBook.save()
    return getBook(id)


def deleteBook(id: str):
    myBook = Book.objects.get(id=id)
    myBook.delete()

def updateBook(id: str, title: str = None, status: str = None, coverExt: str = None):
    update_fields = {}
    if title is not None:
        update_fields['title'] = title
    if status is not None:
        update_fields['status'] = status
    if coverExt is not None:
        update_fields['coverExt'] = coverExt

    if update_fields:
        Book.objects.filter(id=id).update(**update_fields)
