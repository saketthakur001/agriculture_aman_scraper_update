from django.db import models

# Create your models here.
class StateMaster(models.Model):
    state = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True) 

class CityMaster(models.Model):
    fk_state = models.ForeignKey(StateMaster, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=100)
    created_date = models.DateField(null=True , blank=True)

class SeasonMaster(models.Model):
    season = models.CharField(null=True , blank=True,max_length=100)
    
class CropTypeMaster(models.Model):
    fk_season =models.ForeignKey(SeasonMaster,on_delete=models.CASCADE,null=True,blank=True)
    type = models.CharField(null=True, blank=True, max_length=100)

class CropMaster(models.Model):
    fk_crop_type =models.ForeignKey(CropTypeMaster,on_delete=models.CASCADE,null=True,blank=True)
    crop_name = models.CharField(null=True, blank=True, max_length=100)
    crop_image = models.FileField(upload_to="crops/", blank=True, null=True)
    # crop_image_url = models.URLField(max_length=200, null=True, blank=True)

class User_Details(models.Model):
    # fk_fpo = models.ForeignKey(FPO_User,on_delete=models.CASCADE,null=True,blank=True)#fpo will upload the csv and user will be added , or user can register by himselef
    fk_crops =  models.CharField(null=True,blank=True,max_length=100)
    created_date = models.DateField(null=True , blank=True)
    # is_profile_updated  = models.BooleanField(default=False,null=True,blank=True)
    name = models.CharField(null=True,blank=True,max_length=100)
    mobile_no = models.CharField(null=True,blank=True,max_length=10)
    TYPE = (
        ("FPO", "FPO"),
      	("Farmer", "Farmer"),
	)
    type = models.CharField(max_length= 200 , choices = TYPE,default='Farmer')

    LANGUAGE = (
        ("EN", "EN"),
      	("HI", "HI"),
      	("TE", "TE"),  
      	("TA", "TA"),  
	)
    language = models.CharField(max_length= 200 , choices = LANGUAGE,default='EN')
    # update fields 
    profile = models.FileField(upload_to="Profile/", blank=True, null=True)
    address = models.CharField(null=True,blank=True,max_length=200)
    pincode =  models.CharField(null=True,blank=True,max_length=10)
    state =  models.CharField(null=True,blank=True,max_length=100)
    district =  models.CharField(null=True,blank=True,max_length=100)
    sub_district =  models.CharField(null=True,blank=True,max_length=100)
    vilage =  models.CharField(null=True,blank=True,max_length=100)

    # land area
    lat1 =  models.CharField(null=True,blank=True,max_length=100)
    lat2 =  models.CharField(null=True,blank=True,max_length=100)
    lat3 =  models.CharField(null=True,blank=True,max_length=100)
    lat4 =  models.CharField(null=True,blank=True,max_length=100)

class DiseaseMaster(models.Model):
    name = models.CharField(null=True,blank=True,max_length=100)
    symptom = models.TextField(null=True,blank=True)
    reason = models.TextField(null=True,blank=True)
    treatment = models.TextField(null=True,blank=True)

class Disease_Images_Master(models.Model):
    fk_disease = models.ForeignKey(DiseaseMaster,on_delete=models.CASCADE,null=True,blank=True)
    disease_file = models.FileField(upload_to="disease/", blank=True, null=True)


# community purpose
class CommunityPost(models.Model):
    fk_user = models.ForeignKey(User_Details, on_delete=models.CASCADE,null=True,blank=True)
    fk_crop=models.ForeignKey(CropMaster, on_delete=models.CASCADE , null=True,blank=True)
    description=models.TextField(null=True, blank=True)
    created_dt=models.DateTimeField(auto_now_add=False)

class PostsMedia(models.Model):
    fk_post=models.ForeignKey(CommunityPost,on_delete=models.CASCADE,null=True,blank=True)
    video_file=models.FileField(upload_to='post/videos', null=True, blank=True)
    image_file = models.FileField(upload_to='post/image', null=True, blank=True)

class PostComments(models.Model):
    fk_post=models.ForeignKey(CommunityPost,on_delete=models.CASCADE,null=True,blank=True)
    fk_user=models.ForeignKey(User_Details,on_delete=models.CASCADE,null=True,blank=True)
    text=models.TextField(null=True,blank=True)
    created_dt=models.DateTimeField(auto_now_add=False , null=True,blank=True)

class CommentReply(models.Model):
    fk_postcoment = models.ForeignKey(PostComments,on_delete=models.CASCADE,null=True,blank=True)
    fk_user=models.ForeignKey(User_Details,on_delete=models.CASCADE,null=True,blank=True)
    text=models.TextField(null=True,blank=True)
    created_dt=models.DateTimeField(auto_now_add=False)

class PostsLike(models.Model):
    fk_post=models.ForeignKey(PostComments,on_delete=models.CASCADE,null=True,blank=True)    
    fk_user=models.ForeignKey(User_Details,on_delete=models.CASCADE,null=True,blank=True)
    created_dt = models.DateTimeField(auto_now_add=False)
    like_count = models.IntegerField(default=0, blank=True, null=True)


class Service_Provider(models.Model):
    name =  models.CharField(null=True,blank=True,max_length=100)
    service_provider_pic = models.FileField(upload_to="service_provider/", blank=True, null=True)
    created_dt = models.DateTimeField(auto_now_add=False)
    

class Uploaded_Disease(models.Model):
    created_dt = models.DateTimeField(auto_now_add=False)
    fk_Service_Provider=models.ForeignKey(Service_Provider,on_delete=models.CASCADE,null=True,blank=True) 
    fk_crop=models.ForeignKey(CropMaster,on_delete=models.CASCADE,null=True,blank=True)  
    uploaded_image = models.FileField(upload_to="uploaded/", blank=True, null=True)
    filter_type =  models.CharField(null=True,blank=True,max_length=100)


class Article(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Text(models.Model):
    text = models.CharField(max_length=500, null=True, blank=True)


from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    section = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=20, null=True, blank=True)

class Language(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)


class NewsPost(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    section = models.CharField(max_length=50, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

