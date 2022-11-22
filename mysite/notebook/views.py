from pickle import FALSE
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Box, Idea
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render

from django.contrib.auth.mixins import LoginRequiredMixin

#correct link everywhere.
LoginRequiredMixin.login_url = reverse_lazy("notebook:login")

class boxesView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("notebook:login")
    redirect_field_name = "redirect_to"
    model = Box
    template_name = 'notebook/boxes.html'
    context_object_name = 'boxes_list'

    def get_queryset(self):
        #here boxes user doesn't own are not retrieved to be seen.
        t = super(boxesView, self).get_queryset()
        return t.filter(owner=self.request.user)


class boxDetailView(LoginRequiredMixin, generic.ListView):
    template_name = 'notebook/box_detail.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        ideas_list = Idea.objects.filter(box_id=pk, owner=self.request.user)

        if self.request.GET.get('done') == "on":
            ideas_list = ideas_list.filter(done=True)
        elif self.request.GET.get('actionable') == "on":
            ideas_list = ideas_list.filter(actionable=True)
        else:
            ideas_list = ideas_list.filter(actionable=False)

        return ideas_list.order_by('-updated_at', '-created_at')

    def get(self, request, pk):
        #boxes don't exist for users that don't own them.
        bx = Box.objects.get(pk=pk, owner=self.request.user)

        ctx = {
        "idea_list": self.get_queryset(),
        "box": bx,
        }

        return render(request, self.template_name, ctx)


class addBoxView(LoginRequiredMixin, CreateView):
    model = Box
    fields = ['name']
    template_name = 'notebook/new_box.html'

    def get_success_url(self):
        """so user is taken to box_detail page of created box"""
        pk = self.model.objects.last().id
        return reverse_lazy('notebook:box_detail', kwargs={"pk":pk})

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        print(object.owner)
        return super(addBoxView, self).form_valid(form)


class editBoxView(LoginRequiredMixin, UpdateView):
    model = Box
    fields = ['name']
    template_name = 'notebook/edit_box.html'
    success_url = reverse_lazy('notebook:boxes')

    def get_queryset(self):
        qs = super(editBoxView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        print(object.owner)
        return super(editBoxView, self).form_valid(form)


class deleteBoxView(LoginRequiredMixin, DeleteView):
    model = Box
    fields = ['name']
    template_name = 'notebook/delete_box.html'
    success_url = reverse_lazy('notebook:boxes')
    
    def get_queryset(self):
        qs = super(deleteBoxView, self).get_queryset()
        return qs.filter(owner=self.request.user)



class addIdeaView(LoginRequiredMixin, CreateView):
    model = Idea
    fields = ["done", "box", "text", "actionable"]
    template_name = 'notebook/new_idea.html'

    def get_form(self, form_class=None):
        print("this function is called")
        form = super(addIdeaView, self).get_form()
        form.fields["box"].queryset = Box.objects.filter(owner=self.request.user)
        print("fuck", form.fields["box"])
        return form

    def get_success_url(self):
        return reverse_lazy('notebook:box_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self,*args, **kwargs):
        context = super(addIdeaView, self).get_context_data(*args,**kwargs)
        context['box'] = Box.objects.get(pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        return {'box': self.kwargs['pk']}
    
    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        print(object.owner)
        return super(addIdeaView, self).form_valid(form)


class editIdeaView(LoginRequiredMixin, UpdateView):
    model = Idea
    fields = ["done", "box", "text", "actionable"]
    template_name = 'notebook/edit_idea.html'

    def get_form(self, form_class=None):
        print("this function is called")
        form = super(editIdeaView, self).get_form()
        form.fields["box"].queryset = Box.objects.filter(owner=self.request.user)
        print("fuck", form.fields["box"])
        return form

    def get_success_url(self):
        i = Idea.objects.filter(id=self.kwargs['pk'])[0]
        return reverse_lazy('notebook:box_detail', kwargs={'pk': i.box.pk})

    def get_context_data(self,*args, **kwargs):
        context = super(editIdeaView, self).get_context_data(*args,**kwargs)
        i = Idea.objects.filter(id=self.kwargs['pk'])[0]
        context['box'] = Box.objects.get(pk=i.box.pk)
        context['idea'] = i
        return context

    def get_queryset(self):
        qs = super(editIdeaView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class deleteIdeaView(LoginRequiredMixin, DeleteView):
    model = Idea
    fields = ["done", "box", "text", "actionable"]
    template_name = 'notebook/delete_idea.html'

    def get_success_url(self):
        i = Idea.objects.filter(id=self.kwargs['pk'])[0]
        return reverse_lazy('notebook:box_detail', kwargs={'pk': i.box.pk})

    def get_context_data(self,*args, **kwargs):
        context = super(deleteIdeaView, self).get_context_data(*args,**kwargs)
        i = Idea.objects.filter(id=self.kwargs['pk'])[0]
        context['box'] = Box.objects.get(pk=i.box.pk)
        context['idea'] = i
        return context

    def get_queryset(self):
        qs = super(deleteIdeaView, self).get_queryset()
        return qs.filter(owner=self.request.user)