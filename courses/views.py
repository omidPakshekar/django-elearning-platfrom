from django.shortcuts import render, get_list_or_404
from django.views.generic import ( ListView, DetailView,
                    TemplateView, CreateView, UpdateView,DeleteView)


from .models import Course 

class CourseListView(ListView):
    model = Course 
    template_name = 'courses/course_list.html'
    context_object_name = 'object_list'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
  
