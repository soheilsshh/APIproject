from djoser.serializers import UserCreateSerializer as BeaseUserCreateSerializer,UserSerializer

class UserCreateSerializer(BeaseUserCreateSerializer):
    class Meta(BeaseUserCreateSerializer.Meta):
        fields = ['id','username' , 'password' , 'email' , 'first_name' , 'last_name']

class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id','username','first_name','last_name','email']