import glob
import os
import zipfile
import base64
from io import BytesIO
import numpy as np
import tensorflow as tf
import pandas as pd
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from mldb.models import db
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model

def view(request):
   pipe_image_data = db.objects.filter(removed = 0)
   context = {"pipe_image_data":pipe_image_data,
              "pageName": 'View Database'
              } 
   return render(request, "view.html", context)

# rendering the uploads webpage
def upload(request):
   return render(request, 'upload.html',{'pageName': 'Upload to Database'})

def cnn_model(request):
   
   pipe_image_data = db.objects.values('data_folder').distinct()

   context = {"pipe_image_data": pipe_image_data,
              "pageName": 'Submit Dataset and Train Model'
              }
   return render(request, 'cnn_model.html', context)

def cnn_model_function(request):
    data_folder = request.POST.get('data_folder','')
    # for testing purposes until CNN is implamented
    return redirect("cnn_model_results", data_folder)

def cnn_model_results(request, data_folder):
   #data_folder = request.POST.get('data_folder')
    x_train, x_val, y_train, y_val, X_Test, Y_Test = imageClasifiction.prepare(data_folder)
    model = imageClasifiction.build_model()
    history = imageClasifiction.run_model(model, x_train, x_val, y_train, y_val)
    eval =  imageClasifiction.view_results(model, x_train, x_val, y_train, y_val, X_Test, Y_Test)
    acc = convert_to_html(imageClasifiction.build_acuracy_vis(history))
    loss = convert_to_html(imageClasifiction.build_loss_vis(history))
    con = convert_to_html(imageClasifiction.build_confusion_matrix(model, X_Test, Y_Test))
    model_path = imageClasifiction.save_model_function(model)
    context = {
        'data_folder': data_folder,
        'eval': eval,
        'acc' : acc,
        'loss': loss,
        'con' : con,
        'model': model_path,
        'pageName': 'Model Results'
    }
    return render(request, "cnn_model_results.html",context)

def cnn_saved_model(request):
    target_dir = os.path.join(settings.MEDIA_ROOT, 'saved_cnn_models')
    models= os.listdir(target_dir)
    #for m in target_dir:
    #    models.append(m)
    print(models)
    context ={'models': models,
              'pageName': 'View Saved Models'}
    return render(request, "cnn_saved_model.html", context)

def cnn_inference(request):
    m = request.POST.get('models', '')
    target_dir = os.path.join(settings.MEDIA_ROOT, 'saved_cnn_models')
    models = os.path.join(target_dir, m)
    #keras load_model function
    loaded = models
    #print(loaded.summary())
    context = {
        'models': models,
        'loaded': loaded,
        "pageName": 'Inference With Model'
               }
    return render(request, "cnn_inference.html",context)

#this may or may not work
def make_inference(request):
    
    #loading model and image
    model_path = request.POST.get('loaded', '')
    loaded = load_model(model_path)
    #this works
    #print(loaded.summary())

    img = request.FILES.get('img')
    #prepared_image = imageClasifiction.img_preprocess(img)
    prepared_image = prepare_single_image(img)
    # faile to convert numpy array to tensor
    
    print("Shape of prepared_image:", prepared_image.shape)
    print("Type of prepared_image:", type(prepared_image))
    #inference
    prediction = loaded.predict(prepared_image)
    pred = prediction[0][0]
    if pred >= 0.5:
        result = "Normal"
    else:
        result= "Error"
    #printing result of prediction. [[1.]] or [[0.]]
    print(result)
    #return the results
    context ={'result': result,
              'loaded' : model_path,
              }
    return render(request, "cnn_inference.html", context)

def prepare_single_image(upload):
    img = upload.read()
    img = tf.image.decode_png(img,channels=3)
    img = tf.image.rgb_to_grayscale(img)
    img = tf.image.resize(img, [255,255])
    img = np.expand_dims(img, axis=0)
    return img
    

@staticmethod
def convert_to_html(vis):
    bio = BytesIO(vis)
    plt.savefig(bio, format ='png')
    bio.seek(0)
    return base64.b64encode(bio.getvalue()).decode('utf-8')

#rendering zip_upload page
def upload_zip(request):
   return render(request, 'upload_zip.html',{'pageName': 'Upload ZIP'})

