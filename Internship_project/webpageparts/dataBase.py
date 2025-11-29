from django.db import models

class Paths(models.Model):
   #django enum methodology
    class PathTypes(models.TextChoices):
       TRAINING = 'train', 'train'
       TESTING = 'test', 'test'

    class DataType(models.TextChoices):
        NORMAL = 'normal', 'normal'
        TESTING = 'error', 'error'

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#field-choices-enum-types
    path_type = models.CharField(max_length = 5, choices= PathTypes.choices)
    data_type = models.CharField(max_length = 6, choices= DataType.choices)
    dir_path = models.CharField(max_length = 255)
   
    def __str__(self):
        return self.dir_path



    #each entry in database
        # PathType enum --> training or test
        # dataType enum --> error or normal
        #filePath string--> path\to\dir\image

    #this will keep it all in the one database table
    #example error data
    # pathType: training
    # dataType: error
    #filePth: C:\rileyWork\Swinburne\archive\image_data\test\error\KEMP_IMG_DATA_Error_1.png



#    def getPath(self, path_type):
#         if path_type not in self.PathTypes:
#             raise ValueError("Invalid path type. 'train' or 'test'.")
#         if path_type == 'test':
#             #example: 'test/error, test/normal'
#             return arr.array(f"{self.dir_path}/{path_type}/{self.error_path}", f"{self.dir_path}/{path_type}/{self.normal_path}")
#         if path_type == 'train':
#             return arr.array(f"{self.dir_path}/{path_type}/{self.error_path}", f"{self.dir_path}/{path_type}/{self.normal_path}")
#         else:
#             return "Broken. Fix me"
# #        if data_type not in self.DataTypes:
# #            raise ValueError("Invalid data type. 'error' or 'normal'.")
    
    
#     def __str__(self):
#         return f"{self.path_id}: {self.path_type}"
    
#     def getTestPathError(self):
#         return f"{self.path_type}/{self.error_path}/"
    
#     def getTestPathNormal(self):
#         return f"{self.path_type}/{self.normal_path}/"
    
#     def getTrainingPathError(self):
#         return f"{self.path_type}/{self.error_path}/"
    
#     def getTrainingPathNormal(self):
#         return f"{self.path_type}/{self.normal_path}/"



    

# class ImageData(models.Model):
# #    class ImageTypes(models.TextChoices):
# #        ERROR = 'ER', ('error')
# #        NORMAL = 'NO', ('normal')
#     #django auto generates primary key for id
# #    file_type = models.CharField(max_length = 15, choices =ImageTypes.choices)
#     file_name = models.ImageField(max_length=255)  # https://www.geeksforgeeks.org/imagefield-django-models/
#     path_id = models.ForeignKey(Paths, on_delete=models.CASCADE)   #https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_one/
    
#     def __str__(self):
#         return f"{self.path_id}: {self.file_name}"
    
#     def getImagePath(self, path):
#         #get path_id via matching getErrorPath or GetNormalPath method
#         if path == 'train':
#               # return training data
#               return f"{self.path_id.getTrainPath()}/error" 
#         elif path == 'test':
#             #return test data
#             return f""
#         else:
#             return "Arg error. Please enter a vild value 'error' or 'normal'."


    

