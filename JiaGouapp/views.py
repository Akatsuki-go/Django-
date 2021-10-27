from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from JiaGouapp.models import goods, price, Cm, four, kinds, lou, user, collect, address, order, cart, business
from JiaGouapp.serializers import GoodsSerializers, PriceSerializers, CmSerializers, FourSerializers, KindsSerializers, \
    LouSerializers, UserSerializers, CollectSerializers, GoodsListSerializers, AdderssSerializers, OrderSerializers, \
    CartSerializers, BusinessSerializer, PutAdderssSerializers

'''
自定义工具方法
'''


# 根据userid获得user对象
def get_userid(userid):
    out = user.objects.get(userid=userid)
    return out


# 删除字典中‘userid’
def det_userid(dcit):
    del dcit['userid']
    return dcit


# 判断userid存不存在
def judgeUser(userid):
    u = user.objects.get(userid=userid)
    if u is None:
        return False
    else:
        return True


class GoodsModelViewSet(ModelViewSet):
    queryset = goods.objects.all()
    serializer_class = GoodsSerializers

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     return Response()
    def create(self, request, *args, **kwargs):
        if (goods.objects.filter(request['goods']) is None):
            serlizer = GoodsSerializers(data=request.data);
            serlizer.is_valid(raise_exception=True)
            serlizer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response("goods_id已存在")


class PriceModelViewSet(ModelViewSet):
    queryset = price.objects.all()
    serializer_class = PriceSerializers


class ProceSort(APIView):
    pass


class CmModelViewSet(ModelViewSet):
    queryset = Cm.objects.all()
    serializer_class = CmSerializers


class FourModelViewSet(ModelViewSet):
    queryset = four.objects.all()
    serializer_class = FourSerializers


# class LouModelViewSet(ModelViewSet):
#     queryset = lou.objects.all()
#     serializer_class = LouSerializers
# 楼层
class LouModelViewSet(ModelViewSet):
    queryset = goods.objects.all()
    serializer_class = GoodsSerializers

    def list(self, request):
        lous = lou.objects.all()
        title = lous.filter(title=1)
        product = lous.filter(title=0)
        serializer1 = LouSerializers(instance=title, many=True)
        serializer2 = LouSerializers(instance=product, many=True)
        print(serializer1.data)
        print(serializer2.data)
        context = {
            "floor_title": serializer1.data,
            "product_list": serializer2.data
        }
        return Response(context)

    def create(self, request):
        dact = request.data
        serializer = LouSerializers(data=dact)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class KindsListViews(APIView):
    def get(self, request):
        kindset = kinds.objects.all()
        kind1 = kindset.filter(cat_level=0)
        kind2 = kindset.filter(cat_level=1)
        kind3 = kindset.filter(cat_level=2)
        serializer1 = KindsSerializers(instance=kind1, many=True)
        serializer2 = KindsSerializers(instance=kind2, many=True)
        serializer3 = KindsSerializers(instance=kind3, many=True)
        context = {
            "t1": serializer1.data,
            "t2": serializer2.data,
            "t3": serializer3.data,
        }
        return Response(context)

    def post(self, request):
        dact = request.data
        serializer = KindsSerializers(data=dact)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# 用户相关的
class UserView(APIView):
    def post(self, request):
        openid = request.data['userid']
        u = user.objects.filter(userid=openid)
        if u.exists():
            # print("bukong")
            return Response(status=status.HTTP_200_OK)
        else:
            # print("kong")
            serializer = UserSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.is_valid()
            return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        serialzier = UserSerializers(instance=user.objects.all(), many=True)
        return Response(serialzier.data)


# 收藏
class Collect1APIView(APIView):
    def get(self, request):
        collectSet = collect.objects.all()
        serializer = CollectSerializers(instance=collectSet, many=True)
        return Response(serializer.data)

    def post(self, request):
        userid = request.data['userid']
        a = user.objects.filter(userid=userid)
        # print(a[0].id)
        user_id = a[0].id
        goods_id = request.data['goods_id']
        c = collect.objects.filter(user=user_id, goods_id=goods_id)
        # print(c)
        if c.exists():
            return Response("该商品已收藏")
        dict = request.data
        del dict['userid']
        temp = {
            "user": user_id
        }
        dict.update(temp)
        # print(dict)

        serializer = CollectSerializers(data=dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status.HTTP_201_CREATED)


