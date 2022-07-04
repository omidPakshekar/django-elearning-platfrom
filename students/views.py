from django.shortcuts import render
from .forms import CourseEnrollForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, DetailView, UpdateView, FormView)
from django.urls import reverse_lazy

class StudentEnrollCourseView(LoginRequiredMixin, CreateView):
    form_class = CourseEnrollForm
    course = None 

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('courses:course-list')

    








