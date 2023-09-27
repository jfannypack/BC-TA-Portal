from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import admin
from django.template.defaulttags import register
from django.urls import path, include
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
import os
from django.core.mail import send_mail

from .forms import StudentRegisterForm, InstructorRegisterForm, AdminRegisterForm, ApplicationForm, CreateCourseForm
from summary.models import Account, Student, Instructor, Admin, Course, Application

def home(response):
    courses = Course.objects.all()
    return render(response, 'home.html', {'courses':courses})

def applicationoverview(response):
    applications = Application.objects.all()
    return render(response, 'allapplications.html', {'applications':applications})

def studentapplicationsview(response):
    user_email = response.user.email
    applications = Application.objects.filter(account__email=user_email)
    num_applications = len(applications)
    args = {'applications': applications,
            'user_email': user_email,
            'num_applications': num_applications}
    return render(response, 'studentapplications.html', args)

def logout_view(request):
    logout(request)
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

def studentregister(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = StudentRegisterForm()

    context = {'form': form}
    return render(request, 'studentregister.html', context)

def instructorregister(request):
    if request.method == 'POST':
        form = InstructorRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = InstructorRegisterForm()

    context = {'form': form}
    return render(request, 'instructorregister.html', context)

def adminregister(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AdminRegisterForm()

    context = {'form': form}
    return render(request, 'adminregister.html', context)

class createcourse(CreateView):
    model = Course
    fields = ["Instructor", "CourseID", "Name", "Description", "SeatData", "Rooms", "Times", "TAs", "WithDiscussion", "GradedInMeeting", "OfficeHours", "ExtraInfo"]

class courseupdate(UpdateView):
    model = Course
    fields = ["Instructor", "CourseID", "Name", "Description", "SeatData", "Rooms", "Times", "TAs", "WithDiscussion", "GradedInMeeting", "OfficeHours", "ExtraInfo"]
    template_name_suffix = '_update_form'

class coursedetailview(DetailView):
    model = Course

class applicationview(DetailView):
    model = Application

class CreateApplication(CreateView):
    model = Application
    form_class = ApplicationForm()
    template_name = 'application.html'

    def save(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()


def apply(response):
    if response.method == 'POST':
        form = ApplicationForm(response.POST, response.FILES)
        user = response.user
        if user.is_student:
            student = Student.objects.get(email=user.email)
        selected_course = response.POST.get('selected_course')
        course = Course.objects.get(pk=selected_course)
        apps = Application.objects.filter(account=user)
        app_count = len(apps)

        if len(Application.objects.filter(account=user, SelectedCourse=selected_course)) > 0:
            messages.info(response, 'You cannot apply to the same course twice!')

            return redirect('/apply')

        if form.is_valid() and app_count < 5:
            application = Application.objects.create(
                    account = response.user,
                    SelectedCourse = course,
                    Experience = response.POST.get('experience'),
                    Resume = response.FILES['resume'],
                    )
            course.Applications.add(application)
            course.save()
            if user.is_student:
                # Add application to student's list of applications
                student.applications.add(application)
                student.save()
        else:
            print("Application Error")
        return redirect('/')
    else:
        form = ApplicationForm()

    return render(response, 'application.html', {'form':form})


def accept_application(request, pk):
    app = Application.objects.get(pk=pk)
    app.status = 'Accepted'
    app.save()

    send_mail(
    'View your offer',
    f"Dear {app.account.email},\n\n"
    f'Congratulations! Your TA application for {app.SelectedCourse.CourseID} has been accepted! Please check your student TA portal for further instructions. For assistance, please email bctaapp@gmail.com.',
    'bctaapp@gmail.com',
    [app.account.email],
    fail_silently=False
    )   
    return redirect('/allapplications')

def reject_application(request, pk):
    app = Application.objects.get(pk=pk)
    app.status = 'Rejected'
    app.save()
    send_mail(
    f'Update regarding you TA application to {app.SelectedCourse.CourseID}',
    f"Dear {app.account.email},\n\n"
    f'Unfortunately, Your TA application for {app.SelectedCourse.CourseID} has been rejected. Thank you for your application! For assistance, please email bctaapp@gmail.com.',
    'bctaapp@gmail.com',
    [app.account.email],
    fail_silently=False
    ) 
    return redirect('/allapplications')