from django.db import models

class Book(models.Model):
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=50)

    def __str__(self):
        return self.book_name
