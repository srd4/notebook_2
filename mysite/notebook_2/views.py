from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Container, Item
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django import forms
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

LoginRequiredMixin.login_url = reverse_lazy('notebook_2:login')

def itemDone(request, pk):
    i = Item.objects.get(pk=pk, owner=request.user)
    i.toggleDone()
    return render(request, 'notebook_2/item.html', {'container':i.parentContainer, 'item':i})


def containerCollapse(request, pk):
    """toggles collapsed or not on containersView"""
    c = Container.objects.get(pk=pk, owner=request.user)
    c.toggleCollapsed()
    return render(request, 'notebook_2/containersList.html', {'container_list':[c,]})


def containerChangeTab(request, pk):
    """toggles action or non-actionable or not on containerDetailView"""
    c = Container.objects.get(pk=pk, owner=request.user)
    if request.GET.get('toggle') == "True":
        c.toggleTab()
    return render(request, 'notebook_2/itemList.html', {'item_list': c.getItems().order_by('-updated_at'), 'container': c})

class loginView(LoginView):
    template_name = "notebook_2/login.html"

class logoutView(LogoutView):
    next_page = reverse_lazy('notebook_2:login')

class registerView(FormView):
    template_name = "notebook_2/register.html"
    success_url = next_page = reverse_lazy('notebook_2:containers')
    form_class = UserCreationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        User = form.save()
        Container(name="inbox", owner=User).save()
        if User is not None:
            login(self.request, User)
        return super(registerView, self).form_valid(form)


class searchView(LoginRequiredMixin, generic.TemplateView):
    template_name = "notebook_2/searchView.html"

    def get_context_data(self):
        searchInput = self.request.GET.get('q') or ''

        if searchInput:
            cqs = Container.objects.all()
            iqs = Item.objects.all()
            cqs = cqs.filter(Q(Q(name__icontains=searchInput) | Q(description__icontains=searchInput)), owner=self.request.user)
            iqs = iqs.filter(Q(statement__icontains=searchInput), owner=self.request.user)
        else:
            return {"container_list":{}, "item_list":{}}

        return {"container_list":cqs, "item_list":iqs}



class containersView(LoginRequiredMixin, generic.TemplateView):
    model = Container
    template_name = 'notebook_2/containers.html'
    context_object_name = 'container_list'
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx["container_list"] = Container.objects.filter(parentContainer=None, owner=self.request.user).order_by('-timesOpened')
        ctx['container'] = Container.objects.get_or_create(name="inbox", owner=self.request.user)
        return ctx


class containerDetailView(LoginRequiredMixin, generic.ListView):
    model = Container
    template_name = 'notebook_2/containerDetail.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        return Item.objects.filter(parentContainer=self.kwargs['pk'], owner=self.request.user)

    def get_context_data(self, **kwargs):
        c = Container.objects.get(pk=self.kwargs['pk'], owner=self.request.user)
        c.add_lastOpened()
        c.add_timesOpened()
        if self.request.GET.get('toggleDone') != None:
            i = Item.objects.get(pk=self.request.GET.get('toggleDone'), owner=self.request.user)
            i.toggleDone()

        return {"container": c, 'item_list': self.get_queryset().order_by('-updated_at')}

    def post(self, *args, **kwargs):
        if self.request.POST.get('checkbox') != None:
            Item.objects.get(pk=self.request.POST.get('checkbox'), owner=self.request.user).toggleDone()
        return render(self.request, self.template_name, self.get_context_data())




class containerCreateView(LoginRequiredMixin, CreateView):
    model = Container
    template_name = 'notebook_2/containerCreate.html'
    fields = ["name","description", "parentContainer"]

    def get_success_url(self):
        pk = Container.objects.filter(owner=self.request.user).last().id
        return reverse_lazy("notebook_2:containers")

    def get_form(self):
        form = super(containerCreateView, self).get_form()
        form.fields["parentContainer"].required = False
        form.fields["parentContainer"].queryset = Container.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        c = form.save(commit=False)
        c.owner = self.request.user
        c.save()
        return super(containerCreateView, self).form_valid(form)



class containerUpdateView(LoginRequiredMixin, UpdateView):
    model = Container
    template_name = 'notebook_2/containerUpdate.html'
    context_object_name = 'container_list'
    fields = ["name","description", "parentContainer"]
    success_url = reverse_lazy('notebook_2:containers')

    def get_form(self):
        form = super(containerUpdateView, self).get_form()
        form.fields["parentContainer"].required = False
        form.fields["parentContainer"].queryset = Container.objects.filter(owner=self.request.user)
        return form



class containerDeleteView(LoginRequiredMixin, DeleteView):
    model = Container
    template_name = 'notebook_2/containerDelete.html'
    context_object_name = 'container_list'
    success_url = reverse_lazy("notebook_2:containers")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['container'] = Container.objects.get(pk=self.kwargs['pk'], owner=self.request.user)
        return ctx


#item views

class itemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'notebook_2/itemCreate.html'
    fields = ["done", "parentContainer", "parentItem", "statement", "actionable"]
    
    def get_success_url(self):
        return reverse_lazy("notebook_2:container_detail", kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, *args, **kwargs):
        ctx = super(itemCreateView, self).get_context_data(*args,**kwargs)
        ctx['container'] = Container.objects.get(pk=self.kwargs['pk'], owner=self.request.user)
        return ctx

    def get_form(self):
        f = super(itemCreateView, self).get_form()
        f.fields['parentContainer'].initial = Container.objects.get(pk=self.kwargs['pk'], owner=self.request.user)
        f.fields["parentContainer"].queryset = Container.objects.filter(owner=self.request.user)
        f.fields['parentItem'].required = False
        f.fields['parentItem'].initial = self.request.GET.get('pk')
        f.fields['parentItem'].widget = forms.HiddenInput()
        f.fields['actionable'].initial = True if self.request.GET.get('actionable') == "True" else False
        print(self.request.GET.get('pk'), self.request.GET.get('actionable'))
        return f

    def form_valid(self, form):
        i = form.save(commit=False)
        i.owner = self.request.user
        i.save()
        return super(itemCreateView, self).form_valid(form)


class itemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'notebook_2/itemUpdate.html'
    fields = ["done", "parentContainer", "parentItem", "statement", "actionable"]
    success_url = reverse_lazy("notebook_2:container_detail", kwargs={'pk': 1})

    def get_context_data(self, *args, **kwargs):
        ctx = super(itemUpdateView, self).get_context_data(*args,**kwargs)
        item = Item.objects.get(pk=self.kwargs['pk'], owner=self.request.user)
        ctx['container'] = item.parentContainer
        return ctx

    def get_form(self):
        f = super(itemUpdateView, self).get_form()
        f.fields['parentItem'].required = False
        f.fields['parentItem'].widget = forms.HiddenInput()
        return f

    def get_success_url(self):
        success_url = reverse_lazy("notebook_2:container_detail", kwargs={'pk': self.request.GET.get('next')})
        return success_url



class itemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'notebook_2/itemDelete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(itemDeleteView, self).get_context_data(*args,**kwargs)
        item = Item.objects.get(pk=self.kwargs['pk'], owner=self.request.user)
        ctx['container'] = item.parentContainer

        return ctx
    
    def get_success_url(self):
        item = Item.objects.get(pk=self.kwargs['pk'], owner=self.request.user)
        return reverse_lazy('notebook_2:container_detail', kwargs={'pk': item.parentContainer.id})