from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'main/index.html')


def details(request):
    return render(request, 'main/details.html')
