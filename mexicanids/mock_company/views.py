from django.shortcuts import render, redirect
from .forms import ShortPersonForm, FullPersonForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class PageTemplateView(TemplateView):
    template_name = ""


def shortFormComponent(request):
    if request.method == 'POST':
        form = ShortPersonForm(request.POST)
        if form.is_valid():
            request.session['temp_data'] = request.POST
            return redirect('mock_company:full_form')
    else:
        form = ShortPersonForm()

    return render(request, 'mock_company/short_form.html', {'form': form})


def fullFormComponent(request):
    if request.method == 'POST':
        # Case post request.
        form = FullPersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Sucesss!")
    else:
        if 'temp_data' in request.session:
            # Case get request from shortform.
            form = FullPersonForm(initial=request.session['temp_data'])
        else:
            # Case get request elsewhere.
            form = FullPersonForm()

    # Render template with form.
    return render(request, 'mock_company/full_form.html', {'form': form})

