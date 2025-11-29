from django.urls import path
from . import views

#URLConf. needs to be imported into te main project now
#what django looks for as an array of url pattern object
urlpatterns =[
    #returns a url pattern object
    #defin the path and designated view
    path('', views.view, name='view'),
    path('upload/', views.upload, name='upload'),
    path('remove/', views.remove, name='remove'),
    path('upload_new/', views.upload_new, name = 'upload_new'),
    path('upload_zip/', views.upload_zip, name = 'upload_zip'),
    path('upload_zip_function/', views.upload_zip_function, name = 'upload_zip_function'),
    path('remove_function/<int:pk>', views.remove_function, name= 'remove_function'),
    path('cnn_model/', views.cnn_model, name= 'cnn_model'),
    path('cnn_model_function/', views.cnn_model_function, name= 'cnn_model_function'),
    path('cnn_model_results/<str:data_folder>/', views.cnn_model_results, name= 'cnn_model_results'),
    path('cnn_saved_model/', views.cnn_saved_model, name = 'cnn_saved_model'),
    path('cnn_inference/', views.cnn_inference, name ='cnn_inference'),
    path('make_inference/', views.make_inference, name = 'make_inference'),
    ]