def upload_zip_function(request):
    file_name = request.FILES.get('file_name')
    target_dir = os.path.join(settings.MEDIA_ROOT, 'tomato_sauce')
    zipper = ZipFolder(file_name)
    zipper.query_and_extract(target_dir)
    return redirect( "/")

def remove(request):
   
   pipe_image_data = db.objects.all()
   context = {"pipe_image_data":pipe_image_data,
              "pageName": 'Remove From Database'
              } 
   return render(request, "remove.html", context)

def upload_new(request):
   data_split = request.POST.get('data_split', '')
   data_type = request.POST.get('data_type', '')
   file_name = request.FILES.get('file_name','') # .FILES will allow the file to be saved as part of the models.py 
   data_folder = request.POST.get('data_folder', '')
   
   db.objects.create(
      data_type = data_type,
      data_split = data_split,
      file_name = file_name,
      data_folder = data_folder
   )
   return redirect("/")

def remove_function(request, pk):
    pipe = get_object_or_404(db, pk = pk)
    pipe.removed = 1
    pipe.save()
    return redirect("/remove")

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
        print(valuesList)
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

    def query_to_db(self, folder):
        for data in self.zip_split():
            data_type = data[0]
            data_split = data[1]
            file_name = data[2]
            data_folder = folder
            #add into db
            db.objects.create( data_type = data_type, data_split = data_split, file_name = file_name, data_folder = data_folder)
    
    def query_and_extract(self, target_dir):
        folder = self.extract_zip(target_dir)
        self.query_to_db(folder)

