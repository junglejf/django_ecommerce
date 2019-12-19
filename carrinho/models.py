from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed



User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
      def get_or_create():
            return obj, True

      def new_or_get(self, request):
            cart_id = request.session.get("cart_id",None)
            qs = self.get_queryset().filter(id=cart_id)
            if qs.count() == 1:
                  new_obj = False
                  cart_obj = qs.first()
                  if request.user.is_authenticated and cart_obj.user is None:
                        cart_obj_user = request.user
                        cart_obj.save()
            else:
                  cart_obj = Cart.objects.new(user=request.user)
                  new_obj = True
                  print("linha27")
                  print(dir(request.session))
                  request.session['cart_id'] = cart_obj.id
                  print("linha30")
                  print(dir(request.session))
            return cart_obj, new_obj

      def new(self, user=None):
            print("authenticathed = "+str(user.is_authenticated)+"   -    "+str(user))
            user_obj = None
            if user is not None:
                  if user.is_authenticated:
                        user_obj = user
            return self.model.objects.create(user=user_obj)


# Create your models here.
class Cart(models.Model):
      user  = models.ForeignKey(User, null=True, blank=True,on_delete=models.DO_NOTHING)
      products = models.ManyToManyField(Product, blank=True)
      total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
      subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
      updated = models.DateTimeField(auto_now=True)
      timestamp = models.DateTimeField(auto_now_add=True)
      

      objects = CartManager()

      def __str__(self):
            return str(self.id)

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
      
      if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
            #print("INSTANCE = "+str(dir(instance.products)))
            products = instance.products.all()
            #print("procuts m2m = "+str(products))
            total = 0
            for x in products:
                  x.quantidade = x.price * x.selected
                  total += x.price * x.selected
                  x.save()
                  """
                  if 'selected' in dir(x):
                        print("x.selected = "+str(x.selected))
                  else:
                        print("adicionando quantidade inicial selected =1")
                        x.selected = 1
                        print(x.selected)
                        x.save()
                  print("x = "+str(dir(x)))
            print("\nm2m_action =" +str(action))
            """
            if instance.subtotal != total:
                  instance.subtotal = total
                  instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)




def pre_save_cart_receiver(sender, instance, *args, **kwargs):
      if instance.subtotal > 0:
            instance.total = float(instance.subtotal) * 0.5
      else:
            instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender=Cart)