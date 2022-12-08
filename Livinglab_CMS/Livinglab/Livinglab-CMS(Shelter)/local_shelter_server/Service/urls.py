from django.urls import path
from . import views

# app_name = "Service"

urlpatterns = [

    # path 뒤 name이 템플릿에서 href url 경로를 지정해줄 이름이다.
    path('', views.Idle, name='Idle'),
    path('signage/', views.signageView, name='signage'),
    path('contentDetailView/<int:id>', views.contentDetailView, name="contentDetailView"),
    path('ContentLike/<int:id>', views.ContentLike, name="ContentLike"),

    path('community/', views.community, name="community"),
    path('IssueBoard/', views.IssueBoard, name="IssueBoard"),
    path('DailyBoard/', views.DailyBoard, name="DailyBoard"),

    path('paint', views.paint, name='paint'),
    path('paintlist', views.paintlist, name='paintlist'),
    path('ViewPaint/<int:id>', views.ViewPaint, name="ViewPaint"),
]