# get/ userid   del/
class Collect2APIView(APIView):
    def get(self, request, pk):
        cuser = user.objects.get(userid=pk)
        collectset = collect.objects.filter(user=cuser)
        # for a in collectset:
        #     print(a.goods_id)
        #     print(a.collecttime)
        serializer = CollectSerializers(instance=collectset, many=True)
        dict = serializer.data
        i = 0
        for a in serializer.data:
            g = goods.objects.get(goods_id=a['goods_id'])
            temp = {
                "goods_price": g.goods_price,
                "goods_name": g.goods_name,
                "goods_small_logo": g.goods_small_logo
            }
            a.update(temp)
            print(a)
            dict[i] = a
            print(dict)
            i = i + 1
        # print(dict)
        return Response(dict)

    def delete(self, request, pk):
        if judgeUser(pk):
            id = request.data['collect_id']
            c = collect.objects.get(id=id)
            # print(c)
            c.delete()

            dcit = {
                "status": "ok"
            }
            return Response(dcit, status=status.HTTP_204_NO_CONTENT)
        else:
            Response("userid不存在")


# 商品列表 cat_id---返回某分类的商品信息
class GoodsListViews(APIView):
    def get(self, request, cat_id):
        ansset = goods.objects.filter(cat_id=cat_id)
        serializer = GoodsListSerializers(instance=ansset, many=True)
        print(serializer.data)
        return Response(serializer.data)


# 商品详情
class GoodsAllViews(APIView):
    def get(self, request, pk):
        good = goods.objects.get(goods_id=pk)
        serializer1 = GoodsSerializers(instance=good)
        priceset = price.objects.filter(goods=good)
        serializer2 = PriceSerializers(instance=priceset, many=True)

        context = serializer1.data
        context['price'] = serializer2.data
        return Response(context)


