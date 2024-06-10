from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('Get_OTP',Get_OTP,name='Get_OTP'),
    path('Login',Login,name='Login'),
    path('Get_Initial_Screen_Crops',Get_Initial_Screen_Crops,name='Get_Initial_Screen_Crops'),
    path('Get_Season_List',Get_Season_List,name='Get_Season_List'),
    path('Get_Crops_Types_According_Season',Get_Crops_Types_According_Season,name='Get_Crops_Types_According_Season'),
    path('Get_Crop_According_Crop_Types',Get_Crop_According_Crop_Types,name='Get_Crop_According_Crop_Types'),
    path('Updte_Profile',Updte_Profile,name='Updte_Profile'),
    path('Detect_Disease',Detect_Disease,name='Detect_Disease'),
    path('Add_Community_Post',Add_Community_Post,name='Add_Community_Post'),
    path('Comment_On_Post',Comment_On_Post,name='Comment_On_Post'),
    path('Reply_ON_Post_Comment',Reply_ON_Post_Comment,name='Reply_ON_Post_Comment'),
    path('Like_Post_By_User',Like_Post_By_User,name='Like_Post_By_User'),
    path('Service_Provider_List',Service_Provider_List,name='Service_Provider_List'),
    path('Get_Users_Crops',Get_Users_Crops,name='Get_Users_Crops'),
    path('Get_Community_Posts_List',Get_Community_Posts_List,name='Get_Community_Posts_List')
]
# urlpatterns = [*web_urls, *ajax_urls] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
