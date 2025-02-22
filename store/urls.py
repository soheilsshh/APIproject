from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products' , views.ProductViewSet , basename = 'product-detail')
router.register('collections' , views.CollectionVeiwSet)
router.register('carts',views.CartViewSet)
router.register('customer',views.CustomerViewSet)
router.register('order' , views.OrderViewSet , basename = 'orders')

products_router = routers.NestedDefaultRouter(router , 'products' , lookup = 'product')
products_router.register('reviews' , views.ReviewsViewSet , basename = 'products-reviews')

carts_routers = routers.NestedDefaultRouter(router , 'carts' , lookup = 'cart')
carts_routers.register('items' , views.CartItemViewSet , basename = 'cart_item')

# URLConfs
urlpatterns = router.urls + products_router.urls + carts_routers.urls
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>', views.ProductDetail.as_view()),
    # path('collections/' , views.CollectionList.as_view()),
    # path('collections/<int:pk>', views.CollectionDetaile.as_view() , name = 'collcetion-detile'),
