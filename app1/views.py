from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseServerError
import base64
import numpy as np
import cv2
import cfg

from cfg import htr_logger

from cfg.htr_logger import Paragraph_logger

# Create your views here.

def HomePage(request):
    return render(request, 'home.html')

def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 == pass2:
            my_user = User.objects.create_user(username, email, pass1)
            my_user.save()
            messages.success(request, 'User created successfully!')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')

def sayana_ocr_page(request):
    return render(request, 'sayanaocr.html')

import cv2

def preprocess(image):
    # Perform preprocessing operations on the image
    # Example: convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # You can add more preprocessing steps here as needed
    return gray_image



def recognition_process(test_img, uuid):
    try:
        recog_list = []
        recog_spell_check_list = []
        confidence_score_list = []
        Paragraph_logger.log(Paragraph_logger.info, "Operation_manger : Recognition process Started:")

        # for json image open these three line
        byte2image = base64.b64decode(test_img)
        test_img_np_array = np.fromstring(byte2image, dtype=np.uint8)
        np_to_img = cv2.imdecode(test_img_np_array, cv2.IMREAD_COLOR)

        Paragraph_logger.log(Paragraph_logger.info, "Operation_manger : Preprocess Starts:")
        cords = preprocess(np_to_img)
        Paragraph_logger.log(Paragraph_logger.info, "Operation_manger : Preprocess Ends:")

        Paragraph_logger.log(Paragraph_logger.info, "Operation_manger : Sorting Starts:")
        sorted_cords, _ = sort_bounding_boxes(cords)
        Paragraph_logger.log(Paragraph_logger.info, "Operation_manger : Sorting Ends:")

        greyscale_img = cv2.cvtColor(np_to_img, cv2.COLOR_BGR2GRAY)

        for j in sorted_cords:
            try:
                crop = np_to_img[int(j[1]):int(j[3]), int(j[0]):int(j[2])]
                automated_response = check_line_removal(crop)
                if automated_response == 'NO':
                    crop = greyscale_img[int(j[1]):int(j[3]), int(j[0]):int(j[2])]
                    _, thresh = cv2.threshold(crop, 0, 255, cv2.THRESH_OTSU)
                    # thresh = skew_correction(thresh)
                    thresh = slant_correction(thresh)
                else:
                    crop = np_to_img[int(j[1]):int(j[3]), int(j[0]):int(j[2])]
                    thresh = skew_correction(crop)
                    thresh = slant_correction(thresh)
                    thresh = line_removal_and_restoration(thresh)

                recognized_string, confidence_score = Recognition(thresh)
                autocorrected = text_proofreading_with_autocorrect(recognized_string)

            except Exception as error:
                raise error
            recog_list.append(recognized_string)
            recog_spell_check_list.append(autocorrected)
            confidence_score_list.append(confidence_score)

        raw_recog_para, word_confidence_pair = get_paragraph_from_words(recog_list, confidence_score_list)
        improve_recog_para, word_confidence_pair = get_paragraph_from_words(recog_spell_check_list, confidence_score_list)

        Paragraph_logger.log(Paragraph_logger.debug, "operation_manger : recognition done : recongnize result : {} : confidence score : {}".format(raw_recog_para, word_confidence_pair))
        return raw_recog_para, improve_recog_para, word_confidence_pair

    except Exception as error:
        Paragraph_logger.log(Paragraph_logger.error, "operation_manager : recognition_process : failure : {}".format(error))
        raise error


def ocr_process_view(request):
    if request.method == 'POST':
        # Get image data and UUID from the request
        test_img = request.POST.get('image_data')
        uuid = request.POST.get('uuid')

        try:
            # Call the recognition_process function
            raw_recog_para, improve_recog_para, word_confidence_pair = recognition_process(test_img, uuid)

            # Process the OCR results further as needed

            # Return the OCR results as a JSON response
            return JsonResponse({
                'raw_recog_para': raw_recog_para,
                'improve_recog_para': improve_recog_para,
                'word_confidence_pair': word_confidence_pair
            })
        except Exception as e:
            # Handle exceptions if recognition_process fails
            return HttpResponseServerError("OCR processing failed: {}".format(e))

    else:
        # Return an error response for non-POST requests
        return HttpResponseNotAllowed(['POST'])
