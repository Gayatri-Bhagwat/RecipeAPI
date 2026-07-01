"""
url mappings for the user API
"""
from django.urls import path
from user import views
from user.views import ForgotPasswordView, LogOutView

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.TokenUserView.as_view(), name="login"),
    path("update/", views.ManageUserView.as_view(), name="update"),
    path("refresh/", views.RefreshTokenView.as_view(), name="refresh"),

    path("<str:email>/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),

    path("logout/", LogOutView.as_view(), name="logout"),
]
