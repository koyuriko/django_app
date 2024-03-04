from django import forms
from  .models import Message,Good
from django.contrib.auth.models import User

#messageフォームです
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']