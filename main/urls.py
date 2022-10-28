from django.urls import path
from main import views
app_name = 'main'
urlpatterns = [
    path('', views.VisitListView.as_view(), name='visit_all'),
    path('<int:pk>/', views.VisitDetailView.as_view(), name='visit_detail'),
    path('create/', views.VisitCreateView.as_view(), name='visit_create'),
    path('<int:pk>/update/', views.VisitUpdateView.as_view(), 
            name='visit_update'),
    path('<int:pk>/delete/', views.VisitDeleteView.as_view(), 
            name='visit_delete'),

    path('services/', views.ServiceListView.as_view(), name='service_all'),
    path('service/<int:pk>', views.ServiceDetailView.as_view(), 
            name='service_detail'),
    path('service/create/', views.ServiceCreateView.as_view(), 
            name='service_create'),
    path('service/<int:pk>/update/', views.ServiceUpdateView.as_view(), 
            name='service_update'),
    path('service/<int:pk>/delete/', views.ServiceDeleteView.as_view(), 
            name='service_delete'),
]