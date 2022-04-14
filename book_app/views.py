from django.http import  HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic.list import ListView
import requests
from django.core import serializers
from .forms import AddOrEditForm, ImportForm
import datetime

from datetime import datetime

from .models import Book


def extract_ISBN(industryIdentifiers):
    for item in industryIdentifiers:
        if item["type"] == "ISBN_13":
            return item["identifier"]
    return "Brak danych"


def filter_by_query_strings(queryset, request):
    if request.GET.get("language"):
        queryset = queryset.filter(language=request.GET["language"])
    if request.GET.get("author"):
        queryset = queryset.filter(author__icontains=request.GET["author"])
    if request.GET.get("title"):
        queryset = queryset.filter(title__icontains=request.GET["title"])
    if request.GET.get("date_from"):
        queryset = queryset.filter(pub_date__gte=request.GET["date_from"])
    if request.GET.get("date_to"):
        queryset = queryset.filter(pub_date__lte=request.GET["date_to"])
    return queryset


class BookListView(ListView):

    model = Book
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()

        context["query"] = "&".join(
            [
                f"{key}={value}"
                for key, value in self.request.GET.items()
                if key != "page"
            ]
        )
        if self.request.GET.get("date_from") and self.request.GET.get("date_to"):
            if self.request.GET.get("date_from") > self.request.GET.get("date_to"):
                context[
                    "errors"
                ] = "Data początkowa musi być wcześniejsza niż data końcowa"
        return context

    def get_queryset(self):
        queryset = Book.objects.all().order_by("title")

        self.request.choices = set([x.language for x in queryset])
        queryset = filter_by_query_strings(queryset, self.request)
        return queryset

    class Meta:
        ordering = ["title"]



def book_edit_view(request, id):

    if request.method == "POST":
        form = AddOrEditForm(request.POST, instance=Book.objects.get(pk=id))

        if form.is_valid():
            form.save()
            return redirect("/")
       
    else:
        instance = Book.objects.get(pk=id)
        form = AddOrEditForm(
            instance=instance,
            initial={
                "pub_date": instance.pub_date.strftime(format="%Y-%m-%d")
                if instance.pub_date
                else ''
            },
        )
    return render(request, "book_app/book_edit.html", {"form": form})


def book_add_view(request):
    if request.method == "POST":
        form = AddOrEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = AddOrEditForm()
    return render(request, "book_app/book_edit.html", {"form": form})


def book_impoert_view(request):
    if request.method == "GET":
        form = ImportForm()

        query = request.GET.get("query", "")
        if query:
            request_data = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q={query}"
            )
            if request_data.status_code != 200:
                return render(
                    request,
                    "book_app/book_import.html",
                    {"form": form, "errors": "Przepraszamy, nie można pobrać wyników"},
                )
            request_data = request_data.json()
            if "items" not in request_data:
                return render(
                    request,
                    "book_app/book_import.html",
                    {"form": form, "errors": "Przepraszamy, nie znaleziono wyników"},
                )
            books = [
                item
                for item in request_data["items"]
                if item["id"]
                not in [x[0] for x in Book.objects.values_list("google_id")]
            ]
            object_list = [
                {
                    "title": book["volumeInfo"]["title"]
                    + " "
                    + book["volumeInfo"].get("subtitle", ""),
                    "cover_url": book["volumeInfo"]["imageLinks"]["thumbnail"]
                    if "imageLinks" in book["volumeInfo"]
                    else "",
                    "author": ", ".join(book["volumeInfo"]["authors"])
                    if "authors" in book["volumeInfo"]
                    else "Brak danych",
                    "pub_date": book["volumeInfo"]["publishedDate"]
                    if "publishedDate" in book["volumeInfo"]
                    else "Brak danych",
                    "isbn": extract_ISBN(book["volumeInfo"]["industryIdentifiers"])
                    if "industryIdentifiers" in book["volumeInfo"]
                    else "Brak danych",
                    "page_count": book["volumeInfo"]["pageCount"]
                    if "pageCount" in book["volumeInfo"]
                    else "Brak danych",
                    "language": book["volumeInfo"]["language"].upper()
                    if "language" in book["volumeInfo"]
                    else "Brak danych",
                    "google_id": book["id"] if "id" in book else "null",
                }
                for book in books
            ]

            return render(
                request,
                "book_app/book_import.html",
                {"form": form, "object_list": object_list},
            )
        else:
            return render(
                request, "book_app/book_import.html", {"form": form, "object_list": []}
            )


def book_import_to_DB(request, id):
    req = requests.get(f"https://www.googleapis.com/books/v1/volumes/{id}")
    if req.status_code != 200:
        return JsonResponse({"errors": "Przepraszamy, nie można pobrać wyników"})
    book = req.json()
    book = {
        "title": book["volumeInfo"]["title"]
        + " "
        + book["volumeInfo"].get("subtitle", ""),
        "cover_url": book["volumeInfo"]["imageLinks"]["thumbnail"]
        if "imageLinks" in book["volumeInfo"]
        else "",
        "author": ", ".join(book["volumeInfo"]["authors"])
        if "authors" in book["volumeInfo"]
        else "",
        "pub_date": book["volumeInfo"]["publishedDate"]
        if "publishedDate" in book["volumeInfo"]
        else "",
        "isbn": extract_ISBN(book["volumeInfo"]["industryIdentifiers"])
        if "industryIdentifiers" in book["volumeInfo"]
        else "",
        "page_count": book["volumeInfo"]["pageCount"]
        if "pageCount" in book["volumeInfo"]
        else 0,
        "language": book["volumeInfo"]["language"].upper()
        if "language" in book["volumeInfo"]
        else "Nieznany",
        "google_id": book["id"] if "id" in book else "null",
    }

    if book["pub_date"]:
        if len(book["pub_date"].split("-")) == 1:
            book["pub_date"] = datetime.strptime(book["pub_date"], "%Y").date()
        elif len(book["pub_date"].split("-")) == 2:
            book["pub_date"] = datetime.strptime(book["pub_date"], "%Y-%m").date()
        else:
            book["pub_date"] = datetime.strptime(book["pub_date"], "%Y-%m-%d").date()
    b = Book(**book)
    b.save()
    return redirect("/")


def delete(request, id):
    Book.objects.get(pk=id).delete()
    return redirect("/")


def api(request):
    books = Book.objects.all()
    data = filter_by_query_strings(books, request)
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )
