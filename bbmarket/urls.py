from django.urls import path, include

urlpatterns = [
    path('bbmarket', include('products.urls')),
    path('bbmarket', include('users.urls')),
]
