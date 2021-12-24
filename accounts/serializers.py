from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from accounts.models import CustomUser
from accounts.utils import get_user
from legendarymotosports.utils import delete_files, prepare_form_data


class RegisterSerializer(serializers.Serializer):

    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)
    image = serializers.ImageField(required=False)

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')

        errors = {}

        if CustomUser.objects.filter(email=email).exists():
            msg = "*user with this email already exists"
            errors['email'] = msg
        
        if CustomUser.objects.filter(username=username).exists():
            msg = "*user with this username already exists"
            errors['username'] = msg
        
        if not password == password_confirm:
            msg = "*passwords does not match"
            errors['password'] = msg

        if errors:
            self.validation_errors = errors
            raise serializers.ValidationError()

        return super().validate(attrs)


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        errors = {}

        try:
            user = CustomUser.objects.get(email=email) 
        except ObjectDoesNotExist:
            msg = 'User with this email does not exists'
            errors['email'] = msg
            self.validation_errors = errors
            raise serializers.ValidationError()

        if not user.is_active:
            msg = 'User is not active, activate account in your email or press on this message to redirect'
            errors['not_active'] = msg
            errors['redirect_email'] = user.email
            self.validation_errors = errors
            raise serializers.ValidationError()

        if not check_password(password, user.password):
            msg = 'Wrong password'
            errors['password'] = msg
            self.validation_errors = errors
            raise serializers.ValidationError()
        
        attrs['user'] = user
        
        return super().validate(attrs)


class CodeActivationSerializer(serializers.Serializer):

    email = serializers.EmailField()
    activation_code = serializers.CharField()

    @staticmethod
    def set_active(user):
        user.is_active = True
        user.activation_code = ''
        user.save()


    def validate(self, attrs):
        
        email = attrs.get('email')
        activation_code = attrs.get('activation_code')
        
        errors = {}

        if email and activation_code:
            try:
                user = CustomUser.objects.get(email=email)
                if user.is_active:
                    return super().validate(attrs)
            except ObjectDoesNotExist:
                errors['error'] = 'User Not found'
            else:
                if not user.activation_code == activation_code:
                    errors['error'] = 'Wrong activation code'
        else:
            errors['error'] = 'No email or activation code provided'

        if errors:
            self.validation_errors = errors
            raise serializers.ValidationError()
        return super().validate(attrs)


class AccountEditSerializer(serializers.Serializer):

    email = serializers.EmailField()
    current_password = serializers.CharField()
    new_username = serializers.CharField(required=False, allow_blank=True)
    new_password = serializers.CharField(required=False, allow_blank=True)
    new_password_confirm = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(
        required=False, allow_null=True,
        allow_empty_file=True,
    )


    @staticmethod
    def get_data(request) -> dict:
        """ 
        To prevent validation error it put some default data, 
        unnecessary of which will be cleaned in validate function. 
        """
        clean_data = prepare_form_data(request.data)
        user = get_user(request)

        s_data = {
            'email': user.email,
        }
        s_data.update(clean_data)
        
        s_data = dict(filter(lambda items: bool(items[1]), s_data.items())) # removing keys with no value
        
        # # to prevent error occured by 'blank image'
        # if not s_data['image']:
        #     del s_data['image']
        return s_data


    def validate(self, attrs):
        
        email = attrs.pop('email')
        new_username = attrs.get('new_username')
        current_password = attrs.pop('current_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.pop('new_password_confirm', None)

        errors = dict()
        
        if not email:
            msg = '*some error occured, try to login again'
            errors['other'] = msg
            self.validation_errors = errors
            raise serializers.ValidationError()
        
        try:
            user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            msg = '*some error occured, user cannot be found'
            errors['other'] = msg
            self.validation_errors = errors
            raise serializers.ValidationError()



        if new_username and CustomUser.objects.filter(username=new_username).exists():
            msg = '*user with this username already exists'
            errors['username'] = msg

        if not check_password(current_password, user.password):
            msg = '*entered password incorrect'
            errors['current_password'] = msg
        
        if new_password or new_password_confirm:
            if new_password != new_password_confirm:
                msg = '*passwords does not match'
                errors['password'] = msg

        if errors:
            self.validation_errors = errors
            raise serializers.ValidationError()

        return super().validate(attrs)
    
    @staticmethod
    def put_changes(user, new_data):
        
        password = new_data.get('new_password')
        image = new_data.get('image')
        username = new_data.get('new_username')

        if password:
            user.set_password(password)
        
        if image: 
            delete_files(user)
            user.image = image
        
        if username:
            user.username = username
        
        user.save()


# class ResendActivationCodeSerializer(serializers.Serializer):

#     email = serializers.EmailField()

#     def validate(self, attrs):
#         email = attrs.get('email')
#         errors = {}

#         try:
#             CustomUser.objects.get(email=email)
#         except ObjectDoesNotExist:
#             errors['user'] = "User with this email does not exists"
        
#         if errors:
#             self.validation_errors = errors
#             raise ValidationError()
#         return super().validate(attrs)

