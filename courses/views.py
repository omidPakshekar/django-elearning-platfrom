from django.shortcuts import render, get_list_or_404
from django.views.generic import ( ListView, DetailView,
                    TemplateView, CreateView, UpdateView,DeleteView)

from students.forms import CourseEnrollForm


from .models import Course 

class CourseListView(ListView):
    model = Course 
    template_name = 'courses/course_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Course.objects.only('title', 'photo')
    
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enroll_form"] = CourseEnrollForm(initial={'course' : self.object}) 
        return context
    
