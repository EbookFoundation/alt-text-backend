import os
import threading

import bs4
from alttext import alttext
from alttext.descengine.bliplocal import BlipLocal
from alttext.descengine.replicateapi import ReplicateAPI
from alttext.ocrengine.tesseract import Tesseract
from alttext.langengine.openaiapi import OpenAIAPI
from alttext.langengine.privategpt import PrivateGPT
from django.core.files.storage import default_storage

from .postgres import books, images

# from alttext.descengine.googlevertexapi import GoogleVertexAPI


def createAnalyzer():
    descEngine = None
    match os.environ["DESC_ENGINE"].lower():
        case "replicateapi":
            descEngine = ReplicateAPI(os.environ["REPLICATE_KEY"])
        case "bliplocal":
            descEngine = BlipLocal(os.environ["BLIPLOCAL_DIR"])
        # case "googlevertexapi":
        #     descEngine = GoogleVertexAPI(os.environ["VERTEX_PROJECT_ID"], os.environ["VERTEX_LOCATION"], os.environ["VERTEX_GAC_PATH"])
        case _:
            raise ValueError("Invalid description engine")

    ocrEngine = None
    match os.environ["OCR_ENGINE"].lower():
        case "tesseract":
            ocrEngine = Tesseract()
        case _:
            raise ValueError("Invalid OCR engine")

    langEngine = None
    match os.environ["LANG_ENGINE"].lower():
        case "privategpt":
            langEngine = PrivateGPT(os.environ["PRIVATEGPT_HOST"])
        case "openaiapi":
            langEngine = OpenAIAPI(
                os.environ["OPENAI_API_KEY"], os.environ["OPENAI_MODEL"]
            )
        case _:
            raise ValueError("Invalid language engine")

    options = {
        "withContext": bool(int(os.environ["ALT_WITH_CONTEXT"])),
        "withHash": bool(int(os.environ["ALT_WITH_HASH"])),
        "multiThreaded": bool(int(os.environ["ALT_MULTITHREADED"])),
        "version": int(os.environ["ALT_VERSION"]),
    }

    return alttext.AltTextHTML(descEngine, ocrEngine, langEngine, options)


def findHTML(path: str):
    html_file = None
    for root, _, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".html"):
                html_file = default_storage.path(os.path.join(root, file_name))
                break
        if html_file:
            break
    return html_file


def getSize(path: str):
    size = 0
    for path, _, files in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    return size


def analyzeImageV2(alt: alttext.AltTextHTML, img: bs4.element.Tag, bookid: str):
    imgRecord = images.jsonifyImage(images.getImageByBook(bookid, img["src"]))
    context = [imgRecord["beforeContext"], imgRecord["afterContext"]]
    imgData = alt.getImgData(img["src"])
    desc = alt.genDesc(imgData, img["src"], context)
    chars = alt.genChars(imgData, img["src"]).strip()
    thisAlt = alt.langEngine.refineAlt(desc, chars, context, None)

    images.updateImage(
        bookid,
        img["src"],
        status="available",
        genAlt=thisAlt,
        genImageCaption=desc,
        ocr=chars,
        beforeContext=context[0],
        afterContext=context[1],
    )

    return images.jsonifyImage(images.getImageByBook(bookid, img["src"]))


def analyzeSingularImageV2(alt: alttext.AltTextHTML, img: bs4.element.Tag, bookid: str):
    books.updateBook(bookid, status="processing")
    images.updateImage(
        bookid,
        img["src"],
        status="processing",
    )
    analyzeImageV2(alt, img, bookid)
    books.updateBook(bookid, status="available")
    return images.jsonifyImage(images.getImageByBook(bookid, img["src"]))


def analyzeImagesV2(alt: alttext.AltTextHTML, imgs: list[bs4.element.Tag], bookid: str):
    books.updateBook(bookid, status="processing")
    for img in imgs:
        images.updateImage(
            bookid,
            img["src"],
            status="processing",
        )

    if bool(int(os.environ["ALT_MULTITHREADED"])):
        # TODO: TEST WITH OPENAI API
        threads = []
        for img in imgs:
            thread = threading.Thread(target=analyzeImageV2, args=(alt, img, bookid))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    else:
        for img in imgs:
            analyzeImageV2(alt, img, bookid)

    books.updateBook(bookid, status="available")
    return books.jsonifyBook(books.getBook(bookid))
