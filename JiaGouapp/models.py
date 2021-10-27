from django.db import models


# 商品
class goods(models.Model):
    goods_id = models.CharField(max_length=20)
    cat_id = models.CharField(max_length=20)
    goods_small_logo = models.CharField(max_length=200)
    goods_introduce = models.CharField(max_length=5000)
    goods_name = models.CharField(max_length=100)
    goods_number = models.IntegerField(default=0)
    goods_price = models.IntegerField()
    add_time = models.DateTimeField(default=None)
    upd_time = models.DateTimeField(default=None)

    def __str__(self):
        return self.goods_name

# 商品图片 一个商品五张图片
class price(models.Model):
    pics_id = models.CharField(max_length=20)
    # pics_sma = models.CharField(max_length=200)
    pics_mid = models.CharField(max_length=200)
    goods = models.ForeignKey('goods', on_delete=models.CASCADE)
    # pics_big = models.CharField(max_length=200)
    # pgoods_id = models.CharField(max_length=20)
    # goods_id=models.CharField(max_length=20)

# 轮播图
class Cm(models.Model):
    goods_id = models.CharField(max_length=20)
    image_src = models.CharField(max_length=200)
    navigator_url = models.CharField(max_length=200)
    open_type = models.CharField(max_length=20)


# 导航
class four(models.Model):
    name = models.CharField(max_length=20)
    image_src = models.CharField(max_length=200)
    navigator_url = models.CharField(max_length=200, default="")
    open_type = models.CharField(max_length=20, default="")


# 楼层 title
class lou(models.Model):
    # 是不是标题
    title = models.IntegerField(default=0)
    # 分类id
    loukinds = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=20)
    image_src = models.CharField(max_length=200)
    navigator_url = models.CharField(max_length=200, default="")
    open_type = models.CharField(max_length=20, default="")


# 分类信息
class kinds(models.Model):
    # 是不是楼层标题
    cat_chenci = models.IntegerField()
    # 标题分类
    cat_tit = models.CharField(max_length=50, default="")
    # 分类id
    cat_id = models.CharField(max_length=20)
    cat_deleted = models.BooleanField()
    cat_icon = models.CharField(max_length=200, default="")
    cat_level = models.IntegerField()
    cat_name = models.CharField(max_length=50)
    cat_pid = models.IntegerField()


# 用户
class user(models.Model):
    userid = models.CharField(max_length=100)

    def __str__(self):
        return self.userid


# 订单
class order(models.Model):
    goods_id = models.CharField(max_length=20)
    num = models.IntegerField()
    ordertime = models.DateTimeField(auto_now_add=True)
    # userid = models.CharField(max_length=100)
    user = models.ForeignKey('user', on_delete=models.CASCADE,default=None)
    #订单状态
    '''
    0:未支付
    1：已支付
    2：申请退款中
    3：已退款
    '''
    state=models.IntegerField()

# 收藏
class collect(models.Model):
    goods_id = models.CharField(max_length=20)
    collecttime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('user', on_delete=models.CASCADE,default=None)
    # userid = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.goods_id


# 地址
class address(models.Model):
    username = models.CharField(max_length=20)
    telNumber = models.CharField(max_length=13)
    provinceName = models.CharField(max_length=20)
    cityName = models.CharField(max_length=20)
    countyName = models.CharField(max_length=20)
    detailInfo = models.CharField(max_length=50)
    firstName = models.CharField(max_length=10)
    isChecked = models.BooleanField(default=False)
    # userid = models.CharField(max_length=100)
    user = models.ForeignKey('user', on_delete=models.CASCADE,default=None)

#购物车
class cart(models.Model):
    user = models.ForeignKey('user', on_delete=models.CASCADE,default=None)
    goods_id = models.CharField(max_length=20)
    number=models.IntegerField()
    is_check=models.BooleanField(default=False)

#商家管理网址账号
class business(models.Model):
    name=models.CharField(max_length=100)
    password=models.CharField(max_length=30)