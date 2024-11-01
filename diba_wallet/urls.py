from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def working(request):
    return HttpResponse("Up and Running!")

urlpatterns = [
    path("", working),
    path('admin/', admin.site.urls),
    path('api/', include('wallet.urls')),
]


