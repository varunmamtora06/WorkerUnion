from rest_framework import serializers,exceptions
from .models import blog
from django.contrib.auth import models,authenticate
#can also write from django.contrib.auth.models import User

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = blog
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name','last_name','username','email','password']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        username = data.get("username","")
        password = data.get("password","")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Can't Login"
                raise exceptions.ValidationError(msg)
        else:
            msg="Must provide username and password both"
            raise exceptions.ValidationError(msg)
        return data

class RegisterSerializer(serializers.Serializer):
    fname = serializers.CharField()
    lname = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self,data):
        fname =  data.get("fname","")
        lname = data.get("lname","")
        username =  data.get("username","")
        email = data.get("email","")
        password1 =  data.get("password1","")
        password2 =  data.get("password2","")

        if password1 == password2:
            if models.User.objects.filter(username=username).exists():
                msg = "Username exists"
                raise exceptions.ValidationError(msg)
            elif models.User.objects.filter(email=email).exists():
                msg = "email exists"
                raise exceptions.ValidationError(msg)
            else:
                user = models.User.objects.create_user(
                    username=username, email=email, password=password1, first_name=fname, last_name=lname)
                # user.save()
                data["user"]=user
        else:
            msg = "Passwords didnt match"
            raise exceptions.ValidationError(msg)
        return data
