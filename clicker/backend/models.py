from django.db import models
from django.contrib.auth.models import User

class Core(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.IntegerField(default=50)
    power = models.IntegerField(default=5)
    level = models.IntegerField(default=1)
    start_weight_for_level = models.IntegerField(default=50)
    is_weight_prev_for_next_level = models.BooleanField(default=False)
	
    def click(self):
        self.weight+=self.power
        if self.check_price_for_next_level((self.weight+self.power)):
            self.is_weight_prev_for_next_level = True
        else:
             self.is_weight_prev_for_next_level = False
        if self.check_price_for_next_level(self.weight):
            self.level += 1
            self.start_weight_for_level = self.weight
            return self.level
        return False
    def check_price_for_next_level(self, price):
        return price==self.start_weight_for_level+25
