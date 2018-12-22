from django.contrib import admin

<<<<<<< HEAD
from .models import Merchant, Restaurant

=======
from .models import *

admin.site.register(Merchant)
admin.site.register(Restaurant)
>>>>>>> 03b5965d7cb27414b3cea60fac34ed80f4edc72f
# Register your models here.
admin.site.register(Merchant)
admin.site.register(Restaurant)
