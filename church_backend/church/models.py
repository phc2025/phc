from django.db import models

class user_register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default='user')
    # profile_pic = models.ImageField(upload_to='profile_pic', default='default.jpg')
    def __str__(self):
        return self.name

from django.db import models

class helping_hand(models.Model):
    user = models.ForeignKey('user_register', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    image=models.ImageField(upload_to='helping_hand')

    def __str__(self):
        return self.name

class donate(models.Model):
    user = models.ForeignKey('user_register', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.CharField(max_length=100,blank=True, null=True)
    Describe =models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='donate',blank=True,null=True)
    type = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.type

class timings(models.Model):
    day=models.CharField(max_length=100)
    startTime = models.CharField(max_length=100)
    endTime = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):

        return self.day
