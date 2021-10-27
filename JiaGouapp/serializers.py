from rest_framework import serializers
from JiaGouapp.models import goods, price, Cm, four, kinds, lou, user, collect, order, address, cart,business
from rest_framework.viewsets import ModelViewSet
import re
class GoodsSerializers(serializers.ModelSerializer):
    class Meta:
        model = goods
        fields = "__all__"

class PriceSerializers(serializers.ModelSerializer):
    class Meta:
        model = price
        fields = "__all__"

class CmSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cm
        fields = "__all__"

class FourSerializers(serializers.ModelSerializer):
    class Meta:
        model = four
        fields = "__all__"
class LouSerializers(serializers.ModelSerializer):
    class Meta:
        model = lou
        fields = "__all__"
class KindsSerializers(serializers.ModelSerializer):
    class Meta:
        model = kinds
        fields = "__all__"

#与用户有关的使用信息
#用户
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=user
        fields="__all__"

class CollectSerializers(serializers.ModelSerializer):
    class Meta:
        model=collect
        fields="__all__"

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model=order
        fields="__all__"

class AdderssSerializers(serializers.ModelSerializer):
    class Meta:
        model=address
        fields="__all__"
class PutAdderssSerializers(serializers.ModelSerializer):
    isChecked=serializers.BooleanField()
    class Meta:
        model=address
        fields = ['isChecked']
    # userid = models.CharField(max_length=100)
#商品列表
class GoodsListSerializers(serializers.ModelSerializer):
    class Meta:
        model=goods
        fields=['goods_id','goods_small_logo','goods_name','goods_price']

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model=cart
        fields="__all__"

#商家账号
class BusinessSerializer(serializers.Serializer):
    #用户名长度6-10
    name=serializers.CharField(max_length=10,min_length=6)
    #密码长度8-16
    passworld=serializers.CharField(min_length=8,max_length=16)
    def validate_name(self,value):
        #账号由字母和数字以及下划线组成，长度6-10
        if re.match('^[a-zA-Z0-9_]{6,10}$', value):
            return value
        else:
            raise serializers.ValidationError("密码只能有数字、字母和下划线组成")

    def validate_passworld(self, values):
        #密码不包含特殊字符，长度8-16
        if re.match('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$',values):
            return values
        else:
            raise serializers.ValidationError("不包含特殊符号")

    def create(self, validated_data):
        b=business.objects.create(**validated_data)
        return b

    def update(self, instance, validated_data):
        pass