from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import SimpleRouter, DefaultRouter

from JiaGouapp import views

urlpatterns = [
    path('docs/', include_docs_urls(title='My API docs')),
    # path('lou/', views.LouListViews.as_view()),
    path('kinds/', views.KindsListViews.as_view()),
    path('goodsList/<int:cat_id>/', views.GoodsListViews.as_view()),
    path('order/', views.Order1APIViews.as_view()),
    path('order/<str:pk>/', views.Order2APIViews.as_view()),
    path('goodsall/<str:pk>/', views.GoodsAllViews.as_view()),
    path('collect/', views.Collect1APIView.as_view()),
    path('collect/<str:pk>/', views.Collect2APIView.as_view()),
    path('address/', views.Address1Views.as_view()),
    path('address/<str:pk>/', views.Address2Views.as_view()),
    path('cart/', views.cart1View.as_view()),
    path('cart/<str:pk>/', views.cart2View.as_view()),
    path('user/', views.UserView.as_view()),
    path('search/<str:pk>/', views.SearchGoodsViews.as_view()),

    path('register/', views.register.as_view()),
    path('login/', views.login.as_view()),
    path('priceSort/<str:cat_id>/sortF=<str:sortF>', views.priceSort.as_view()),
]
# 1,创建路由对象
router = SimpleRouter()
# 商品详情
router.register('goods', views.GoodsModelViewSet)
router.register('price', views.PriceModelViewSet)
router.register('Cm', views.CmModelViewSet)
router.register('four', views.FourModelViewSet)
router.register('lou', views.LouModelViewSet)
# router.register('user', views.UserModelViewSet)
urlpatterns += router.urls

# 3,输出结果
# print(urlpatterns)
