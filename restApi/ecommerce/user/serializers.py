from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ecommerce.utils.password_regex_validation import \
    password_regex_validation
from ecommerce.utils.name_formatter import name_format
from ecommerce.user.models import Address


User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    street = serializers.CharField(max_length=255)
    class Meta:
        model = Address
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'cpf',
            'phone_number', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class CustomRegisterSerializer(serializers.Serializer):
    address = AddressSerializer()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with this email already exists."
            )
        ]
    )
    cpf = serializers.CharField(
        max_length=11,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with this CPF already exists."
            )
        ]
    )
    phone_number = serializers.CharField(max_length=20)
    password1 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        fields = ["street"]
    
    def validate_first_name(self, first_name):
        first_name = name_format(first_name)
        return first_name

    def validate_last_name(self, last_name):
        last_name = name_format(last_name)
        return last_name

    def validate_cpf(self, cpf):
        return cpf

    def validate_phone_number(self, phone_number):
        return phone_number

    def validate_password1(self, password1):
        if not password_regex_validation(password1):
            raise serializers.ValidationError(
                ("""Password should contain at least one digit,
                one lowercase letter
                one uppercase letter
                one special character (!@#$%^&*()-_=+{};:,<.>/?)
                not contain any whitespace"
                have a minimum length of 8 characters.""")
            )

        return password1

    def validate_password2(self, password2):
        password1 = self.context['request'].data['password1']
        if password1 != password2:
            raise serializers.ValidationError(
                "The two password fields didn't match."
            )
        return password2

    def create(self, validated_data):
        validated_data['password'] = validated_data['password1']
        del validated_data['password1']
        del validated_data['password2']
        
        address = Address.objects.create(**validated_data['address'])
        validated_data['address'] = address
        user = User.objects.create_user(**validated_data)
        return user


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        attrs['user'] = user
        return attrs

