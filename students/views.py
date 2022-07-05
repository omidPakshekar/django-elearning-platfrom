from msilib.schema import ListView
from webbrowser import get
from django.shortcuts import render
from .forms import CourseEnrollForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, DetailView, UpdateView, ListView, FormView)
from django.urls import reverse_lazy

from courses.models import Course


class StudentQueryMixin(object):
    def get_queryset(self):
        qs = super(StudentQueryMixin, self).get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    form_class = CourseEnrollForm
    course = None 

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:course-list')

class StudentCourseListView(LoginRequiredMixin,StudentQueryMixin,  ListView):
    model = Course 
    template_name = 'students/student_course_list.html'

    

class StudentCourseDetailView(LoginRequiredMixin, StudentQueryMixin, DetailView):
    model = Course 
    template_name = "students/student_course_detail.html"

    
