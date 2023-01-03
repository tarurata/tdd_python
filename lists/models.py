from django.db import models
from django.urls import reverse
from django.conf import settings


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    # text = models.TextField('', default='')
    
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    # text = models.TextField('', default='', unique=True)
    text = models.TextField('', default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, null=True, default=None)
    
    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')
