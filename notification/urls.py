
from django.urls import path
from .views import notificationApi , notificationorder  ,OrderComplete 

urlpatterns = [
    path('notification/', notificationApi.as_view(), name='notification'),
    path('readmessage/', notificationApi.as_view(), name='readmessage'),
    path('order/', notificationorder.as_view(), name='order'),
    # path('order/<int:id>/', notiorderid.as_view(), name='orderid'),
    path('order/<int:id>/status/', OrderComplete.as_view(), name='orderidcomplete'),
]
