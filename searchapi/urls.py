from django.urls import path

from .views import auth, comments

urlpatterns = [
    path('register', auth.RegisterView.as_view()),
    path('login', auth.LoginView.as_view()),
    path('user', auth.UserView.as_view()),
    path('logout', auth.LogoutView.as_view()),
    path('comments/', comments.CommentListView.as_view()),
    path('comments/<int:pk>', comments.CommentDetailView.as_view()),
]