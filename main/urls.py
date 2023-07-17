from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='main'), 
    path('sign_in', views.sign_in, name='sign_in'), 
    path('sign_up', views.sign_up, name='sign_up'), 
    path('logout', views.log_out, name='logout'), 
    path('search_person', views.SearchPersonView.as_view(), name='search_person'), 
    path('send_message', views.SendMessageView.as_view(), name='send_message'),
    path('get_messages', views.GetMessagesView.as_view(), name='get_messages'),
    path('edit_info', views.edit_info, name='edit_info')
]
