from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView


from .forms import AddOrEditForm



from .models import Book


class BookListView(ListView):

    model = Book
    paginate_by = 2  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        
        context['query'] = '&'.join([f"{key}={value}" for key, value in self.request.GET.items() if key!='page'])
        print(context['query'])
        if self.request.GET.get('date_from') and self.request.GET.get('date_to'):
            if (self.request.GET.get('date_from')>=self.request.GET.get('date_to')):
                context['errors'] = 'Data początkowa musi być wcześniejsza niż data końcowa'
        return context
        
    def get_queryset(self):
        queryset = Book.objects.all().order_by('title')
        
        self.request.choices = set([x.language for x in queryset])
        if self.request.GET.get('language'):
            queryset = queryset.filter(language=self.request.GET['language'])
        if self.request.GET.get('author'):
            queryset = queryset.filter(author__istartswith=self.request.GET['author'])
        if self.request.GET.get('title'):
            queryset = queryset.filter(title__istartswith=self.request.GET['title'])
        if self.request.GET.get('date_from'):
            queryset = queryset.filter(pub_date__gte=self.request.GET['date_from'])
        if self.request.GET.get('date_to'):
            queryset = queryset.filter(pub_date__lte=self.request.GET['date_to'])
        return queryset
    
    class Meta:
        ordering = ['title']




def BookEditView(request,pk):   

    if request.method == 'POST':
        form = AddOrEditForm(request.POST,instance=Book.objects.get(pk=pk))

        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
    else:
        instance = Book.objects.get(pk=pk)
        form = AddOrEditForm(instance=instance,initial={'pub_date':instance.pub_date.strftime(format='%Y-%m-%d')})
    return render(request, 'book_app/book_edit.html', {'form': form})
def BookAddView(request):
    if request.method == 'POST':
        form = AddOrEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = AddOrEditForm()
    return render(request, 'book_app/book_edit.html', {'form': form})
