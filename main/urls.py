from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='main'), 
    path('sign_in', views.sign_in, name='sign_in'), 
    path('sign_up', views.sign_up, name='sign_up'), 
    path('logout', views.log_out, name='logout'), 
    path('edit_info', views.edit_info, name='edit_info'), 
    path('settings', views.settings, name='settings'),
    path('search_person', views.SearchPersonView.as_view(), name='search_person'), 
    path('send_message', views.SendMessageView.as_view(), name='send_message'),
    path('get_messages', views.GetMessagesView.as_view(), name='get_messages'),
    path('block_user', views.BlockUserView.as_view(), name='block_user'),
    path('unblock_user', views.UnblockUserView.as_view(), name='unblock_user'),
    path('clear_history', views.ClearHistoryView.as_view(), name='clear_history')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
