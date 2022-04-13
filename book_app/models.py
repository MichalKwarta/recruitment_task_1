from email.policy import default
from django.db import models

# Create your models here.


# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=100)
    pub_date = models.DateField()
    isbn = models.CharField(max_length=17)
    page_count = models.PositiveSmallIntegerField()
    cover_url = models.URLField(max_length=200)
    language = models.CharField(max_length=3)

    def __str__(self):
        return self.title



