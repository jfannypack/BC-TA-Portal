from django import forms
from summary.models import Account, Student, Instructor, Admin, Course, Application
from django.forms import ModelForm, Textarea, PasswordInput, Select, Form, FileInput
from django.db import models
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.validators import RegexValidator

from summary.models import Account, Student, Instructor, Admin, Course, Application

class StudentRegisterForm(UserCreationForm):
    firstname = forms.CharField(label="First name", max_length=100, required=True)
    #firstname = forms.CharField()
    lastname = forms.CharField(label="Last name", max_length=100, required=True)
    #lastname = forms.CharField()
    email = forms.EmailField()
    major = forms.CharField()
    year_in_school = forms.ChoiceField(choices=Student.YEAR_IN_SCHOOL)
    work = forms.ChoiceField(label='Are you available to work?', choices=Student.OPEN_TO_WORK)
    #eagleid = forms.CharField()
    eagleid = forms.CharField(label='Eagle ID', validators=[RegexValidator(r'^\d{8}$', message='Eagle ID must be an 8-digit number.')])
    class Meta:
        model = Account
        fields = ['email', 'firstname', 'lastname', 'major', 'year_in_school', 'eagleid']
    

    def save(self):
        account = super().save(commit=False)
        email = self.cleaned_data.get('email')
        account.is_student = True
        account.email = email
        account.save()
        Student.objects.create(
            account = account,
            firstname=self.cleaned_data.get('firstname'),
            lastname=self.cleaned_data.get('lastname'),
            email = email,
            major=self.cleaned_data.get('major'),
            year_in_school=self.cleaned_data.get('year_in_school'),
            eagleid=self.cleaned_data.get('eagleid')
        )
        return account

class InstructorRegisterForm(UserCreationForm):
    firstname = forms.CharField(label="First name", max_length=100, required=True)
    #firstname = forms.CharField()
    lastname = forms.CharField(label="Last name", max_length=100, required=True)
    #lastname = forms.CharField()
    email = forms.EmailField()
    position = forms.CharField()

    class Meta:
        model = Account
        fields = ['email', 'firstname', 'lastname', 'position']

    def save(self):
        account = super().save(commit=False)
        email = self.cleaned_data.get('email')
        account.is_instructor = True
        account.email = email
        account.save()
        Instructor.objects.create(
            account=account,
            firstname=self.cleaned_data.get('firstname'),
            lastname=self.cleaned_data.get('lastname'),
            email=email,
            position = self.cleaned_data.get('position'),
        )
        return account


class AdminRegisterForm(UserCreationForm):
    firstname = forms.CharField(label="First name", max_length=100, required=True)
    #firstname = forms.CharField()
    lastname = forms.CharField(label="Last name", max_length=100, required=True)
    #lastname = forms.CharField()
    email = forms.EmailField()
    position = forms.CharField()

    class Meta:
        model = Account
        fields = ['email', 'firstname', 'lastname', 'position']

    @transaction.atomic
    def save(self):
        account = super().save(commit=False)
        email = self.cleaned_data.get('email')
        account.is_admin = True
        account.is_staff = True
        account.is_superuser = True
        account.email = email
        account.save()
        Admin.objects.create(
            account=account,
            firstname=self.cleaned_data.get('firstname'),
            lastname=self.cleaned_data.get('lastname'),
            email=email,
            position = self.cleaned_data.get('position'),
        )
        return account

class ApplicationForm(forms.ModelForm):
    course_list = Course.objects.all()
    selected_course = forms.ModelChoiceField(label="Select A Course to Apply For.", queryset=Course.objects.all())
    resume = forms.FileField(label="Upload a resume here.", required=False)
    experience = forms.CharField(label="Describe your previous experience with the course, including any grades you may have recieved.")
    class Meta:
        model = Application
        fields = ["selected_course", "experience", "resume"]

class CreateCourseForm(forms.ModelForm):
    Instructor = forms.ModelChoiceField(label="Instructor for the course", queryset=Instructor.objects.all())
    CourseID = forms.CharField(label = "CourseID")
    Name = forms.CharField(label = "Course Name")
    Description = forms.CharField(label = "Description")
    SeatData = forms.CharField(label = "Seats")
    Rooms = forms.CharField(label = "Rooms")
    Times = forms.CharField(label = "Times")
    TAs = forms.CharField(label = "TAs Needed")
    WithDiscussion = forms.CharField(label = "With Discussion?")
    GradedInMeeting = forms.CharField(label = "Graded In Meeting?")
    ExtraInfo = forms.CharField(label = "Extra Course Info")

    class Meta:
        model = Course
        fields = ('CourseID', 'Name', 'Instructor', 'Description', 'SeatData', 'Rooms', 'Times', 'TAs', 'WithDiscussion', 'GradedInMeeting', 'ExtraInfo')

class EditCourseForm(forms.Form):
    class Meta:
        model = Course
        fields = ('CourseID', 'Name', 'Instructor', 'Description', 'SeatData', 'Rooms', 'Times', 'TAs', 'WithDiscussion', 'GradedInMeeting', 'ExtraInfo')

class ApplicationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["experience"].widget.attrs.update({'class':'form-control form-control-lg mb-2'})

    course_list = Course.objects.all()
    selected_course = forms.ModelChoiceField(label="Select A Course to Apply For.", queryset=Course.objects.all())
    resume = forms.FileField(label="Upload a resume here.", required=False)
    experience = forms.CharField(label="Describe your previous experience with the course, including any grades you may have recieved.", widget=forms.Textarea)

    experience.widget.attrs.update(size="30")
    class Meta:
        model = Application
        fields = ["selected_course", "experience", "resume"]
        # widgets = {
        #         'selected_course': Select(choices=course_list),
        #         'experience': forms.TextInput(),
        #         'resume': forms.FileInput(),
        #         }

