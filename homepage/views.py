from django.shortcuts import render
from courses.models import Course

def hompageView(request):
    object_list = Course.objects.all()
    return render(request, 'home/index.html', {'object_list' : object_list})