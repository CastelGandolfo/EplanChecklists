from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Eplan, Device, EplanDevice, ChecklistPoint, SelectedCheckpoint
from itertools import chain
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from .forms import CheckpointForm

def home(request):
    return render(request, 'checklists/home.html')


# /projects
@login_required
def projects(request):
    projects = Project.objects.all()

    # wyciągniecie ilości eplanów do każdego projektu 
    for project in projects:
        project.eplan_count = Eplan.objects.filter(project=project).count()


    selected_projects = 0
    checkpoint_projects = 0
    # wyciągnięcie do każdego eplanu, urządzeń, pytań, stosunek selected/checkpoint
    for project in projects:
        eplans = Eplan.objects.filter(project=project)
        
        selected_project = 0
        project_checkpoint = 0

        for eplan in eplans:
            eplan_devices = EplanDevice.objects.filter(eplan=eplan)  

            # pytania zrobione dla każdego eplan_device
            for eplan_device in eplan_devices:

                selected_projects += SelectedCheckpoint.objects.filter(eplan_device=eplan_device).count()
                selected_project += SelectedCheckpoint.objects.filter(eplan_device=eplan_device).count()
                # łączna ilość pytań 
                device = eplan_device.device
                checkpoint_projects += ChecklistPoint.objects.filter(device=device).count()
                project_checkpoint += ChecklistPoint.objects.filter(device=device).count()       
        try:
            project.progress = round((selected_project / checkpoint_projects) * 100)
        except ZeroDivisionError:
            project.progress = 0
                   
    # Progress projektu w %
    try:
        progress_procentage = round((selected_projects / checkpoint_projects) * 100)
    except ZeroDivisionError:
        progress_procentage = 0
 
    return render(request, 'checklists/projects.html', {"projects": projects, "selected_projects": selected_projects, "checkpoint_projects": checkpoint_projects, "progress_procentage": progress_procentage})

# Pojedynczy projekt
# /projects/1
@login_required
def singleproject(request, project_pk):
    # znalezienie projektu pk
    project = get_object_or_404(Project, pk=project_pk)

    # filtrowanie eplanów (objekt Eplan) dla danego projektu
    eplans = Eplan.objects.filter(project=project_pk)

    selected_eplans = 0
    checkpoint_eplans = 0

    for eplan in eplans:
        eplan_devices = EplanDevice.objects.filter(eplan=eplan)
        eplan.device_count = EplanDevice.objects.filter(eplan=eplan).count()


        selected_eplan = 0
        checkpoint_eplan = 0

        for eplan_device in eplan_devices:
            selected_eplan += SelectedCheckpoint.objects.filter(eplan_device=eplan_device).count()
            selected_eplans += SelectedCheckpoint.objects.filter(eplan_device=eplan_device).count()
            # łączna ilość pytań 

            device = eplan_device.device
            checkpoint_eplan += ChecklistPoint.objects.filter(device=device).count()
            checkpoint_eplans += ChecklistPoint.objects.filter(device=device).count()


        try:
            eplan.progress = round((selected_eplan / checkpoint_eplan) * 100)
        except ZeroDivisionError:
            eplan.progress = 0
                   
    # Progress projektu w %
    try:
        progress_procentage = round((selected_eplans / checkpoint_eplans) * 100)
    except ZeroDivisionError:
        progress_procentage = 0
  


    return render(request, 'checklists/singleproject.html', {"eplans": eplans, "project": project, "selected_eplans": selected_eplans, "checkpoint_eplans": checkpoint_eplans, "progress_procentage": progress_procentage})

