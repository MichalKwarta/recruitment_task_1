from django import forms
from pkg_resources import require

from .models import Book

class AddOrEditForm(forms.ModelForm):
    title = forms.CharField(label='Tytuł')
    author = forms.CharField(label='Autor')
    pub_date = forms.DateField(label='Data publikacji',widget=forms.widgets.DateInput(attrs={'type': 'date'}),required=False)
    isbn = forms.CharField(label='ISBN',required=False)
    page_count = forms.IntegerField(label='Liczba stron',min_value=1,required=False)
    cover_url = forms.URLField(label='URL okładki',required=False)
    language = forms.CharField(label='Język',required=False)

    def clean(self):
        super().clean()
        if self.cleaned_data.get('language')=='':
            self.cleaned_data['language'] = None
        
    class Meta:
        model=Book
        fields = ['title','author','pub_date','isbn','page_count','cover_url','language'] 
class ImportForm(forms.Form):
    query = forms.CharField(label='Wyszukaj',required=False)
    

      

    