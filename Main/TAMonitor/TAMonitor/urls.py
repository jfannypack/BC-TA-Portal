"""TAMonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("django.contrib.auth.urls")),
    path('', view.home, name='home'),
    path('accounts/',include("django.contrib.auth.urls")),
    path('register/', view.register, name='register'),
    path('studentregister/', view.studentregister, name='studentregister'),
    path('instructorregister/', view.instructorregister, name='instructorregister'),
    path('adminregister/', view.adminregister, name='adminregister'),
    path('createcourse/', view.createcourse.as_view(success_url="/"), name='createcourse'),
    path('courseupdate/<int:pk>', view.courseupdate.as_view(success_url="/"), name='courseupdate'),
    path('coursedetail/<int:pk>', view.coursedetailview.as_view(), name="coursedetail"),
    path('applictionview/<int:pk>', view.applicationview.as_view(), name="applicationview"),
    path('allapplications/', view.applicationoverview, name="applicationoverview"),
    path('studentapplications/', view.studentapplicationsview, name="studentapplicationsview"),
    path('acceptapp/<int:pk>', view.accept_application, name="acceptapp"),
    path('rejectapp/<int:pk>', view.reject_application, name="rejectapp"),
    path('apply/', view.apply, name='apply'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
