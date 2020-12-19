from django.db import models


class Table1(models.Model):
    userid = models.CharField(max_length=100)
    uploaded_time = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100)
    price = models.IntegerField()
    year = models.IntegerField()
    county_name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)

    def __str__(self):
        return self.userid
