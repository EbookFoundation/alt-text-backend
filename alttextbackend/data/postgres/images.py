import sys
import os
import django


current_script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_script_path, '..', '..', '..')
sys.path.insert(0, os.path.abspath(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "alttextbackend.settings")
django.setup()

from alttextbackend.data.postgres.models import Image, Book


"""
IMAGE DATABASE ATTRIBUTES
    *bookid: str
    *src: str
    hash: str
    status: str
    alt: str
    originalAlt: str
    genAlt: str
    genImageCaption: str
    ocr: str
    beforeContext: str
    afterContext: str
    additionalContext: str
"""

def jsonifyImage(image: tuple):
    return {
        "bookid": image[0],
        "src": image[1],
        "hash": image[2],
        "status": image[3],
        "alt": image[4],
        "originalAlt": image[5],
        "genAlt": image[6],
        "genImageCaption": image[7],
        "ocr": image[8],
        "beforeContext": image[9],
        "afterContext": image[10],
        "additionalContext": image[11],
    }


def getImageByBook(bookid: str, src: str):
    book = Book.objects.get(id=bookid)
    image_tuple = Image.objects.filter(book=book, src=src).values_list(
        'book_id', 'src', 'hash', 'status', 'alt', 'originalAlt',
        'genAlt', 'genImageCaption', 'ocr', 'beforeContext', 
        'afterContext', 'additionalContext', named=False
    ).first()

    # Check if an image was found; if not, return None
    if image_tuple is None:
        return None

    return image_tuple


def getImagesByBook(bookid: str):
    book = Book.objects.get(id=bookid)
    images_tuples = Image.objects.filter(book=book).values_list(
        'book_id', 'src', 'hash', 'status', 'alt', 'originalAlt',
        'genAlt', 'genImageCaption', 'ocr', 'beforeContext', 
        'afterContext', 'additionalContext', named=False
    )

    return list(images_tuples)


def getImagesByHash(hash: str):
    images_tuples = Image.objects.filter(hash=hash).values_list(
        'book_id', 'src', 'hash', 'status', 'alt', 'originalAlt',
        'genAlt', 'genImageCaption', 'ocr', 'beforeContext', 
        'afterContext', 'additionalContext', named=False
    )

    return list(images_tuples)


def addImage(
    bookid: str,
    src: str,
    hash: str = None,
    status: str = "available",
    alt: str = "",
    originalAlt: str = None,
    genAlt: str = None,
    genImageCaption: str = None,
    ocr: str = None,
    beforeContext: str = None,
    afterContext: str = None,
    additionalContext: str = None,
):
    status = status if status in ["available", "processing"] else "available"

    # Truncate strings to their maximum allowed length based on the model's definitions
    alt = alt[:1000] if alt is not None else None
    originalAlt = originalAlt[:1000] if originalAlt is not None else None
    genAlt = genAlt[:1000] if genAlt is not None else None
    genImageCaption = genImageCaption[:1000] if genImageCaption is not None else None
    ocr = ocr[:1000] if ocr is not None else None
    beforeContext = beforeContext[:2000] if beforeContext is not None else None
    afterContext = afterContext[:2000] if afterContext is not None else None
    additionalContext = additionalContext[:1000] if additionalContext is not None else None

    book_instance = Book.objects.get(id=bookid)

    # Create and save the new Image instance
    new_image = Image.objects.create(
        book=book_instance,
        src=src,
        hash=hash,
        status=status,
        alt=alt,
        originalAlt=originalAlt,
        genAlt=genAlt,
        genImageCaption=genImageCaption,
        ocr=ocr,
        beforeContext=beforeContext,
        afterContext=afterContext,
        additionalContext=additionalContext,
    )

    return new_image


def deleteImage(bookid: str, src: str):
    book = Book.objects.get(id=bookid)
    Image.objects.filter(book=book, src=src).delete()


def updateImage(
    bookid: str,
    src: str,
    status: str = None,
    alt: str = None,
    genAlt: str = None,
    genImageCaption: str = None,
    ocr: str = None,
    beforeContext: str = None,
    afterContext: str = None,
    additionalContext: str = None,
):
    update_fields = {}
    if status is not None:
        update_fields['status'] = status
    if alt is not None:
        update_fields['alt'] = alt
    if genAlt is not None:
        update_fields['genAlt'] = genAlt
    if genImageCaption is not None:
        update_fields['genImageCaption'] = genImageCaption
    if ocr is not None:
        update_fields['ocr'] = ocr
    if beforeContext is not None:
        update_fields['beforeContext'] = beforeContext
    if afterContext is not None:
        update_fields['afterContext'] = afterContext
    if additionalContext is not None:
        update_fields['additionalContext'] = additionalContext

    # Only execute the update if there are fields to update
    if update_fields:
        book = Book.objects.get(id=bookid)
        Image.objects.filter(book=book, src=src).update(**update_fields)
