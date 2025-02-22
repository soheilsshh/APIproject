from decimal import Decimal
from rest_framework import serializers
from .models import Cart, Customer, Product ,Collection,Review ,CartItem

class CollcetionSerializer(serializers.ModelSerializer): #serializer.Serializer
    class Meta:
        model = Collection
        fields = ['id' , 'title','product_count'] # we can use fields = '__all__' this is bad way
        
    product_count = serializers.IntegerField()
        
        
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' ,'title','unit_price','collection','price_with_tax' , 'slug' ,'description' ,'inventory']
        #collection = Collectionserializer() this way for nested token

    price_with_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')


    
    def calculate_tax(self , product:Product ): #python dont know product type so we must defin it with :Product
        return product.unit_price * Decimal(1.1)


class Reviewserializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id' , 'date' , 'name' , 'description']
        
    def create(self, validated_data): # this is important impliment for this code
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id , **validated_data)
    
class CartProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']
    
class CartItemsSerializer(serializers.ModelSerializer):
    product = CartProductItemSerializer()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity','total_price']
        
        
    def get_total_price(self ,cartItem):
        return cartItem.quantity * cartItem.product.unit_price

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    items = CartItemsSerializer(many = True, read_only = True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    
    class Meta:
        model = Cart 
        fields = ['id' , 'items','total_price']
        


class AddCartItemserializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def validate_product_id(self,value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('no product with the given id was found.')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            cart_item = CartItem.objects.get(cart_id = cart_id , product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id , **self.validated_data) 
        
        return self.instance
            
    class Meta:
        model = CartItem
        fields = ['id' , 'product_id' , 'quantity']
        
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
        

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)
    
    class Meta:
        model = Customer
        fields = ['id' , 'user_id' ,'membership' , 'phone' , 'birth_date']