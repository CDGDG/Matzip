from django.db import models

from django.contrib.auth.models import User

class Restaurant(models.Model):
    
    name = models.CharField(db_column='name', max_length=11, default='정보없음')
    type = models.CharField(db_column='type', max_length=16, default='기타')
    address = models.CharField(db_column='address', max_length=100, null=True)
    phone = models.CharField(db_column='phone', max_length=12, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='user')

    class Meta:
        db_table = 'mz_matzip'

    def __str__(self):
        return self
    
