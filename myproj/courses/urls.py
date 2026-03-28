from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course-list'),
    path('courses/<int:course_id>/', views.course_detail, name='course-detail'),
    path('courses/<int:course_id>/submit/', views.submit_exam, name='submit-exam'),
    path('submissions/<int:submission_id>/result/', views.exam_result, name='exam-result'),
]
