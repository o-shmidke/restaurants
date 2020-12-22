from django.urls import path

from analytics.views import get_data, view_data

app_name = 'data_analysis'
urlpatterns = [
    path('get_data', get_data, name='get_data'),
    path('view_data', view_data, name='view_data'),

]
