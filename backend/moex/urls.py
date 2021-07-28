from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import home, IssuerView, SecurityView, PriceView, PortfolioView
from .dash.home import layout as home_layout
from .dash.home import callbacks as home_callbacks


router = routers.DefaultRouter()
router.register(r'issuers', IssuerView)
router.register(r'securities', SecurityView)
router.register(r'prices', PriceView)
router.register(r'portfolio', PortfolioView)

urlpatterns = [
    path('home/', home),
    path('api/', include(router.urls)),
]
