from django.shortcuts import render

# Create your views here.

def hompageView(request):
    return render(request, 'home/index.html', {})