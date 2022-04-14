
from django.db import models
from django.core.validators import MinLengthValidator,RegexValidator
# Create your models here.


# Create your models here.
class Book(models.Model):
    google_id = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    pub_date = models.DateField(blank=True,null=True)
    isbn = models.CharField(max_length=13,validators=[MinLengthValidator(13),RegexValidator(regex='^[0-9]*$',message='Podaj numer ISBN składający się z cyfr bez znaków')],blank=True, null=True)
    page_count = models.PositiveSmallIntegerField(blank=True,null=True)
    cover_url = models.URLField(max_length=500,blank=True,null=True)
    language = models.CharField(max_length=3,blank=True,null=True)
    def __str__(self):
        return self.title



