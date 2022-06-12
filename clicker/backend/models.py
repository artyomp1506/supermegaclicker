from django.db import models
from django.contrib.auth.models import User

class Core(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.IntegerField(default=50)
    power = models.IntegerField(default=5)
    level = models.IntegerField(default=1)
    start_weight_for_level = models.IntegerField(default=50)
    is_weight_prev_for_next_level = models.BooleanField(default=False)
    is_levelup = models.BooleanField(default=False)
    image_number = models.IntegerField(default=1)
	
    def click(self):
        self.weight+=self.power
        if self.check_price_for_next_level((self.weight+self.power)):
            self.is_weight_prev_for_next_level = True
        else:
             self.is_weight_prev_for_next_level = False
        if self.check_price_for_next_level(self.weight):
            self.level += 1
            if self.level <= 10:
                self.image_number=self.level
            self.start_weight_for_level = self.weight
            self.is_levelup = True
        else:
            self.is_levelup=False
        return False
    def check_price_for_next_level(self, price):
        return price==self.start_weight_for_level+25
class Boost(models.Model): 
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE) 
    level = models.IntegerField(default=1) 
    price = models.IntegerField(default=10) 
    power = models.IntegerField(default=1)

    def levelup(self):
        if self.price > self.core.coins:
            return False

        old_boost_stats = copy(self)
        self.core.coins -= self.price
        self.core.power += self.power
        self.core.save()
        self.level += 1
        self.power += 5
        self.price += 25
        self.save()

        return old_boost_stats, self
