from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from main.models import Visit, Service
from main.forms import ClientVisitForm, MasterVisitForm


#---------Service----------
class ServiceListView(ListView):
    model = Service


class ServiceDetailView(DetailView):
    model = Service


class ServiceCreateView(CreateView):
    model = Service
    fields = '__all__'
    template_name = 'main/form.html'
    success_url = reverse_lazy('main:service_all')

class ServiceUpdateView(UpdateView):
    model = Service
    fields = '__all__'
    template_name = 'main/form.html'
    success_url = reverse_lazy('main:service_all')

class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy('main:service_all')


#---------Visit-----------
class VisitListView(ListView):
    model = Visit
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        print(data)
        return data


class VisitDetailView(DetailView):
    model = Visit



class VisitCreateView(CreateView):
    template_name = 'main/visit_form.html'
    success_url = reverse_lazy('main:visit_all')
    master_group = 'Master'
    
    def form_valid(self, form):
        if not self.request.user.groups.filter(name=self.master_group).exists():
            obj = form.save(commit=False)
            obj.client = self.request.user
            obj.save()
        else:
            form.save()
        return super(CreateView, self).form_valid(form)

    def get_form_class(self, *args, **kwargs):
        if self.request.user.groups.filter(name=self.master_group).exists():
            return MasterVisitForm
        else:
            return ClientVisitForm

"""
    def get(self, request):
        if request.user.groups.filter(name=self.master_group).exists():
            form = MasterVisitForm()
        else:
            form = ClientVisitForm()
        return render(request, self.template_name, {'form': form })
    
    def post(self, request):
        if request.user.groups.filter(name=self.master_group).exists():
            form = MasterVisitForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.success_url)
            else:
                return render(request, self.template, {'form': form })
        else:
            form = ClientVisitForm(request.POST)
            if form.is_valid():
                visit = form.save(commit=False)
                visit.client = request.user
                visit.save()
                return redirect(self.success_url)
            else:
                return render(request, self.template, {'form': form })
"""

class VisitUpdateView(UpdateView):
    model = Visit
    template_name = 'main/visit_form.html'
    master_group = 'Master'
    success_url = reverse_lazy('main:visit_all')

    def get_form_class(self, *args, **kwargs):
        if self.request.user.groups.filter(name=self.master_group).exists():
            return MasterVisitForm
        else:
            return ClientVisitForm

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(client=self.request.user)


class VisitDeleteView(DeleteView):
    model = Visit
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(client=self.request.user)