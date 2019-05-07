from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import User, Route, Note, Workflow, RouteWorkflow, Note, RouteLog

from .forms import NoteForm, RouteForm, UploadFileForm

def route_list(request):
    if(request.user.is_authenticated):
        routes = Route.objects.all()
        rw = []
        for route in routes:
            r = RouteWorkflow.objects.filter(route=route).first()
            rw.append(r)

        routes = merge(routes, rw)
        return render(request, 'route_list.html', {'routes': routes})
    else:
        return render(request, 'home.html')

def merge(list1, list2): 
      
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
    return merged_list 

def route(request, route_name):
    route = Route.objects.filter(route_name = route_name).first()
    notes = Note.objects.filter(route__route_name=route_name)
    logs = RouteLog.objects.filter(route__route_name=route_name)
    wf = RouteWorkflow.objects.filter(route__route_name=route_name, status=1).first()
    if not wf:
        wf = RouteWorkflow.objects.filter(route__route_name=route_name, status=3).first()
    return render(request, 'route.html', {'route':route, 'wf':wf, 'notes':notes, 'logs':logs})

def add_note(request, route_name):
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            start = form.cleaned_data['start_frame']
            end = form.cleaned_data['end_frame']
            message = form.cleaned_data['message']
            # print(message)
            # print(route_name)
            route = Route.objects.filter(route_name=route_name).first()
            note = Note.objects.create(route=route, start_frame=start, end_frame=end, message=message)

            notes = Note.objects.filter(route__route_name=route_name)
            # return render(request, 'route.html', {'route':route, 'notes':notes})
            return redirect('/routes/' + route_name)
    else:
        form = NoteForm()

    return render(request, 'add_note.html', {'form': form})

def add_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)

        if form.is_valid():
            route_name = form.cleaned_data['route_name']
            route_length = form.cleaned_data['route_length']

            route = Route.objects.create(route_name=route_name, route_length=route_length)
            route.save()

            return redirect('add_route')
    else:
        form = RouteForm()

    return render(request, 'add_route.html', {'form': form})

def checkout(request, route_name):
    route = Route.objects.filter(route_name=route_name).first()
    route.active_user=request.user
    route.save()

    rw = RouteWorkflow.objects.filter(route=route).first()
    rw.status=1
    rw.save()

    log = RouteLog.objects.create(user=request.user, route=route, workflow=rw.workflow)
    log.save()

    routes = Route.objects.all()
    return redirect('route_list')

def turnin(request, route_name):
    route = Route.objects.filter(route_name=route_name).first()
    route.active_user=None
    route.save()

    rw = RouteWorkflow.objects.filter(route=route).first()

    log = RouteLog.objects.filter(workflow=rw.workflow).first()
    log.save()

    wf1 = Workflow.objects.filter(workflow_name='WF1').first()
    wf2 = Workflow.objects.filter(workflow_name='WF2').first()
    wf3 = Workflow.objects.filter(workflow_name='WF3').first()
    qc = Workflow.objects.filter(workflow_name='QC').first()
    rw.status=0
    if (rw.workflow == wf1):
        rw.workflow = wf2
    elif (rw.workflow == wf2):
        rw.workflow = wf3
    elif (rw.workflow == wf3):
        rw.workflow = qc
    else:
        rw.status = 3
    rw.save()

    

    return redirect('route_list')
