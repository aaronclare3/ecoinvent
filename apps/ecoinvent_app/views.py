from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .models import User, UserManager, ActData
from xml.etree.ElementTree import tostring
from django.contrib import messages
import xml.etree.ElementTree as ET
from django.conf import settings
import xmltodict
import bcrypt
import json
import os




def home(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        searchResults = ""
        if "filterBy" not in request.session:
            request.session['filterBy'] = ""
        else:
            if(request.session['filterBy'] == 'geo'):
                searchResults = ActData.objects.filter(geography__icontains = request.session['filterSearch']).values()
            elif(request.session['filterBy'] == 'act'):
                searchResults = ActData.objects.filter(activityName__icontains = request.session['filterSearch'])
            elif(request.session['filterBy'] == 'prod'):
                searchResults = ActData.objects.filter(productName__icontains = request.session['filterSearch'])

        if "toggleData" not in request.session:
            request.session['toggleData'] = -1
            jsonData = 0
        else:
            if request.session['toggleData'] != -1:
                jsonDataObject = ActData.objects.get(id = request.session['toggleData'])
                jsonData = jsonDataObject.uploaded_file
            else:
                jsonData = 0

        context = {
            'jsonData': jsonData,
            'searchResults': searchResults,
            'list_activities': ActData.objects.all().order_by("geography"),
            'current_user': current_user,
        }
        return render (request, 'ecoinvent_app/home.html', context)

def handle_xml(request):
    errors = User.objects.duplicateDataValidator(request.FILES['xmlfile'].name)
    print(request.FILES['xmlfile'].name)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        print(messages.extra_tags)
        return redirect ("/home")
    else:
        dataset_uploaded = request.FILES['xmlfile']
        x = ET.parse(dataset_uploaded)
        root = x.getroot()
        for child in root[0]:
            for element in child:
                if(element.tag == "{http://www.EcoInvent.org/EcoSpold02}geography"):
                    geography = element[0].text
        try:
            xmlToStr = ET.tostring(root, encoding='utf8', method='xml')
            ParsedXmlStr = xmltodict.parse(xmlToStr)
            xmlToJson = json.dumps(ParsedXmlStr)
        except:
            xmlToJson = "Sorry, couldn't get data"
        activityName = root[0][0][0][0].text
        productName = root[0][1][0][0].text
        systemModel = root[0][2][0][0].text
        current_user = User.objects.get(id=request.session['user_id'])
        ActData.objects.create(
            activityName = activityName, 
            productName = productName, 
            geography = geography, 
            uploaded_file = xmlToJson, 
            file_name = dataset_uploaded.name, 
            user_uploaded=current_user, 
            system_model=systemModel)
        return redirect("/home")

def deleteDataset(request, datasetId):
    DataToDelete = ActData.objects.get(id=datasetId)
    current_user = User.objects.get(id=request.session['user_id'])
    if current_user == DataToDelete.user_uploaded:  
        DataToDelete.delete()
    return redirect("/home")

def filterData(request):
    if "filterBy" not in request.session:
        request.session['filterBy'] = ""
    else:
        filterSearch = request.POST['filterSearch']
        filterBy = request.POST['filterBy']
        request.session['filterBy'] = filterBy
        request.session['filterSearch'] = filterSearch
    return redirect("/home")

def resetData(request):
    request.session['filterBy'] = ""
    request.session['filterSearch'] = ""
    return redirect("/home")

def seeData(request, datasetId):
    dataset = ActData.objects.get(id=datasetId)
    jsonData = dataset.uploaded_file
    context = {
        "jsonData": jsonData,
    }
    return render(request, 'ecoinvent_app/jsonData.html', context)


#### LOGIN/REGISTER ####

def loginpage(request):
    if "user_id" in request.session:
        return redirect("/home")
    else:
        return render(request, 'ecoinvent_app/loginpage.html')

def processlogin(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect ("/")
    else: 
        user = User.objects.get(username=request.POST['username'])
        request.session['user_id'] = user.id
        return redirect("/home")

def logout(request):
    del request.session['user_id']
    return redirect('/')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        hashedpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(first_name=fname, last_name=lname, username=username, email=email, password=hashedpw.decode())
        request.session['user_id'] = user.id
        return redirect("/home")
