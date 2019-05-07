from django import forms

from .models import Note, Route

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('start_frame', 'end_frame', 'message',)

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ('route_name', 'route_length',)

def validate_csv(value):
    if not value.name.endswith('.csv'):
        raise ValidationError(u'Error message')

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField(validators=[validate_csv])