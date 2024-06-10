
# Create your views here.
import  json
import traceback
from django.http import JsonResponse
from .models import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import random
# user registraion , user can be of two types FPO,Farmer
from django.http import HttpResponse
import pandas as pd
import xlrd
import pandas as pd
import requests
import os
from urllib.parse import urlparse

base_url = "64.227.136.113:8000"

def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if request fails
        os.makedirs('media/crops', exist_ok=True)
        
        file_path = os.path.join('media/crops', filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        return f"crops/{filename}"  # Return the file path where the image is saved
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
        return None

def Add_Crop():
    # image_url = "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcQRt_0WRr8Mc016RGaTK8eaiv6dSHKuNjIwdUrnF_7Xa_GdQL9YX9f4le5qucuyVUpKxbo7gqIGC0pZo14"
    # output_filename = "downloaded_image.jpg"
    file_path = 'static/data.xlsx'
    data = pd.read_excel(file_path)
    for index, row in data.iterrows():
        output_filename = row['Crops']
        image_url = row['Image_URL']
        output = download_image(image_url, f"{output_filename}.jpg")
    # print(output,'pppppppppppppppp')

        typeofcrop= row['Type_of_Crop']
        season = ['Season']
        if str(typeofcrop) == 'nan': 
            pass
        else:
            print(typeofcrop)
            # obj = CropTypeMaster.objects.get(crop_type=typeofcrop,fk_season__season=season)
            # print(obj.id)
            CropMaster.objects.create(crop_name=output_filename,crop_image=output)
# Add_Crop()


def Disease_Images(Disease,url,filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if request fails
        os.makedirs('media/disease', exist_ok=True)
        
        file_path = os.path.join('media/disease', filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        obj =  DiseaseMaster.objects.get(name=Disease)
        Disease_Images_Master.objects.create(fk_disease_id=obj.id,disease_file=f"disease/{filename}")
        return f"disease/{filename}"  # Return the file path where the image is saved
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
        return None

def read_diseas_imgages_Xl():
    file_path = 'static/disease_images.xlsx'
    data = pd.read_excel(file_path,sheet_name='Sheet2')
    for index, row in data.iterrows():
        filename = row['Disease']
        iamge_url = row['Image_URL']
        Disease = row['Disease']

        Disease_Images(Disease,iamge_url,f"{filename}.jpg")

# read_diseas_imgages_Xl()

def Add_Disease():
    file_path = 'static/disease_images.xlsx'
    data = pd.read_excel(file_path,sheet_name='Sheet1')
    for index, row in data.iterrows():
        Name = row['Name']
        Symtomps = row['Symtomps']
        Treatment = row['Treatments before Sowing']
        Reasons = row['Reasons']

        print(Name)
        DiseaseMaster.objects.create(name=Name,symptom=Symtomps,reason=Reasons,treatment=Treatment)

# Add_Disease()

@csrf_exempt
def Get_OTP(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            mobile_no = data['mobile_no']
            otp =random.randint(10000, 99999)
            send_data = {'status':1,'msg':"OTP for login",'otp':otp}
        else:
            send_data = {'status':0,'msg':"Request is not post"}
    except:
        send_data = {'status':0,'msg':"Something went wrong",'error':traceback.format_exc()}
    return JsonResponse(send_data)

@csrf_exempt
def Login(request):
    # User type will be  , Farmer FPO
    # Login or registratrions both functionality included here
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            user_type = data['user_type']
            language  = data['language']
            mobile_no = data['mobile_no']
            if user_type == 'Farmer':
                if User_Details.objects.filter(mobile_no=mobile_no).exists():
                    obj = User_Details.objects.get(mobile_no=mobile_no)
                    send_data = {'status':1,'msg':"User exists",'obj':obj.id}
                else:
                    obj = User_Details.objects.create(mobile_no=mobile_no,language=language,type=user_type,created_date = datetime.today().date())
                    send_data = {'status':1,'msg':"User created, use this otp for login",'user_id':obj.id}

            elif user_type == 'FPO':
                # for fpo code...............
                print('FPO.........')
        else:
            send_data = {'status':0,'msg':"Request is not post"}
    except:
        send_data = {'status':0,'msg':"Something went wrong",'error':traceback.format_exc()}
    return JsonResponse(send_data)

# this is for first scrreen
@csrf_exempt
def Get_Initial_Screen_Crops(request):
    try:
        dummy_list = []
        dumm_dict = {}

        crop_types_obj = CropTypeMaster.objects.all()
        for i in crop_types_obj:
            obj = CropMaster.objects.filter(fk_crop_type_id=i.id)
            dumm_dict[i.type] = list(obj.values())
            for crop in dumm_dict[i.type]:
                crop['crop_image'] = f"{base_url}/media/{crop['crop_image']}"
            dummy_list.append(dumm_dict)
            dumm_dict = {}
        send_data = {'status':1,'msg':"Get initials crops data",'data':dummy_list}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':"Something went wrong",'error':traceback.format_exc()}
    return JsonResponse(send_data)

@csrf_exempt
def Get_Season_List(request):
    try:
        obj = SeasonMaster.objects.all()
        send_data = {'status':1,'msg':"season list" ,'season_list':list(obj.values())}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':"Something went wrong",'error':traceback.format_exc()}
    return JsonResponse(send_data)

# this is for filter popup
@csrf_exempt
def Get_Crops_Types_According_Season(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            fk_season_id = data['fk_season_id']
            obj = CropTypeMaster.objects.filter(fk_season_id=fk_season_id) 
            send_data = {'status':1,'msg':"Crops Types list",'crops_type':list(obj.values())}
        else:
            send_data = {'status':0,'msg':"Request is not post"}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':"Something went wrong",'error':traceback.format_exc()}
    return JsonResponse(send_data)

# this api will be used to show crops on scrren after filter crops
@csrf_exempt
def Get_Crop_According_Crop_Types(request):
    try:
        if request.method == 'POST':
            dummy_list = []
            dumm_dict = {}
            data = json.loads(request.body.decode('utf-8'))
            crop_type_id_arr = data['crop_type_id_arr']

            crop_types_obj=CropTypeMaster.objects.filter(id__in = crop_type_id_arr)
            for i in crop_types_obj:
                obj = CropMaster.objects.filter(fk_crop_type_id=i.id)
                dumm_dict[i.type] = list(obj.values())
                for crop in dumm_dict[i.type]:
                    crop['crop_image'] = f"{base_url}/media/{crop['crop_image']}"
                dummy_list.append(dumm_dict)
                dumm_dict = {}
            send_data = {'status':1,'msg':"Filter data",'data':dummy_list}
        else:
            send_data = {'status':0,'msg':"Request is not post"}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':"Something went wrong",'error':traceback.format_exc()}
    return JsonResponse(send_data)


@csrf_exempt
def Updte_Profile(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            id = data['id']
            crop_id_arr = data['crop_id_arr']
            address_line_1 = data['address_line_1']
            pincode = data['pincode']
            state = data['state']
            district = data['district']
            sub_district = data['sub_district']
            vilage = data['vilage']
            # get latlong here 
            # lat1 = data['lat1']
            # lat2 = data['lat2']
            # lat3 = data['lat3']
            # lat4 = data['lat4']
            User_Details.objects.filter(id=id).update(fk_crops=crop_id_arr,address=address_line_1,pincode=pincode,state=state,district=district,sub_district=sub_district,vilage=vilage)
            send_data = {'status':1,'msg':"Profile updated successfully"}
        else:
            send_data = {'status':1,'msg':"Request is not post"}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':"Something went wrong",'error':traceback.format_exc()}
    return JsonResponse(send_data)

@csrf_exempt
def Service_Provider_List(request):
    try:
        obj = Service_Provider.objects.all()
        send_data = {'status':1,'msg':"Service provider list",'data':list(obj.values())}
    except: 
        traceback.print_exc()
        send_data = {'status':0,'msg':"Something went wrong",'error':traceback.format_exc()}
    return JsonResponse(send_data)

import ast
@csrf_exempt
def Get_Users_Crops(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            user_id = data['user_id']
            obj = User_Details.objects.get(id=user_id)
            result = ast.literal_eval(obj.fk_crops)
            crop_obj = CropMaster.objects.filter(id__in = result)
            send_data = {'status':1,'msg':"Get crops list",'data':list(crop_obj.values())}
        else:
            send_data = {'status':0,'msg':"Request is not post"}
    except: 
        traceback.print_exc()
        send_data = {'status':0,'msg':"Something went wrong",'error':traceback.format_exc()}
    return JsonResponse(send_data)


######### AI functions start start ###################
from transformers import pipeline
from PIL import Image
def process_image(image, model_name):
    pipe = pipeline("image-classification", model=model_name, device='cpu')
    predictions = pipe(image)
    max_prediction = max(predictions, key=lambda x: x['score'])
    disease_name = max_prediction['label']
    return disease_name, predictions

@csrf_exempt
def Detect_Disease(request):
    try:
        if request.method == 'POST':
            service_provider_id = request.POST.get('service_provider_id')
            crop_id = request.POST.get('crop_id')
            crop_name = request.POST.get('crop_name')
            filter_type = request.POST.get('filter_type')  # leaves, potato, furnished product
            image = request.FILES.get('image')
            if image:
                pil_image = Image.open(image)

                # code start for potato
                if crop_name.lower()=="potato":
                    if filter_type.lower() == 'crop':
                        model_name= "Amanaccessassist/finetuned-potato-food"
                    elif filter_type.lower() == 'leaves':
                        model_name="Amanaccessassist/finetuned-potato-leafdisease"

                    elif filter_type.lower() == 'chips defect':
                        model_name="Amanaccessassist/finetuned-potato-chips"
                    else:
                        send_data = {'status':0, 'msg': "Invalid filter type for Potato"}
                # code end for potato


                # ############code start for mango
                elif crop_name.lower()=="mango":
                    if filter_type.lower() == 'mango':
                        model_name="Amanaccessassist/finetuned-mango-food"
                    else:
                        send_data = {'error': "Invalid filter type for Mango"}
                else:
                    send_data = {'status':0,'msg': "Invalid Crop type"}
                disease_name, disease_images = process_image(pil_image, model_name)
                # ############code end for mango
                obj = DiseaseMaster.objects.get(name=disease_name)
                disease_images = Disease_Images_Master.objects.filter(fk_disease_id=obj.id)

                # Update coins
                # fk_userid = request.POST.get('fk_userid')
                # coins = User_Details.objects.get(id=fk_userid)
                # coins.add_coins(10)
                # coins.save()

                Uploaded_Disease.objects.create(created_dt=datetime.now(),fk_Service_Provider_id=service_provider_id,fk_crop_id =crop_id,filter_type=filter_type,uploaded_image=image)
                send_data = {'status':1,'msg':'disease information','disease': disease_name,'symptom': obj.symptom,'reason': obj.reason,'treatment': obj.treatment,'images': list(disease_images.values()),'base_path': '/media/disease','message': "Disease detected successfully"}            
            else:
                send_data ={'status':0,'msg': "No image provided"}
        else:
            send_data ={'status':0,'msg': "Request method must be POST"}

    except:
        traceback.print_exc()
        send_data = {'status':0,'msg': 'Something went wrong'}
    return JsonResponse(send_data)

def chips_defect(image):
    pipe = pipeline("image-classification", model="Amanaccessassist/finetuned-potato-chips",device='cuda:0')
    predictions=pipe(image)
    max_prediction = max(predictions, key=lambda x: x['score'])
    chips = max_prediction['label']
    return chips

def potatoleaf_disease(image):
    pipe = pipeline("image-classification", model="Amanaccessassist/finetuned-potato-leafdisease",device='cuda:0')
    predictions=pipe(image)
    max_prediction = max(predictions, key=lambda x: x['score'])
    chips = max_prediction['label']
    return chips


def mango_disease(image):
    pipe = pipeline("image-classification", model="Amanaccessassist/finetuned-mango-food",device='cuda:0')
    predictions=pipe(image)
    max_prediction = max(predictions, key=lambda x: x['score'])
    chips = max_prediction['label']
    return chips

def mango_types(image):
    pipe = pipeline("image-classification", model="Amanaccessassist/finetuned-mango-types",device='cuda:0')
    predictions=pipe(image)
    max_prediction = max(predictions, key=lambda x: x['score'])
    chips = max_prediction['label']
    return chips
######### AI functions start end ###################

@csrf_exempt
def Get_Community_Posts_List(request):
    try:
        if request.method == 'POST':
            final_list = []
            obj = CommunityPost.objects.all()

            for post in obj:
                final_dict = {
                    'id': post.id if post.id else '',
                    'description': post.description if post.description else '',
                    'created_dt': post.created_dt if post.created_dt else '',
                    'comment_list': []
                }

                comment_list = []
                comment_objects = PostComments.objects.filter(fk_post_id=post.id)

                for comment in comment_objects:
                    comment_dict = {
                        'post_comment': comment.text if comment.text else '',
                        'reply_comments': []
                    }

                    reply_list = []
                    reply_objects = CommentReply.objects.filter(fk_postcoment_id=comment.id)

                    for reply in reply_objects:
                        reply_dict = {
                            'id': reply.id if reply.id else '',
                            'text': reply.text if reply.text else ''
                        }
                        reply_list.append(reply_dict)

                    comment_dict['reply_comments'] = reply_list
                    comment_list.append(comment_dict)

                final_dict['comment_list'] = comment_list
                final_list.append(final_dict)

            send_data = {'status': 1, 'msg': "Community post list", 'data': final_list}
        else:
            send_data = {'status': 0, 'msg': "Request is not post"}
    except Exception as e:
        traceback.print_exc()
        send_data = {'status': 0, 'msg': "Something went wrong", 'error': str(e)}
    return JsonResponse(send_data)


@csrf_exempt
def Add_Community_Post(request):
    try:
        if request.method=="POST":
            fk_user_id = request.POST.get('fk_user_id')
            fk_crop_id = request.POST.get('fk_crop_id')
            description =request.POST.get('description')
            video_file =request.FILES.get('video_file')
            image_file =request.FILES.get('image_file')
            obj=CommunityPost.objects.create(fk_user_id=fk_user_id,fk_crop_id=fk_crop_id,description=description,created_dt=datetime.now())
            if video_file:
                PostsMedia.objects.create(fk_post_id=obj.id,video_file=video_file,image_file=image_file)
            send_data = {'status':1,'msg':'Post Created Successfully'}
        else:
            send_data = {'status':0,'msg':'Request is not post'}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':'Something went wrong'}
    return JsonResponse(send_data)

@csrf_exempt
def Comment_On_Post(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            fk_user_id = data['fk_user_id']
            fk_post_id = data['fk_post_id']
            comemnt_text = data['comemnt_text']
            PostComments.objects.create(fk_user_id=fk_user_id,fk_post_id=fk_post_id,text=comemnt_text,created_dt=datetime.now())
            send_data = {'status':1,'msg':'comment on post successfully'}
        else:
            send_data = {'status':0,'msg':'request is not post'}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':'Something went wrong'}
    return JsonResponse(send_data)


@csrf_exempt
def Reply_ON_Post_Comment(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            fk_postcoment_id = data['fk_postcoment_id']
            fk_user_id = data['fk_user_id']
            text = data['text']
            CommentReply.objects.create(fk_postcoment_id=fk_postcoment_id,fk_user_id=fk_user_id,text=text,created_dt = datetime.now())
            send_data = {'status':1,'msg':'Reply on comment successfully'}
        else:
            send_data = {'status':0,'msg':'request is not post'}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':'Something went wrong'}
    return JsonResponse(send_data)

@csrf_exempt
def Like_Post_By_User(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            fk_post_id = data['fk_post_id']
            fk_user_id = data['fk_user_id']
            if PostsLike.objects.filter(fk_post_id=fk_post_id,fk_user_id=fk_user_id).exists():
                obj = PostsLike.objects.get(fk_post_id=fk_post_id,fk_user_id=fk_user_id)
                obj.like_count + 1
                obj.save()
            else:
                PostsLike.objects.create(fk_post_id=fk_post_id,fk_user_id=fk_user_id,like_count=1)
            send_data = {'status':1,'msg':'Reply on comment successfully'}
        else:
            send_data = {'status':0,'msg':'request is not post'}
    except:
        traceback.print_exc()
        send_data = {'status':0,'msg':'Something went wrong'}
    return JsonResponse(send_data)

'''@csrf_exempt
def like_post(request, post_id):
    if request.method == 'POST':
        post = PostDetails.objects.get(pk=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            message = 'Post unliked successfully'
        else:
            post.likes.add(request.user)
            message = 'Post liked successfully'
        return JsonResponse({'status': 'success', 'message': message})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

def post_detail(request, post_id):
    try:
        post = PostDetails.objects.get(pk=post_id)
        data = {
            'description': post.description,
            'post_date': post.post_date,
            'crop_type': post.crop_type,
            'likes_count': post.likes.count(),
            'likes_by': [like.user.username for like in post.likes.all()],
            'replies': [{'username': reply.user.username, 'text': reply.text, 'created_at': reply.created_at} for reply in post.replies.all()],
            'comments': [{'username': comment.user.username, 'text': comment.text, 'created_at': comment.created_at} for comment in post.comments.all()]
        }
        return JsonResponse(data)
    except PostDetails.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'})'''
