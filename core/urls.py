from django.urls import path
from .views import landing_page
from .views import project_detail
from .views import client_detail
from .views import ai_chat


urlpatterns = [
    path('', landing_page, name='home'),
    path('project/<int:id>/', project_detail, name='project_detail'),
    path('client/<int:id>/', client_detail, name='client_detail'),
    path("ai-chat/", ai_chat, name="ai_chat"),


]


