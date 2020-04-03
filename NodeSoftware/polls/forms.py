from django import forms
from multiupload.fields import MultiFileField
#fully functional

class NewQuestion(forms.Form):

    tag_options = [
        (11, 'Tag1'),
        (12, 'Tag2'),
        (13, 'Tag3'),
        (14, 'Tag4'),
        (15, 'Tag5'),
    ]

    language_options = [
        ('Python', 'Python')
    ]

    title = forms.CharField(max_length=64)
    language = forms.ChoiceField(required = False, choices = language_options)
    spec = forms.FileField()
    datasets = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    code = forms.FileField(required = False)
    tags = forms.MultipleChoiceField(required = False, choices = tag_options)

# TO COMPLETE

class NewSubmissionForm(forms.Form):
    submitted_code_file = forms.FileField()
    editing_area = forms.CharField(widget = forms.Textarea, required = False)

# Fully functional

class NewNode(forms.Form):
    name = forms.CharField(min_length = 1, max_length = 200)

#Fully functional

class NewClient(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(min_length = 1, max_length = 200)
    password = forms.CharField(widget = forms.PasswordInput)
    confirm_password = forms.CharField(widget = forms.PasswordInput)

#FINISHED

class LoginForm(forms.Form):
    username = forms.CharField(min_length = 1, max_length = 200)
    password = forms.CharField(widget = forms.PasswordInput)

#FINISHED

class InviteForm(forms.Form):
    options = ((11, 'Regular User'), (12, 'Admin User'))
    choice = forms.ChoiceField(widget = forms.RadioSelect, choices = options)
    email = forms.EmailField()

class SearchForm(forms.Form):
    search_field = forms.CharField(max_length = 200, required = False)

class TestForm(forms.Form):
    multi_file_field = MultiFileField(min_num = 1, max_num = 5, required = False)
