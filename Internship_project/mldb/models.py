from django.db import models
from django.utils import timezone

# Create your models here.
class db(models.Model):
    #django enum methodology
    class PathTypes(models.TextChoices):
       TRAINING = 'train', 'train'
       TESTING = 'test', 'test'

    class DataType(models.TextChoices):
        NORMAL = 'normal', 'normal'
        TESTING = 'error', 'error'

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#field-choices-enum-types
    data_split = models.CharField(max_length = 5, choices= PathTypes.choices)
    data_type = models.CharField(max_length = 6, choices= DataType.choices)
    data_folder = models.CharField(max_length= 255)
    date_time = models.DateTimeField(default=timezone.datetime.now)
    removed = models.BigIntegerField(default=0)
    file_name = models.FileField(upload_to='tomato_sauce')
    
    # this will ensure django knows this database is in association
    # with an already existing one with managed = False and the name
    # of the existing data base is as declared in db_table

    class Meta:
        managed = False
        db_table = 'pipe_image_data'
        #go to settings.py to configure databse settings