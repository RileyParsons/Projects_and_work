import os

# Create your views here.
# view function needs to be mapped to a URL. so when a request is sent to the URL this function is called
import zipfile

class ZipFolder:
    def __init__(self, zip_filename):
        self.zip_filename = zip_filename
    #use python function for 
    def dir_path(self):
        with zipfile.ZipFile(self.zip_filename, 'r') as myzip:
            return myzip.namelist()

    #remember that all methods within python class should have a self parameter.
    #thus you can use your own methods as arguments
    def zip_split(self):
        # create empty list for list of lists which will create the database entry data
        valuesList = []
        for each in self.dir_path():
            splt = each.split('/')
            valuesList.append(splt)
        #in clean_val the value is = to value for each in ValuesList if the length is greater than or equal to 3
        clean_val = [val for val in valuesList if len(val) >=3]
        return clean_val
    
    #target dir will be 'source' folder for database
    def extract_zip(self, target_dir):
        #create data folder index number
        data_folder_num = 1
        while True:
            #while a folder exists with the same name as current folder continue loop and increment data_folder_num
            folder = os.path.join(target_dir, f'data_{data_folder_num}')
            #if folder name does not exist break out of loop and continue to zip extraction
            if not os.path.exists(folder):
                break
            data_folder_num +=1
        #fodler path as arg1, exist = True to leave directory unaltered if it already exists
        os.makedirs(folder, exist_ok=True)
        with zipfile.ZipFile(self.zip_filename) as myzip:
            myzip.extractall(folder) # target folder will be our newly create data_x fodler
            # return folder name as part of query and extract
            return folder

    def query_to_db(self, db, folder):
        for data in self.zip_split():
            data_type = data[0]
            data_split = data[1]
            file_name = data[2]
            data_folder = folder
            #add into db
            db.objects.create( data_type = data_type, data_split = data_split, file_name = file_name, data_folder = data_folder)

    def query_and_extract(self, target_dir, db):
        folder = self.extract_zip(target_dir)
        self.query_to_db(db, folder)