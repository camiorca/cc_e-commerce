from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

from api.products.views import RegisterAPI, LoginAPI, ProductViewSet, CreditCardViewSet, PurchaseViewSet, OrderViewSet
from api.products import views
from knox import views as knox_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/v1/products', ProductViewSet)
router.register(r'api/v1/creditcards', CreditCardViewSet, basename='creditcards')
router.register(r'api/v1/vieworders', OrderViewSet, basename='vieworders')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/v1/register/', RegisterAPI.as_view(), name='register'),
    path('api/v1/login/', LoginAPI.as_view(), name='login'),
    path('api/v1/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/v1/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/v1/order/', PurchaseViewSet.as_view(), name='order'),
    path('docs/', include_docs_urls(title='Code Challenge API'))
]
