from django.forms import ModelForm
from .models import Chatbot
from django import forms

# Create the form class.
class ChatbotCreationForm(ModelForm):
    csv_file = forms.FileField(label='Upload CSV File', required=False)
    class Meta:
        model = Chatbot
        fields = ["name"]
