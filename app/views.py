from django.shortcuts import render
from django.shortcuts import redirect, render

# Create your views here.
def home(request):
    context = {}
    return redirect("/swagger/")