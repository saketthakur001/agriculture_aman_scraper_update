import traceback
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from PMS_Admin_App.models import *
from PMS_App.models import *


# below code is decorator to check user login or not

def Admin_login_required_decorator(view_func):
	def _wrapped_view(request, *args, **kwargs):
		try:
			user_id = request.session.get('user_id')
			usertype = request.session.get('user_type')
			if user_id and usertype:
				if Super_Admin.objects.filter(id=user_id).exists():
					user = Super_Admin.objects.get(id=user_id)
					return view_func(request, user, *args, **kwargs) 
				else:
					return redirect('/Pms_admin/Login')
			else:
				return redirect('/pms_admin/Login')
		except Exception as e:
			traceback.print_exc()
			return redirect('/pms_admin/Login')  # Redirect or return an error page
	return _wrapped_view

### check request is authenticated or not 
def User_login_required_decorator(view_func):
	def _wrapped_view(request, *args, **kwargs):
		try:
			user_id = request.session.get('user_id')
			usertype = request.session.get('user_type')
			if user_id and usertype:
				if User_Details.objects.filter(id=user_id).exists():
					user = User_Details.objects.get(id=user_id)
					return view_func(request, user, *args, **kwargs) 
				else:
					return redirect('/')
			else:
				return redirect('/')
		except Exception as e:
			traceback.print_exc()
			return redirect('/')  # Redirect or return an error page
	return _wrapped_view

def handle_ajax_exception(func):
	'''Function template to handle POST request and handle exceptions...'''
	def wrapper(request, *args, **kwargs):
		send_data = {'status': 0, 'msg': 'Something went wrong.', 'errTitle' : 'error'}
		try:
			if request.method == 'POST':
				return func(request, *args, **kwargs)
			else:
				send_data['msg'] = 'POST method required.'
		except ObjectDoesNotExist:
			send_data['msg'] = 'Object not found.'
		except:
			traceback.print_exc()
		return JsonResponse(send_data)
	return wrapper