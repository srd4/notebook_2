from pickle import FALSE
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Box, Idea
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

class boxesView(generic.ListView):
    model = Box
    template_name = 'notebook/boxes.html'
    context_object_name = 'boxes_list'

    def get_queryset(self):
        """Return all boxes."""
        return Box.objects.all()


class boxDetailView(generic.ListView):
    template_name = 'notebook/box_detail.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        ideas_list = Idea.objects.filter(box_id=pk)

        if self.request.GET.get('done') == "on":
            ideas_list = ideas_list.filter(done=True)
        elif self.request.GET.get('actionable') == "on":
            ideas_list = ideas_list.filter(actionable=True)

        return ideas_list

    def get(self, request, pk):
        """Return all ideas."""
        bx = Box.objects.get(pk=pk)
        ctx = {
        "idea_list": self.get_queryset(),
        "box": bx,
        'done': self.request.GET.get('done'),
        'actionable': self.request.GET.get('actionable'),
        'non-actionable': self.request.GET.get('non-actionable'),
        }
        return render(request, self.template_name, ctx)


class addBoxView(CreateView):
    model = Box
    fields = '__all__'
    template_name = 'notebook/new_box.html'

    def get_success_url(self):
        """so user is taken to box_detail page of created box"""
        pk = self.model.objects.last().id
        return reverse_lazy('notebook:box_detail', kwargs={"pk":pk})


class editBoxView(UpdateView):
    model = Box
    fields = '__all__'
    template_name = 'notebook/edit_box.html'
    success_url = reverse_lazy('notebook:boxes')


class deleteBoxView(DeleteView):
    model = Box
    fields = '__all__'
    template_name = 'notebook/delete_box.html'
    success_url = reverse_lazy('notebook:boxes')


#views for ideas.
class ideasView(generic.ListView):
    model = Idea
    template_name = 'notebook/ideas.html'
    context_object_name = 'ideas_list'

    def get_queryset(self):
        """Return all ideas."""
        return Idea.objects.all()


class addIdeaView(CreateView):
    model = Idea
    fields = '__all__'
    template_name = 'notebook/new_idea.html'

    def get_success_url(self):
        return reverse_lazy('notebook:box_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self,*args, **kwargs):
        context = super(addIdeaView, self).get_context_data(*args,**kwargs)
        context['box'] = Box.objects.get(pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        return {'box': self.kwargs['pk']}


class editIdeaView(UpdateView):
    model = Idea
    fields = '__all__'
    template_name = 'notebook/edit_idea.html'

    def get_success_url(self):
        i = Idea.objects.filter(id=self.kwargs['pk'])[0]
        return reverse_lazy('notebook:box_detail', kwargs={'pk': i.box.pk})

    def get_context_data(self,*args, **kwargs):
        context = super(editIdeaView, self).get_context_data(*args,**kwargs)
        i = Idea.objects.filter(id=self.kwargs['pk'])[0]
        context['box'] = Box.objects.get(pk=i.box.pk)
        context['idea'] = i
        return context



class deleteIdeaView(DeleteView):
    model = Idea
    fields = '__all__'
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


