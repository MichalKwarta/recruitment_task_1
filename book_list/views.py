from django.shortcuts import redirect


def redirectView(request):
    return redirect('/books')