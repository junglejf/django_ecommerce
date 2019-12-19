from django.db import models
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse
# Create your models here.



class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    #def featured(self):
        #return self.get_queryset().filter(featured = True)
        #return self.get_queryset().featured()

    def get_by_id(self,id):
        qs = self.get_queryse().filter(id = id)
        if qs.count()==1:
            return qs.first()
        return None

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    objects = CategoryManager()
    
    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug = self.slug)
        return reverse("products:list_products_product", kwargs={"slug":self.slug})
    
    #exibir o nome do produto
    def __str__(self):
        return self.name



class CategoryQuerySet(models.query.QuerySet):
    pass
    #def active(self):
     #   return self.filter(active=True)

    #def featured(self):
     #   return self.filter(featured=True, active=True)

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(category_pre_save_receiver, sender = Category)

### MODELO PRODUTO ##########
#MANAGER
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active().order_by('title')

    def featured(self):
        #return self.get_queryset().filter(featured = True)
        return self.get_queryset().featured().order_by('title')

    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()
        return None

#PRODUTO
class Product(models.Model): #product_category
    title       = models.CharField(max_length=120)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=20, default=100.00)
    image       = models.ImageField(upload_to = 'products/', null = True, blank = True)
    featured    = models.BooleanField(default = False)
    active      = models.BooleanField(default = True)
    slug        = models.SlugField(blank = True, unique = True)
    category    = models.ForeignKey(Category, related_name = 'products',on_delete=models.DO_NOTHING)
    reg_date    = models.DateField(null=True)
    quantidade = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    selected = models.IntegerField(default=1)
    

    objects = ProductManager() 

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug = self.slug)
        return reverse("products:detail", kwargs={"slug":self.slug})
    
    #exibir o nome do produto
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title
    

#COMUNICAÇÂO COM O BANCO
class ProductQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(active=True).order_by('title')

    def featured(self):
        return self.filter(featured=True, active=True).order_by('title')

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender = Product)

