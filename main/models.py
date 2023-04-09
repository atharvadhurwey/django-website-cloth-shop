from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=(
        ('Male', 'Male'), ('Female', 'Female'), ('Kid', 'Kid')), default='Male')
    image = models.ImageField(upload_to="images/cat_imgs/")

    class Meta:
        verbose_name_plural = '1. Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="70" />' % (self.image.url))

    def __str__(self):
        return "%s %s" % (self.gender, self.title)


class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/brand_imgs/")

    class Meta:
        verbose_name_plural = '2. Brands'

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '3. Sizes'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    details = models.TextField()
    specs = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '4. Products'

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="images/product_imgs/", null=True)

    class Meta:
        verbose_name_plural = '5. ProductAttributes'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="70" />' % (self.image.url))

    def __str__(self):
        return self.product.title

# Order
status_choice=(
        ('process','In Process'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
    )


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amt = models.FloatField()
    paid_status = models.BooleanField(default=False)
    order_dt = models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(choices=status_choice,default='process',max_length=150)

    class Meta:
        verbose_name_plural = '6. Orders'

# OrderItems


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    class Meta:
        verbose_name_plural = '7. Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))


# Product Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='8. Reviews'

    def get_review_rating(self):
        return self.review_rating


# WishList
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='9.Wishlist'


# AddressBook
class UserAddressBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.PositiveIntegerField(null=True)
    address=models.TextField()
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='AddressBook'