#image classification from document
class imageClasifiction:
    def __init__(self, path):
        self.train_df = self.create_df(path, "\\train")
        self.test_df = self.create_df(path, "\\test")
    
    @staticmethod
    #create dataframe with iamge path and outcome (normal, error)
    def create_df(path, path2):
        full_path =(path + path2)
        files1 = glob.glob(os.path.join(full_path + "\\normal\*.png"))
        files2 = glob.glob(os.path.join(full_path + "\\error\*.png"))
        print("normal: ", len(files1))
        print("error: ", len(files2))
        df_n = pd.DataFrame()
        df_p = pd.DataFrame()
        df_n["name"] = [x for x in files2]
        df_n["outcome"] = 0.0
        df_p["name"] = [x for x in files1]
        df_p["outcome"] = 1.0
        df = pd.concat([df_n, df_p], axis=0, ignore_index = True)
        df = shuffle(df)
        return df
    
    def create_x_and_y(self):
        #for each value in paths create numpy array val
        X = np.array([self.img_preprocess(p) for p in self.train_df.name.values])
        Y = self.train_df.outcome.values
        return X, Y
    
    #use this after the model has been created for the test part of the model =
    def create_x_and_y_test(self):
        X = np.array([self.img_preprocess(p) for p in self.test_df.name.values])#for each value in paths create numpy array val
        Y = self.test_df.outcome.values
        return X, Y

    #data split
    @staticmethod
    def data_split(X,Y):
        x_train, x_val, y_train, y_val = train_test_split(X,Y, test_size = 0.2, random_state = 0)
        return x_train, x_val, y_train, y_val

    @staticmethod
    def img_preprocess(i_path):
        #change dtype
        img = tf.io.read_file(i_path)
        img = tf.image.decode_png(img,channels=3)
        img = tf.image.rgb_to_grayscale(img)
        img = tf.image.resize(img, [255,255])
        return img
    
    @staticmethod
    def prepare(data_path):
        # r is included at the start so python treats it as a raw string
        dir_path = os.path.join(os.getcwd(), data_path)  #adjust path for django
        aic = imageClasifiction(path=dir_path)
        X,Y = aic.create_x_and_y()
        x_test,y_test = aic.create_x_and_y_test()
        X=X/255
        x_test/255
        X = np.expand_dims(X, -1)
        x_test = np.expand_dims(x_test, -1)
        X = np.array(X, dtype=np.float64)
        Y =  np.array(Y, dtype=np.float64)
        x_test = np.array(x_test, dtype=np.float64)
        y_test =  np.array(y_test, dtype=np.float64)
        x_train, x_val, y_train, y_val = aic.data_split(X,Y)
        return x_train, x_val, y_train, y_val, x_test, y_test

    @staticmethod
    def build_model():
        #create model object
        model = tf.keras.Sequential()
        # 32 filters, (3,3) convolution window, padding type, anctivatino functions, input shape of data
        #Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead
        model.add(layers.Conv2D(16,(3,3), padding='same', activation='relu', input_shape=(255,255,1)))
        model.add(layers.MaxPooling2D((3,3)))
        model.add(layers.Conv2D(32,(3,3), padding='same',activation = 'relu'))
        model.add(layers.MaxPooling2D((3,3)))
        model.add(layers.Conv2D(64,(3,3),padding='same', activation = 'relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dropout(0.3))#to reduce over fitting
        model.add(layers.Dense(1, activation = 'sigmoid')) #softmax calculates probability
        model.compile(optimizer = 'adam', loss=tf.keras.losses.BinaryCrossentropy(), metrics = ['accuracy'])
        return model

    @staticmethod
    def run_model(model,x_train, x_val, y_train, y_val):
        early_stopping = EarlyStopping(monitor='val_loss', patience = 20, restore_best_weights=True)
        class_weight = {0:1., 1: 25.}
        #early_stopping added to this model                    #change to 20% of X,Y
        history = model.fit(x_train,y_train, epochs = 5,validation_data=(x_val, y_val), callbacks=[early_stopping], class_weight=class_weight)
        return history
    
    @staticmethod
    def view_results(model, x_train, x_val, y_train, y_val, X_Test, Y_Test):
        test_eval = model.evaluate(x = X_Test, y= Y_Test) #will return the loss value and metric values for the model in the test
        validation_eval = model.evaluate(x = x_val, y= y_val) #will return the loss value and metric values for the model in the test
        train_eval = model.evaluate(x = x_train, y= y_train) #will return the loss value and metric values for the model in the test
        #print(f"Test data evaluation: {test_eval}")
        #print(f"Validation data evaluation: {validation_eval}")
        #print(f"Train data evaluation: {train_eval}")
        return{
            'test_eval': test_eval,
            'validation_eval': validation_eval,
            'train_eval': train_eval
        }

    @staticmethod
    def build_confusion_matrix(model, x_test, y_test):
        predicted = model.predict(x_test) 
        conf_matrix = metrics.confusion_matrix(y_true= y_test, y_pred= predicted)       
        fig, ax = plt.subplots(figsize =(6.5,6.5))
        #matshow is the basis of a matrix more or less. 0,0 0,1, 1,0 1,1 in this case
        ax.matshow(conf_matrix, alpha = 0.2)
        label = {0: 'Normal', 1: 'Error'}
        #ax.set_xticklabels([label[i] for i in range(conf_matrix.shape[1])])
        #ax.set_yticklabels([label[i] for i in range(conf_matrix.shape[0])])

        for i in range(conf_matrix.shape[0]):
            for o in range(conf_matrix.shape[1]):
                ax.text(x=i , y = o, s=conf_matrix[i,o], size ='xx-large')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')

    @staticmethod
    def build_acuracy_vis(history):
        plt.figure()
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('Model Accuracy')
        plt.xlabel('epoch')
        plt.ylabel('Accuracy')
        plt.legend(['train', 'New validation data'], loc = 'lower right')
        #plt.show()

    @staticmethod
    def build_loss_vis(history):
        plt.figure()
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.xlabel('epoch')
        plt.ylabel('Loss')
        plt.legend(['loss', 'New validation data'], loc = 'upper right')
       # plt.show()

    @staticmethod
    def save_model_function(model):
        target_dir = os.path.join(settings.MEDIA_ROOT, 'saved_cnn_models')
        os.makedirs(target_dir, exist_ok= True) # does the dir exist
        data_folder_num = 1
        while True:
            #while a folder exists with the same name as current folder continue loop and increment data_folder_num
            file = os.path.join(target_dir, f'cnn_model_{data_folder_num}.keras')
            #if folder name does not exist break out of loop and continue to zip extraction
            if not os.path.exists(file):
                break
            data_folder_num +=1
        print(file)
        model.save(file)
        return file
