from django.urls import path
from .views import SupplementListView, UserSupplementListCreateView, UserSupplementLogListCreateView, UserSupplementLogDeleteView, UserSupplementLogTodayView        

urlpatterns = [
    path('list/', SupplementListView.as_view(), name='supplement-list'),
    path('user/list/', UserSupplementListCreateView.as_view(), name='user-supplement-list'),
    path('user/add/', UserSupplementListCreateView.as_view(), name='user-supplement-add'),
    path('user/log/list/', UserSupplementLogListCreateView.as_view(), name='user-supplement-log-list'),
    path('user/log/add/', UserSupplementLogListCreateView.as_view(), name='user-supplement-log-add'),
    path('user/log/today/', UserSupplementLogTodayView.as_view(), name='user-supplement-log-today'),
    path('user/log/delete/<int:log_id>/', UserSupplementLogDeleteView.as_view(), name='user-supplement-log-delete'),
]











