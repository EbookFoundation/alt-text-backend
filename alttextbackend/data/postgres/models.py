from django.db import models

class Book(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    numImages = models.IntegerField(null=True, blank=True)
    coverExt = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.title
    
class Image(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    src = models.CharField(max_length=255)
    hash = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    alt = models.TextField(blank=True, null=True)
    originalAlt = models.TextField(blank=True, null=True)
    genAlt = models.TextField(blank=True, null=True)
    genImageCaption = models.TextField(blank=True, null=True)
    ocr = models.TextField(blank=True, null=True)
    beforeContext = models.TextField(blank=True, null=True)
    afterContext = models.TextField(blank=True, null=True)
    additionalContext = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'images'
        unique_together = ('book', 'src')

    def __str__(self):
        return f"Image {self.src} of Book {self.book.id}"