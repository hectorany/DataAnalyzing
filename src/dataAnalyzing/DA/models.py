from django.db import models
from django.utils import timezone
# Create your models here.

class CustDataSchem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default = timezone.now )
    db_created = models.IntegerField()
    schem = models.TextField(blank = True, null = True)
    
    def __str__(self):
        return self.name
    
class DataBase(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    shown = models.BooleanField(default = True)
    pub_date = models.DateTimeField(default = timezone.now )
    data_schema = models.ForeignKey(CustDataSchem,on_delete=models.CASCADE)
    items = models.IntegerField( default = 0)
    
        
    