# Pojedynczy eplan w projekcie
# /projects/1/1
@login_required
def singleeplan(request, project_pk, eplan_pk):
    # znalezienie projektu pk
    project = get_object_or_404(Project, pk=project_pk)
    # znalezienie eplanu pk
    eplan = get_object_or_404(Eplan, pk=eplan_pk)
        
    eplan_devices = EplanDevice.objects.filter(eplan=eplan)
    eplan.device_count = EplanDevice.objects.filter(eplan=eplan).count()

    selected_devices = 0
    checkpoint_devices = 0

    for eplan_device in eplan_devices:       

        selected_device = 0
        checkpoint_device = 0

        selected_device += SelectedCheckpoint.objects.filter(eplan_device=eplan_device).count()
        selected_devices += SelectedCheckpoint.objects.filter(eplan_device=eplan_device).count()
        # łączna ilość pytań 

        device = eplan_device.device
        eplan_device.checkpoint_count = ChecklistPoint.objects.filter(device=device).count()

        checkpoint_device += ChecklistPoint.objects.filter(device=device).count()
        checkpoint_devices += ChecklistPoint.objects.filter(device=device).count()
        try:
            eplan_device.progress = round((selected_device / checkpoint_device) * 100)
        except ZeroDivisionError:
            eplan_device.progress = 0
                   
    # Progress projektu w %
    try:
        progress_procentage = round((selected_devices / checkpoint_devices) * 100)
    except ZeroDivisionError:
        progress_procentage = 0

    return render(request, 'checklists/singleeplan.html', {"eplan_devices": eplan_devices, "eplan": eplan, "project": project,"selected_devices": selected_devices, "checkpoint_devices": checkpoint_devices, "progress_procentage": progress_procentage})

# Pojedyncze urządzenie w eplanie w projekcie
# /projects/1/1/1
@login_required
def eplandevice(request, project_pk, eplan_pk, eplandevice_pk):
    # znalezienie projektu pk
    project = get_object_or_404(Project, pk=project_pk)
    # znalezienie eplanu pk
    eplan = get_object_or_404(Eplan, pk=eplan_pk)

    # znalezienie device do danego eplana
    eplan_device = get_object_or_404(EplanDevice, pk=eplandevice_pk)

    selected_checklist_points = eplan_device.selected_checklist_points.all()

    # znalezienie typu device
    device = eplan_device.device
    # device = Device.objects.filter(device = eplan_device)

    # znalezienie checkpointów
    checkpoints = ChecklistPoint.objects.filter(device=device)

    for checkpoint in checkpoints:
        if checkpoint in selected_checklist_points:
            if not SelectedCheckpoint.objects.filter(checklist_point=checkpoint).first().user_edited == "":
                checkpoint.is_finished = True
                checkpoint.user_edited = SelectedCheckpoint.objects.filter(checklist_point=checkpoint).first().user_edited
            if not SelectedCheckpoint.objects.filter(checklist_point=checkpoint).first().user_verified == "":
                checkpoint.is_verified = True
                checkpoint.user_verified = SelectedCheckpoint.objects.filter(checklist_point=checkpoint).first().user_verified
          
        # print(checkpoint.is_finished)

    return render(request, 'checklists/eplandevice.html', {"checkpoints": checkpoints, "device": device, "eplan_device": eplan_device, "eplan": eplan, "project": project})

@login_required
def checkpoint(request, project_pk, eplan_pk, eplandevice_pk, checkpoint_pk):
    if request.method == 'POST':
        # znalezienie device do danego eplana
        eplan_device = get_object_or_404(EplanDevice, pk=eplandevice_pk)

        # selected checkpointy
        selected_checklist_points = eplan_device.selected_checklist_points.all()

        # znalezienie checkpointa z forma
        checkpoint = ChecklistPoint.objects.get(pk=checkpoint_pk)

        # name = request.GET['name']
        # form = MyForm(request.POST)
        project = request.POST.get('finish', False)
        verify = request.POST.get('verify', False)


        print(project)
        print(verify)
        # print(request.POST.get('finish', False))
        # print(request.POST.get('verify', False))

        if project:
            if project == "projected":
                cpoint = SelectedCheckpoint(eplan_device=eplan_device, checklist_point=checkpoint, user_edited = request.user.username)
                cpoint.save()
            else:
                # usunięcie checkpointa
                if checkpoint in selected_checklist_points:
                    SelectedCheckpoint.objects.filter(checklist_point=checkpoint).delete()
                
        if verify:
            if verify == "verified":
                if SelectedCheckpoint.objects.filter(checklist_point=checkpoint).first():
                    cpoint = SelectedCheckpoint.objects.filter(checklist_point=checkpoint).first()
                    print(cpoint)
                    cpoint.user_verified = request.user.username
                    cpoint.save()

                # print(cpoint.user_verified)
                print("zweryfikowane")
            else:
                cpoint = SelectedCheckpoint.objects.filter(checklist_point=checkpoint).first()
                cpoint.user_verified = ""
                cpoint.save()
                print("odweryfikowane")
        # for item in request.POST:
        #     print(item)

        # print(request.POST)
        # try:
        #     if request.POST['finish']:
        #         print(request.POST['value'])
        # except:
        #     print("xx")

        

        return redirect('eplandevice', project_pk, eplan_pk, eplandevice_pk)
    else:
        return redirect('eplandevice', project_pk, eplan_pk, eplandevice_pk)

