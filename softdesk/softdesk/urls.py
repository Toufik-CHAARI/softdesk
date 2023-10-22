from django.contrib import admin
from django.urls import path,include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication import views as auth_views
from project_management import views

urlpatterns = [
    path("admin/", admin.site.urls),    
    path('api/', include('project_management.urls')),    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('api/register/', auth_views.register, name='api_register'),    
    path('api/getuserdata/', auth_views.getUserData, name='get_data'),
    path('api/user_detail/<int:user_id>/', auth_views.user_detail, name='user_detail'),    
]