# 地址
class Address1Views(APIView):
    def get(self, request):
        Set = address.objects.all()
        serializer = AdderssSerializers(instance=Set, many=True)
        return Response(serializer.data)

    def post(self, request):
        userid = request.data['userid']
        temp = request.data
        # print(userid)
        del temp['userid']
        adduser = user.objects.get(userid=userid)
        dict = {
            'user': adduser.id
        }
        dict.update(temp)
        print(dict)
        serializer = AdderssSerializers(data=dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Address2Views(APIView):
    def get(self, request, pk):
        u = user.objects.get(userid=pk)
        set = address.objects.filter(user=u)
        serializer = AdderssSerializers(instance=set, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        add = address.objects.get(id=pk)
        serializer = PutAdderssSerializers(instance=add, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        if judgeUser(pk):
            address.objects.get(id=request.data['address_id']).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("userid不存在")


# 购物车
class cart1View(APIView):
    def get(self, request):
        Set = cart.objects.all()
        serializer = CartSerializers(instance=Set, many=True)
        dict = serializer.data
        i = 0
        for a in serializer.data:
            u = user.objects.get(id=a['user'])
            temp = {
                "userid": u.userid
            }
            # user的id删除
            del a['user']
            a.update(temp)
            dict[i] = a
            # print(a)
            i = i + 1
        # print(dict)
        return Response(dict)

    def post(self, request):
        u = get_userid(request.data['userid'])
        set = cart.objects.filter(user=u.id, goods_id=request.data['goods_id'])
        # print(set)
        dict = {
            'user': u.id
        }
        temp = det_userid(request.data)
        dict.update(temp)
        # print(dict)
        serializer = CartSerializers(data=dict)
        serializer.is_valid(raise_exception=True)
        # 购物车信息存在时
        if set.exists():
            d = serializer.data
            print(serializer.data)
            temp = {
                "id": set[0].id,
                "staus": "exist"
            }
            d.update(temp)
            return Response(d)
        # 第一次添加时
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class cart2View(APIView):
    def get(self, request, pk):
        u = get_userid(pk)
        set = cart.objects.filter(user=u)
        seriazlier = CartSerializers(instance=set, many=True)
        # print(seriazlier.data)
        dcit = seriazlier.data
        list = []
        for a in dcit:
            a1 = a
            gid = a['goods_id']
            g = goods.objects.get(goods_id=gid)
            temp = {
                'goods_small_logo': g.goods_small_logo,
                'goods_name': g.goods_name,
                'goods_price': g.goods_price
            }
            a1.update(temp)
            list.append(a1)
            # print(a1)

        return Response(list)

    def put(self, request, pk):
        if judgeUser(pk):
            judge = request.data['put']
            c = cart.objects.get(id=request.data['cart_id'])
            if (judge == "+"):
                c.number = c.number + 1
            if (judge == "-"):
                c.number = c.number - 1
            if (judge == "check"):
                c.is_check = not c.is_check
            c.save()
            dict = CartSerializers(instance=c)

            return Response(dict.data, status=status.HTTP_201_CREATED)
        else:
            return Response("不存在")

    # pk是购物车id
    def delete(self, request, pk):
        if judgeUser(pk):
            cu = cart.objects.get(id=request.data['cart_id'])
            cu.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("userid不存在")


class Order1APIViews(APIView):
    def get(self, request):
        Set = order.objects.all()
        serializer = OrderSerializers(instance=Set, many=True)
        return Response(serializer.data)

    def post(self, request):
        userid = user.objects.get(userid=request.data['userid']).id
        print(userid)
        goodsid = goods.objects.get(goods_id=request.data['goods_id']).id
        # print(goodsid)
        dict = {
            "goods_id": goodsid,
            "num": request.data['num'],
            "ordertime": request.data['ordertime'],
            "state": request.data['state'],
            "user": userid
        }
        # print(dict)
        serializer = OrderSerializers(data=dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Order2APIViews(APIView):
    def get(self, request, pk):
        userid = get_userid(pk)
        orderset = order.objects.filter(user=userid)
        # print(orderset)
        serializer = OrderSerializers(instance=orderset, many=True)

        dict = serializer.data
        i = 0
        for a in serializer.data:
            # print(a)
            g = goods.objects.get(id=a['goods_id'])
            temp = {
                "goods_price": g.goods_price,
                "goods_name": g.goods_name,
                "goods_small_logo": g.goods_small_logo
            }
            a.update(temp)
            dict[i] = a
            i = i + 1
        return Response(dict, status=status.HTTP_200_OK)
        # return Response()

    def put(self, request, pk):
        if order.objects.get(id=int(pk)) is not None:
            updataOrder = order.objects.get(id=int(pk))
            dict = {}
            dict['id'] = updataOrder.id
            dict['goods_id'] = updataOrder.goods_id
            dict['num'] = updataOrder.num
            dict['ordertime'] = updataOrder.ordertime
            dict['user_id'] = updataOrder.user_id
            dict['state'] = request.data['state']
            serializer = OrderSerializers(instance=updataOrder, data=dict)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("id对应的订单是空的")

    def delete(self, request, pk):
        if judgeUser(pk):
            order.objects.get(id=request.data['order_id']).delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("userid不存在")


# 搜索
class SearchGoodsViews(APIView):
    def get(self, request, pk):
        print(pk)
        set = goods.objects.filter(goods_name__contains=pk)
        list = []
        for a in set:
            dict = {}
            dict["goods_id"] = a.goods_id
            dict["goods_name"] = a.goods_name
            list.append(dict)
        # print(list)
        return Response(list)


'''
商家网站
'''


# 商家注册
class register(APIView):
    # 账号名只由字母、中文和下划线
    def post(self, request):
        buser = business.objects.filter(name=request.data['name'])
        if buser is not None:
            return Response("用户名已注册")
        else:
            serializer = BusinessSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


# 商家登录
class login(APIView):
    def post(self, request):
        name = request.data['name']
        password = request.data['password']
        b = business.objects.get(name=name)
        if b is not None:
            if b.password == password:
                return Response("登录成功")
            else:
                return Response("登录失败")
        else:
            return Response("登录失败")


# 按价格排序
# cartid->set--sort-->newSet
# sortF=0 :从大到小， 1：从小到大
class priceSort(APIView):
    def get(self, request, cat_id, sortF):
        if (sortF is "1"):
            set = goods.objects.filter(cat_id=cat_id).order_by('goods_price')
        if (sortF is "0"):
            set = goods.objects.filter(cat_id=cat_id).order_by('-goods_price')

        len = set.count()
        i = 0
        list = []
        while i < len:
            dict = {}
            dict['goods_id'] = set[i].goods_id
            dict['goods_small_logo'] = set[i].goods_small_logo
            dict['goods_name'] = set[i].goods_name
            dict['goods_price'] = set[i].goods_price
            list.append(dict)
            i += 1

        return Response(list)
