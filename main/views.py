from datetime import datetime

from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.conf import settings

from main.models import Visit, Service
from main.forms import ClientVisitForm, MasterVisitForm, ServiceForm
from main.utils import has_group

#---------Service---------------------------------------------------------------
class ServiceListView(ListView):
    model = Service


class ServiceCreateView(PermissionRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy('main:service_all')
    permission_required = ('main.add_service',)


class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy('main:service_all')
    permission_required = ('main.change_service',)


class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('main:service_all')
    permission_required = ('main.delete_service',)

#---------Visit-----------------------------------------------------------------
class VisitListView(ListView):
    model = Visit
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data


class GetQuerySetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if not has_group(self.request.user, settings.MASTER_GROUP_NAME):
            queryset = queryset.filter(client=self.request.user)
        return queryset


class FormValidMixin:
    exclude_object = False

    def form_valid(self, form):
        new_date_time = form.cleaned_data.get('date_time')
        new_service = form.cleaned_data.get('service')
        
        if new_date_time.date() <= datetime.now().date(): 
            form.add_error('date_time', _('Сan\'t create an entry for a past date'))
            return self.form_invalid(form)
        
        visits_date = Visit.objects.filter(date_time__date=new_date_time.date())
        if self.exclude_object:
            visits_date = visits_date.exclude(id=self.get_object().id)
            
        for visit in visits_date:
            if (visit.date_time < new_date_time < visit.end_date_time
                    or visit.date_time < (new_date_time+new_service.duration)
                        < visit.end_date_time ):
                form.add_error('date_time', _('Requested date and time are already taken'))
                return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_form_class(self, *args, **kwargs):
        if has_group(self.request.user, settings.MASTER_GROUP_NAME):
            return MasterVisitForm
        else:
            return ClientVisitForm


class ExtraClientMixin:
    def form_valid(self, form):
        if not has_group(self.request.user, settings.MASTER_GROUP_NAME):
            obj = form.save(commit=False)
            obj.client = self.request.user
            obj.save()
        return super().form_valid(form)


class VisitCreateView(FormValidMixin, ExtraClientMixin, LoginRequiredMixin, CreateView):
    template_name = 'main/visit_form.html'
    success_url = reverse_lazy('main:visit_all')


class VisitUpdateView(GetQuerySetMixin, FormValidMixin, LoginRequiredMixin, UpdateView):
    model = Visit
    template_name = 'main/visit_form.html'
    success_url = reverse_lazy('main:visit_all')
    exclude_object = True


class VisitDeleteView(GetQuerySetMixin, LoginRequiredMixin, DeleteView):
    model = Visit
    success_url = reverse_lazy('main:visit_all')
