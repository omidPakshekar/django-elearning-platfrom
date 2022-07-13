from django.shortcuts import render, get_list_or_404
from django.views.generic import ( ListView, DetailView,
     TemplateView, CreateView, UpdateView,DeleteView)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from students.forms import CourseEnrollForm
from django.urls import reverse_lazy, reverse

from .models import Course 

class CourseListView(ListView):
    model = Course 
    template_name = 'courses/course_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        if 'mine' in self.request.get_full_path():
               return Course.objects.filter(owner=self.request.user).only('title', 'photo')
        return Course.objects.only('title', 'photo')
    
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enroll_form"] = CourseEnrollForm(initial={'course' : self.object}) 
        return context

class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner = self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['category', 'title', 'slug', 'overview']
    success_url = reverse_lazy('courses:course-list')
    template_name = 'courses/manage/course_form.html'

class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

    
