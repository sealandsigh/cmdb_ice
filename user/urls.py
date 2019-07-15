from django.urls import path
from user import views

app_name='user'

urlpatterns = [
    path('index/',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('delete/',views.delete,name='delete'),
    path('view/',views.view,name='view'),
    path('update/',views.update,name='update'),
    path('addview/',views.addview,name='addview'),
    path('add/',views.add,name='add'),
    path('passwordview/',views.passwordview,name='passwordview'),
    path('password/',views.password,name='password'),
    path('accesslog/',views.accesslog,name='accesslog'),
    path('add/ajax/',views.add_ajax,name='add_ajax'),
    path('delete/ajax',views.delete_ajax,name='delete_ajax'),
    path('view/ajax',views.view_ajax,name='view_ajax'),
    path('update/ajax',views.update_ajax,name='update_ajax'),
    path('password/ajax',views.password_ajax,name='password_ajax'),
]
