from django.forms import ModelForm
from .models import ChecklistPoint

class CheckpointForm(ModelForm):
    class Meta:
        model = ChecklistPoint
        fields = ['title']
