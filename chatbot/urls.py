from django.urls import path
from . import views

urlpatterns = [
   path('chatbot/user_data', views.handle_user_data, name='user-data'),
   path('chatbot/get_user_data_scoring_list/', views.UserScoringList.as_view(), name='get-user-data-scoring-list'),
   path('chatbot/get_single_user_data_scoring/<int:user_id>/', views.UserScoringDetail.as_view(), name='get-single_user-data-scoring')
]
