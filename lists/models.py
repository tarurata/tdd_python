from django.db import models
from django.urls import reverse


# Create your models here.
class List(models.Model):
    text = models.TextField('', default='')
    
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    # text = models.TextField('', default='', unique=True)
    text = models.TextField('', default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True, default=None)
    
    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ('id', )
        unique_together = ('list', 'text')