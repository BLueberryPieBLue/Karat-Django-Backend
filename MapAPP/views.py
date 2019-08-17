from django.shortcuts import render

# Create your views here.
from Karat.settings import RequestHost


def SchoolHistoryMuseum(request):
    return render(request, 'test.html',{"RequestHost":RequestHost})