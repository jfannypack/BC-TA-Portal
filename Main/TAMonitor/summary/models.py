from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class Account(AbstractUser):
    email = models.EmailField(('email address'), max_length=64, unique=True)
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    username = models.CharField(max_length=20, unique=False, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
      return self.email

class Application(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, primary_key=False)
    SelectedCourse = models.ForeignKey('Course', on_delete=models.CASCADE, primary_key=False)
    # SelectedCourse = models.CharField(max_length=255)
    Experience = models.CharField(max_length=4096)
    Resume = models.FileField(upload_to="resumes", default='', blank=True)

    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Available',
    )

    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Applications")


    def __str__(self):
        return 'TA-Application-' + str(self.account.email) + '-' + self.SelectedCourse.CourseID

class Student(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    email = models.EmailField(max_length=40)
    YEAR_IN_SCHOOL = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]

    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL,
        default='Freshman',
    )

    OPEN_TO_WORK = [
        ('YES', 'Open to work'),
        ('NO', 'Not open to work'),
    ]

    major = models.CharField(max_length=64)
    eagleid = models.CharField(max_length=16)
    work = models.CharField(max_length=16, choices=OPEN_TO_WORK, default='Open to work')
    applications = models.ManyToManyField(Application, default='', blank=True)

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
      return self.email

class Instructor(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    position = models.CharField(max_length=255) # e.g CS Professor
    email = models.EmailField(max_length=40)

    class Meta:
        verbose_name = _("Instructor")
        verbose_name_plural = _("Instructors")

    def __str__(self):
      return self.email

class Admin(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    email = models.EmailField(max_length=40)
    position = models.CharField(max_length=255) # e.g IT Admin

    class Meta:
        verbose_name = _("Admin")
        verbose_name_plural = _("Admins")

    def __str__(self):
      return self.email

class Course(models.Model):
    Instructor  = models.ForeignKey(Instructor, on_delete=models.CASCADE, primary_key=False)
    CourseID    = models.CharField(max_length=255)
    Name        = models.CharField(max_length=255)
    # Instructor  = models.CharField(max_length=255)
    Description = models.CharField(max_length=2056, null=True)
    SeatData    = models.CharField(max_length=255)
    Rooms       = models.CharField(max_length=255)
    Times       = models.CharField(max_length=255)
    TAs = models.IntegerField(null=True)
    WithDiscussion = models.BooleanField()
    GradedInMeeting = models.BooleanField()
    OfficeHours = models.IntegerField(null=True)
    ExtraInfo   = models.CharField(max_length=2056, null=True)
    Applications = models.ManyToManyField(Application, default='', blank=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
      return self.CourseID


