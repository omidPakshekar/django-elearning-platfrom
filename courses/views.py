from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.views.generic import ( ListView, DetailView,
     TemplateView, CreateView, UpdateView,DeleteView)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from students.forms import CourseEnrollForm
from django.urls import reverse_lazy, reverse
from django.views import View
from django.apps import apps
from .models import Content, Course, Module
import logging

logger = logging.getLogger(__name__)

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


class CourseModuleListView(View):
    course = None
    template_name = 'courses/manage/module_list.html'
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleListView, self).dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"object" : self.course})



class ModuleObjectMixin(object):
    def get_object(self):
        if "content_id" in self.kwargs:
            return Content.objects.get(id=int(self.kwargs['content_id']))
        if 'module_id' in self.kwargs:
            return Module.objects.get(id=int(self.kwargs['module_id']))
        return super(ModuleObjectMixin, self).get_queryset()

class CourseModuleDeleteView(ModuleObjectMixin, DeleteView, PermissionRequiredMixin):
    model = Module
    permission_required = 'modules.delete_module'

    def get_success_url(self):
        return reverse('courses:course-module-list', kwargs={'pk': self.kwargs['pk']})

class CourseModuleEditMixin(object):
    model = Module
    fields = [ 'title', 'description']
    template_name='courses/manage/module_update.html'
    def get_success_url(self):
        return reverse('courses:course-module-list', kwargs={'pk': self.kwargs['pk']})
    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=int(self.kwargs["pk"]))
        logger.debug('add course to form')
        return super(CourseModuleEditMixin, self).form_valid(form)


class CourseModuleUpdateView(ModuleObjectMixin, CourseModuleEditMixin, UpdateView, PermissionRequiredMixin):
    permission_required = 'modules.change_module'


class CourseModuleCreateView(ModuleObjectMixin, CourseModuleEditMixin, CreateView, PermissionRequiredMixin):
    permission_required = 'modules.add_module'

class CourseModuleDetailView(LoginRequiredMixin, OwnerMixin, DetailView):
    model = Course 
    template_name = "courses/manage/course_module_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get current object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.first()
        return context


class ModuleContentDeleteView(PermissionRequiredMixin, ModuleObjectMixin, DeleteView):
    model = Content
    permission_required = 'contents.delete_content'
    
    def post(self, request, *args, **kwargs):
        logger.debug(type(self.get_object().item  ))
        self.get_object().item.delete()
        return super(ModuleContentDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('courses:course-module', kwargs={'pk': self.kwargs['pk'], "module_id" : self.kwargs['module_id']})
"""
    manage content craete and update content (text, file, video, image)

"""
class ContentMixin(object):
    def get_success_url(self):
        return reverse('courses:course-module', kwargs={'pk': self.kwargs['pk'], "module_id" : self.kwargs['module_id']})
    
    def get_model(self, model_name):
        if model_name == 'text':
            self.fields.append('title')
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_fields(self, model):
        fields_ = ['id', 'pk', 'title','owner',  'updated_time', 'created_time']
        for i in model._meta.fields:
            if i.name not in fields_ :
                self.fields.append(i.name)

    def get_object(self):
        return self.model.objects.get(id=Content.objects.get(id=int(self.kwargs['content_id'])).object_id)



class ModuleContentUpdateView(PermissionRequiredMixin, ContentMixin, UpdateView):
    model = None
    fields = []
    template_name='courses/manage/update_create_content.html'
    permission_required = 'contents.change_content'
    
    def dispatch(self, request, module_id, content_id, pk):
        content = Content.objects.get(pk=content_id).item
        logger.debug(content._meta.model_name)
        model_ = self.get_model(content._meta.model_name)
        self.get_fields(model_)
        logger.debug(self.fields)
        self.model = model_   
        return super(ModuleContentUpdateView, self).dispatch(request, module_id, content_id, pk)

class ModuleContentCreateView(PermissionRequiredMixin, ContentMixin, CreateView):
    model = None
    fields = []
    module = None
    template_name='courses/manage/update_create_content.html'
    permission_required = 'contents.add_content'

    def dispatch(self, request, module_id,  model_name, pk):
        model_ = self.get_model(model_name)
        self.get_fields(model_)
        logger.debug(self.fields)
        self.module = get_object_or_404(Module, id = module_id, course__owner = request.user)
        self.model = model_   
        return super(ModuleContentCreateView, self).dispatch(request, module_id,  model_name, pk)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        object = form.save()
        Content.objects.create(module= self.module, item=object)
        return redirect('courses:course-module', pk = self.kwargs['pk'], module_id= self.kwargs['module_id'])



            