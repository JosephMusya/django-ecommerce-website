from django.urls import path
from . import views
from  django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('login/', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerUser, name='register'),
    path('add-item/', views.addItem, name='add-item'),
    path('view-item/', views.viewItem, name='view-item'),
    path('edit-item/<str:pk>', views.editItem, name = 'edit-item'),
    path('view-category/<str:pk>', views.viewCategory, name = 'view-category'),
    path('item/<str:pk>', views.viewSingle, name = 'view-single'),
    path('add-to-cart', views.addCart, name='add-to-cart'),
    path('view-cart', views.viewCart, name='view-cart'),
    path('edit-cart', views.editCart, name='edit-cart'),
    path('delete-item-cart', views.remove, name='delete'),
    path('checkout', views.checkout, name='checkout'),
    path('place-order', views.placeOrder, name='place-order'), 
    path('order-history', views.orderHistory, name='order-history'),
    path('view-history/<str:pk>', views.viewHistory, name ='view-history'),
    path('prod-list', views.prodList, name='prod-list'),
    path('main', views.dispCart, name='main')     
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)