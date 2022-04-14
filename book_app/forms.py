from django import forms

from .models import Book

class AddOrEditForm(forms.ModelForm):
    title = forms.CharField(label='Tytuł')
    author = forms.CharField(label='Autor')
    pub_date = forms.DateField(label='Data publikacji',widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    isbn = forms.CharField(label='ISBN')
    page_count = forms.IntegerField(label='Liczba stron',min_value=1)
    cover_url = forms.URLField(label='URL okładki')
    language = forms.CharField(label='Język')

    
    class Meta:
        model=Book
        fields = ['title','author','pub_date','isbn','page_count','cover_url','language'] 
class ImportForm(forms.Form):
    query = forms.CharField(label='Wyszukaj',required=False)
    

      

    