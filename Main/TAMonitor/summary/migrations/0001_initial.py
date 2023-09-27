# Generated by Django 4.1.7 on 2023-05-02 21:00

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=64, unique=True, verbose_name='email address')),
                ('is_student', models.BooleanField(default=False)),
                ('is_instructor', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('username', models.CharField(default='', max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Experience', models.CharField(max_length=4096)),
                ('Resume', models.FileField(blank=True, default='', upload_to='resumes')),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Unavailable', 'Unavailable'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Available', max_length=15)),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('firstname', models.CharField(max_length=64)),
                ('lastname', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=40)),
                ('position', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Admins',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('firstname', models.CharField(max_length=64)),
                ('lastname', models.CharField(max_length=64)),
                ('position', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=40)),
            ],
            options={
                'verbose_name': 'Instructor',
                'verbose_name_plural': 'Instructors',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CourseID', models.CharField(max_length=255)),
                ('Name', models.CharField(max_length=255)),
                ('Description', models.CharField(max_length=2056, null=True)),
                ('SeatData', models.CharField(max_length=255)),
                ('Rooms', models.CharField(max_length=255)),
                ('Times', models.CharField(max_length=255)),
                ('TAs', models.IntegerField(null=True)),
                ('WithDiscussion', models.BooleanField()),
                ('GradedInMeeting', models.BooleanField()),
                ('OfficeHours', models.IntegerField(null=True)),
                ('ExtraInfo', models.CharField(max_length=2056, null=True)),
                ('Applications', models.ManyToManyField(blank=True, default='', to='summary.application')),
                ('Instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='summary.instructor')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.AddField(
            model_name='application',
            name='SelectedCourse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='summary.course'),
        ),
        migrations.AddField(
            model_name='application',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('firstname', models.CharField(max_length=64)),
                ('lastname', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=40)),
                ('year_in_school', models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate')], default='Freshman', max_length=2)),
                ('major', models.CharField(max_length=64)),
                ('eagleid', models.CharField(max_length=16)),
                ('work', models.CharField(choices=[('YES', 'Open to work'), ('NO', 'Not open to work')], default='Open to work', max_length=16)),
                ('applications', models.ManyToManyField(blank=True, default='', to='summary.application')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
    ]
