from django import forms
from app.models import Canvas


class CanvasForm(forms.ModelForm):
    class Meta:
        model = Canvas
        fields = ['company','description','logo',
        'value_propositions','customer_segments',
        'partners','relationships','channels','activities',
        'resources','revenue','cost']
        dim = {'rows':4, 'cols':150}
        widgets = {
            'value_propositions': forms.Textarea(attrs=dim),
            'customer_segments': forms.Textarea(attrs=dim),
            'partners': forms.Textarea(attrs=dim),
            'relationships': forms.Textarea(attrs=dim),
            'channels': forms.Textarea(attrs=dim),
            'activities': forms.Textarea(attrs=dim),
            'resources': forms.Textarea(attrs=dim),
            'revenue': forms.Textarea(attrs=dim),
            'cost': forms.Textarea(attrs=dim),
        }