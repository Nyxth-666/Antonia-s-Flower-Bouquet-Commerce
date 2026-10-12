from django.shortcuts import render

def occasions_page(request):
    return render(request, "occasions/occasions.html")