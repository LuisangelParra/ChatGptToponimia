from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Person, Log
from .forms import PersonForm

# Create your views here.
def index(request):
    context = {}
    form = PersonForm()
    action = "create"
    persons = Person.objects.all()
    context["persons"] = persons
    context["form"] = form
    context["action"] = action

    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            Log.objects.create(action=f"Registró persona: {form.cleaned_data['first_name']} {form.cleaned_data['lasts_names']}, Tipo de documento: {form.cleaned_data['document_type']}, Número de documento: {form.cleaned_data['document_id']}")
            toponimia = Person.objects.get(document_id=form.cleaned_data['document_id']).toponimia
            logs = Log.objects.all().order_by('-timestamp')
            context["logs"] = logs
            context["toponimia"] = toponimia
            return render(request, "crud.html",  context)
        else:
            form = PersonForm()
    logs = Log.objects.all().order_by('-timestamp')
    context["logs"] = logs
    return render(request, "crud.html",  context)

def update(request, id):
    context = {}
    action = "update"
    person = Person.objects.get(id=id)
    persons = Person.objects.all()
    form = PersonForm(instance=person)
    toponimia = person.toponimia
    context["form"] = form
    context["persons"] = persons
    context["action"] = action
    context["toponimia"] = toponimia

    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            Log.objects.create(action=f"Actualizó persona: {form.cleaned_data['first_name']} {form.cleaned_data['lasts_names']}, Tipo de documento: {form.cleaned_data['document_type']}, Número de documento: {form.cleaned_data['document_id']}")
            return redirect("index")
        else:
            form = PersonForm()
    logs = Log.objects.all().order_by('-timestamp')
    context["logs"] = logs
    return render(request, "crud.html", context)

def delete(request, id):
    person = Person.objects.get(id=id)
    Log.objects.create(action=f"Eliminó persona: {person.first_name} {person.lasts_names}, Tipo de documento: {person.document_type}, Número de documento: {person.document_id}")
    person.delete()
    return redirect("index")