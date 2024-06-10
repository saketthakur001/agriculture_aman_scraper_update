from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(StateMaster)
class StateMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'state']
    
@admin.register(CityMaster)
class CityMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_state', 'city']
    
@admin.register(CropTypeMaster)
class CropTypeMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_season', 'type']

@admin.register(CropMaster)
class CropMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_crop_type', 'crop_name', 'crop_image']
    
@admin.register(User_Details)
class User_DetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_crops', 'created_date']

@admin.register(SeasonMaster)
class SeasonMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'season']

@admin.register(DiseaseMaster)
class DiseaseMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Disease_Images_Master)
class Disease_Images_MasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_disease', 'disease_file']

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_user', 'fk_crop', 'created_dt', 'description']

@admin.register(PostComments)
class PostCommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_user', 'fk_post', 'created_dt', 'text']


@admin.register(Service_Provider)
class Service_ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'service_provider_pic', 'created_dt']

@admin.register(Uploaded_Disease)
class Uploaded_DiseaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'fk_Service_Provider', 'fk_crop', 'filter_type', 'uploaded_image', 'created_dt']


@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'url', 'language', 'created_at']

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(NewsPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'section', 'language', 'created_at')
    search_fields = ('title', 'content')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
