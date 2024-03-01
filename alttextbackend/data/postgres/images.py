try:
    from .config import Database
except ImportError:
    from config import Database

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


def createImageTable():
    db = Database()
    query = "CREATE TABLE images (bookid varchar(255) NOT NULL, src varchar(255) NOT NULL, hash varchar(255), status varchar(255), alt varchar(1000), originalAlt varchar(1000), genAlt varchar(1000), genImageCaption varchar(1000), ocr varchar(1000), beforeContext varchar(2000), afterContext varchar(2000), additionalContext varchar(1000), CONSTRAINT PK_Image PRIMARY KEY (bookid, src), FOREIGN KEY (bookid) REFERENCES books(id) ON DELETE CASCADE);"
    db.sendQuery(query)
    db.commit()
    db.close()


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
    db = Database()
    query = "SELECT * FROM images WHERE bookid = %s AND src = %s"
    params = (bookid, src)
    db.sendQuery(query, params)
    image = db.fetchOne()
    db.close
    return image


def getImagesByBook(bookid: str):
    db = Database()
    query = "SELECT * FROM images WHERE bookid = %s"
    params = (bookid,)
    db.sendQuery(query, params)
    images = db.fetchAll()
    db.close()
    return images


def getImagesByHash(hash: str):
    db = Database()
    query = "SELECT * FROM images WHERE hash = %s"
    params = (hash,)
    db.sendQuery(query, params)
    images = db.fetchAll()
    db.close()
    return images


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
    db = Database()
    query = "INSERT INTO images (bookid, src, hash, status, alt, originalalt, genalt, genimagecaption, ocr, beforecontext, aftercontext, additionalcontext) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    if status != "available" and status != "processing":
        status = "available"
    if alt is not None:
        alt = alt[:1000]
    if originalAlt is not None:
        originalAlt = originalAlt[:1000]
    if genAlt is not None:
        genAlt = genAlt[:1000]
    if genImageCaption is not None:
        genImageCaption = genImageCaption[:1000]
    if ocr is not None:
        ocr = ocr[:1000]
    if beforeContext is not None:
        beforeContext = beforeContext[:2000]
    if afterContext is not None:
        afterContext = afterContext[:2000]
    if additionalContext is not None:
        additionalContext = additionalContext[:1000]
    params = (
        bookid,
        src,
        hash,
        status,
        alt,
        originalAlt,
        genAlt,
        genImageCaption,
        ocr,
        beforeContext,
        afterContext,
        additionalContext,
    )
    db.sendQuery(query, params)
    db.commit()
    db.close()
    return getImageByBook(bookid, src)


def deleteImage(bookid: str, src: str):
    db = Database()
    query = "DELETE FROM images WHERE bookid = %s AND src = %s;"
    params = (bookid, src)
    db.sendQuery(query, params)
    db.commit()
    db.close()


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
    db = Database()

    if (
        status
        or alt
        or genAlt
        or genImageCaption
        or ocr
        or beforeContext
        or afterContext
        or additionalContext
    ):
        params = []
        query = "UPDATE images SET"

        if status:
            query += " status = %s,"
            params.append(status)

        if alt:
            query += " alt = %s,"
            params.append(alt)

        if genAlt:
            query += " genalt = %s,"
            params.append(genAlt)

        if genImageCaption:
            query += " genimagecaption = %s,"
            params.append(genImageCaption)

        if ocr:
            query += " ocr = %s,"
            params.append(ocr)

        if beforeContext:
            query += " beforecontext = %s,"
            params.append(beforeContext)

        if afterContext:
            query += " aftercontext = %s,"
            params.append(afterContext)

        if additionalContext:
            query += " additionalcontext = %s,"
            params.append(additionalContext)

        query = query[:-1]

        query += " WHERE bookid = %s AND src = %s"
        params.append(bookid)
        params.append(src)
        db.sendQuery(query, params)
        db.commit()

    db.close()
