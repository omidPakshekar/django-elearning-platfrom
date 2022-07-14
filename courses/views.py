from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.views.generic import ( ListView, DetailView,
     TemplateView, CreateView, UpdateView,DeleteView)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from students.forms import CourseEnrollForm
from django.urls import reverse_lazy, reverse
from django.views import View
from .models import Course, Module

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
        print('form=',form)
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['category', 'title', 'slug', 'photo', 'overview']
    success_url = reverse_lazy('courses:course-list')
    template_name = 'courses/manage/course_form.html'

class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    permission_required = 'courses.delete_course'
    success_url = reverse_lazy('courses:course-list')

class CourseModuleUpdate(PermissionRequiredMixin, OwnerCourseMixin):
    
    def dispatch(self, request, pk, *args, **kwargs):
        """ 
            befour calling get(or post) method we assign our current
            model that want to work on
        """
        # self.cour
        return super(CourseModuleUpdate, self).dispatch(request, pk, *args, **kwargs)

class CourseModuleListView(View):
    course = None
    template_name = 'courses/manage/module_list.html'

    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleListView, self).dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"object" : self.course})