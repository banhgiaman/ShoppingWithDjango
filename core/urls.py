from django.urls import path, include
from .views import IndexView, ContactView, ProductDetail, ProductComments, AddComment, Register, Register_Success


from django.contrib.auth import views as auth_views


app_name = 'core'
urlpatterns = [
    path('', IndexView, name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('product/<int:product_id>', ProductDetail, name='product'),
    path('product/<int:product_id>/comments', ProductComments, name='product_comments'),
    path('product/<int:product_id>/addcmt', AddComment, name='add_comment'),

    path('register/', Register, name='register'),
    path('register/regist', Register_Success, name='register_success'),

    path('login/', auth_views.LoginView.as_view(template_name='homepage/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

urlpatterns += [
    path('', include('django.contrib.auth.urls')),
]