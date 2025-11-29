#adjust this and the django_db.py file for this

from django.http import HttpRequest
import glob

class DataProcessManageView():
    #databse is db
    #folder_path = "C:\\rileyWork\Swinburne\\archive\image_data\\test\error"
    def get(self, folder_path, pathType, dataType, db):
        #read in all files to a temporary list
        temp = glob.glob(f"{folder_path}/*.png")
        for i in temp:
            #for each in list ad to databse where pathType and datatype = arg
            data = db(dir_path = i, path_type= pathType, data_type = dataType)
            data.save()


# test =[]
# #print(glob.glob(f"{testFolder}/*.png"))
# testFolder = "C:\\rileyWork\Swinburne\\archive\image_data\\test\error"
# test.append(glob.glob(f"{testFolder}/*.png"))
# for each in test:
#     print(each)


