from django.db import models


# Project - grupa sterowników Eplan, jeden projekt zawiera wiele sterowników w eplanie
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # created = models.DateTimeField(auto_now_add=True)
    # datecompleted = models.DateTimeField(null=True, blank=True)
    # important = models.BooleanField(default=False)
    # Foregin key to user model
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    eplan_count = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# Eplan - pojedynczy zw1 w eplanie
class Eplan(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    device_count = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.title

# EplanDevice - urządzenie z ID z eplana


# Device - urządzenie z przypisanymi punktami
class Device(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class EplanDevice(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    eplan = models.ForeignKey(Eplan, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    selected_checklist_points = models.ManyToManyField(
        'ChecklistPoint', through='SelectedCheckpoint')


    checkpoint_count = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# ChecklistPoint - punkt z checklisty przyporządkowany do device
class ChecklistPoint(models.Model):
    title = models.CharField(max_length=100)
    checkpoint_text = models.TextField(blank=True)
    is_finished = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user_edited = models.CharField(blank=True, max_length=100)
    user_verified = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.title


class SelectedCheckpoint(models.Model):
    eplan_device = models.ForeignKey(EplanDevice, on_delete=models.CASCADE)
    checklist_point = models.ForeignKey(
        ChecklistPoint, on_delete=models.CASCADE)
    user_edited = models.CharField(blank=True, max_length=100)
    user_verified = models.CharField(blank=True, max_length=100)
