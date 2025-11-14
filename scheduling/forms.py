from django import forms
from .models import Slot


class SlotCreateForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ["start_time", "end_time", "location", "max_students"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Room 301 or Zoom link"}),
            "max_students": forms.NumberInput(attrs={"class": "form-control", "min": 1, "value": 1}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_time")
        end = cleaned.get("end_time")
        if start and end and end <= start:
            self.add_error("end_time", "End time must be after start time.")
        return cleaned