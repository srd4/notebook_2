from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Box, Idea
from django.urls import reverse_lazy
from django.shortcuts import render

class boxesView(generic.ListView):
    model = Box
    template_name = 'notebook/boxes.html'
    context_object_name = 'boxes_list'

    def get_queryset(self):
        """Return all boxes."""
        return Box.objects.all()


class boxDetailView(generic.ListView):
    template_name = 'notebook/box_detail.html'
    context_object_name = 'ideas_list'

    def get(self, request, pk):
        """Return all ideas."""
        il = Idea.objects.filter(box_id=pk)
        bx = Box.objects.filter(id=pk)[0]

        ctx = {"ideas_list": il,"box_name": bx.box_name, "box_id": bx.id}
        return render(request, self.template_name, ctx)


class addBoxView(CreateView):
    model = Box
    fields = '__all__'
    success_url = reverse_lazy('notebook:boxes')
    template_name = 'notebook/new_box.html'


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
    template_name = 'notebook/new_box.html'

    def get_success_url(self):
        box_id = self.kwargs['pk']
        return reverse_lazy('notebook:box_detail', kwargs={'pk': box_id})


class editIdeaView(UpdateView):
    model = Idea
    fields = '__all__'
    template_name = 'notebook/edit_box.html'

    def get_success_url(self):
        idea_id = self.kwargs['pk']
        box_id = Idea.objects.filter(id=idea_id)[0].box.id
        return reverse_lazy('notebook:box_detail', kwargs={'pk': box_id})


class deleteIdeaView(DeleteView):
    model = Idea
    fields = '__all__'
    template_name = 'notebook/delete_box.html'

    def get_success_url(self):
        idea_id = self.kwargs['pk']
        box_id = Idea.objects.filter(id=idea_id)[0].box.id
        return reverse_lazy('notebook:box_detail', kwargs={'pk': box_id})











