from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # we'll use render for this when I find the doc...
    return render(request, 'camelot/index.html')
