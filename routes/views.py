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

def my_routes(request):
    if(request.user.is_authenticated):
        routes = Route.objects.filter(active_user=request.user)
        rw = []
        for route in routes:
            r = RouteWorkflow.objects.filter(route=route).first()
            rw.append(r)

        routes = merge(routes, rw)
        return render(request, 'my_routes.html', {'routes': routes})
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

def handle_uploaded_file(file):
    print('Heyo')

def upload_csv(request):
    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST)
    #     print('Heyo')

    #     if form.is_valid():
    #         handle_uploaded_file(request.FILES['file'])

    #         return redirect('upload_csv')
    # else:
    #     form = UploadFileForm()

    # return render(request, 'upload_csv.html', {'form': form})

    if "GET" == request.method:
        return render(request, "upload_csv.html")
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return redirect('upload_csv')
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return redirect('upload_csv')

        file_data = csv_file.read().decode("utf-8")		

        lines = file_data.split("\n")
        #loop over the lines and save them in db. If error , store as string and then display
        for line in lines:						
            fields = line.split(",")
            data_dict = {}
            data_dict["route_name"] = fields[0]
            data_dict["length"] = float(fields[1])
            r = Route.objects.create(route_name=fields[0], route_length=float(fields[1]))
            r.save()
            print(data_dict)

        return render(request, "upload_csv.html", {"Success":1})
            

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    return render(request, "upload_csv.html", {"Success":0})

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
    return redirect('route', route_name=route_name)

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

    

    return redirect('route', route_name=route_name)