# /devices
@login_required
def genericdevices(request):
    devices = Device.objects.all()

    return render(request, 'checklists/devices.html', {"devices": devices})

# /devices/1
@login_required
def singledevice(request, device_pk):
    # znalezienie typu device
    device = get_object_or_404(Device, pk=device_pk)
    # device = Device.objects.filter(device = eplan_device)

    # znalezienie checkpointów
    checkpoints = ChecklistPoint.objects.filter(device=device)

    
    return render(request, 'checklists/singledevice.html', {"checkpoints": checkpoints, "device": device})

# /devices/1 - tworzenie nowego checkpointa do device generycznego
@login_required
def createcheckpoint(request, device_pk):

    device = get_object_or_404(Device, pk=device_pk)
    # device = Device.objects.filter(device = eplan_device)

    # znalezienie checkpointów
    checkpoints = ChecklistPoint.objects.filter(device=device)

    if request.method == 'GET':
        return render(request, 'checklists/createcheckpoint.html', {'form':CheckpointForm()})
    else:
        try:
            form = CheckpointForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.device = device
            newtodo.save()
            return render(request, 'checklists/singledevice.html', {"checkpoints": checkpoints, "device": device})
        except ValueError:
            return render(request, 'checklists/createcheckpoint.html', {'form':CheckpointForm(), 'error':'Bad data passed in. Try again.'})

# /devices/1/1/delete - usuniecie checkpointa do urzadzenia generycznego
@login_required
def deletecheckpoint(request, device_pk, checkpoint_pk):

    device = get_object_or_404(Device, pk=device_pk)
    # device = Device.objects.filter(device = eplan_device)
    checkpoints = ChecklistPoint.objects.filter(device=device)

    # znalezienie checkpointów
    checkpoint = ChecklistPoint.objects.filter(pk=checkpoint_pk).first()

    if request.method == 'POST':
        checkpoint.delete()
        return render(request, 'checklists/singledevice.html', {"checkpoints": checkpoints, "device": device})
    else:
        return render(request, 'checklists/singledevice.html', {"checkpoints": checkpoints, "device": device})

def logoutuser(request):
    # czesto przegladarki w momencie zaladowania strony tam gdzie się da robią get requesty, zeby bylo szybciej jak juz sobie klikniesz 
    # if logout is get request chrome can kick out 
    # we logout only for post request!!!
    if request.method == "POST":
        logout(request)
        return redirect('home')


def loginuser(request):
    # Podobnie jak w przypadku tworzenia konta, przy GET request, z tą różnica ze zamiast UserCreationForm dostajemy AuthenticationForm
    if request.method == 'GET':
        return render(request, 'checklists/loginuser.html', {'form':AuthenticationForm()})
    else:
        # W przypadku login form nie mamy juz password1 i password2 tylko password bo jest tylko jeden
        # importujemy sobie funkcje authenticate (podobnie jak w przypadku login/logout)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # sprawdzamy czy dostajemy jakiegos usera w zamian za username i password z login forma którego sobie utworzyliśmy
        if user is None:
            return render(request, 'checklists/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match. Try again'})
        else:
            # jesli z funkcji authenticate dostajemy jakiegos usera wtedy mozemy go po prostu zalogowac i gitara
            login(request, user)
            #  no i przekierować do aktualnych zadań
            return redirect('projects')