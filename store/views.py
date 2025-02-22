from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet ,GenericViewSet
from rest_framework import status
from rest_framework.mixins import CreateModelMixin ,RetrieveModelMixin, DestroyModelMixin , UpdateModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated ,AllowAny


from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Cart, CartItem, OrderItem, Product,Collection, Review, Customer
from .serializers import CartSerializer, CustomerSerializer, ProductSerializer,CollcetionSerializer, Reviewserializer , CartItemsSerializer,AddCartItemserializer, UpdateCartItemSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title','description']
    ordering_fields = ['unit-price', 'last_update']

    def get_serializer_context(self):
        return {'request' : self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({'error' : 'producr can not deleted'},status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    #--------------------------------------------------------------------
    # filterset_fields = ['collection_id'] 
    
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id = collection_id)
    #     return queryset
    # def delete(self , request, pk):
    #     product = get_object_or_404(Product , pk = pk)
    #     product.delete()
    #     return Response(status = status.HTTP_204_NO_CONTENT)
    #--------------------------------------------------------------------

class CollectionVeiwSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        product_count = Count('products')
    )
    serializer_class = CollcetionSerializer

    def delete(self , reqeust , pk):
        collection = get_object_or_404(Collection , pk = pk)
        if collection.products.count() > 0:
            return Response({'error' : 'this collection can not deleted'} , status = status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class ReviewsViewSet(ModelViewSet):
    serializer_class = Reviewserializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']}

class CartViewSet(CreateModelMixin , GenericViewSet , RetrieveModelMixin , DestroyModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get' , 'patch' , 'post' , 'delete']
    
    def get_serializer_context(self):
        return {'cart_id' : self.kwargs['cart_pk']}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemserializer
        if self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemsSerializer
    
    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id = self.kwargs['cart_pk'])\
            .select_related('product')
            

class CustomerViewSet(CreateModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      GenericViewSet):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    #eede
    @action(detail = False , methods = ['GET' , 'PUT'])
    def me(self,request):
        (customer,created) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer , data = request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)