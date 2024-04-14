from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Usermaster
from django.core.mail import send_mail

@csrf_exempt
def signup(request):
    try:
        if request.method == 'POST':
            response = {}
            json_data = json.loads(request.POST.get('data'))

            full_name = json_data.get('fullname')
            email = json_data.get('email')
            password = json_data.get('password')
            confirm_password = json_data.get('confirmpassword')
            mobilenumber=json_data.get('mobilenumber')
            gender=json_data.get('gender')
            countryCode=json_data.get('countryCode')
            # Check if the user already exists
            if Usermaster.objects.filter(email=email).exists():
                response['status'] = False
                response['message'] = 'User with this email already exists'
            elif password != confirm_password:
                response['status'] = False
                response['message'] = 'Passwords do not match'
            else:
                # Create a new user
                user_details = Usermaster.objects.create(
                    fullname=full_name,
                    password=password,
                    confirmpassword=confirm_password,
                    email=email,
                    mobilenumber=mobilenumber,
                    gender=gender,
                    countryCode=countryCode
                    
                )
                response['status'] = True
                response['message'] = 'Signup successful, please login with valid credentials'
                
                # Send confirmation email
                subject = 'Welcome to our platform'
                message = f'Hello {full_name},\n\nThank you for signing up!\n\nPlease login with your credentials.'
                from_email = 'mobitrailappsec2017@gmail.com'  # Replace with your email
                recipient_list = [email]  # Passing dynamic email ID
                send_mail(subject, message, from_email, recipient_list)
            # return HttpResponse(response)    
            
            return JsonResponse(response)
    
    except Exception as e:
        print(e)
        response = {'status': False, 'message': 'Something went wrong'}
        # return HttpResponse(response)
        return JsonResponse(response)


# @csrf_exempt
# def signin(request):
#     if request.method=='POST':
#         print(f"in signin function")
#         response={}
#         response['status']=True
#         response['message']='Signin successful'
#         return JsonResponse(response)