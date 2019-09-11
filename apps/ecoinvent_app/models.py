from django.db import models
from django.utils.dateparse import parse_date
from datetime import date
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        fname = postData['fname']
        lname = postData['lname']
        email = postData['email']
        username = postData['username']
        pw = postData['password']
        confirmpw = postData['confirmpassword']
        already_taken = User.objects.filter(username=username)
        if len(fname) < 3:
            errors['fname'] = 'First name should be at least 3 characters'
        if len(lname) < 3:
            errors['lname'] = 'Last name should be at least 3 characters'
        if len(username) < 2:
            errors['username'] = 'Username should be at least 2 characters'
        if len(already_taken) > 0:
            errors['username_taken'] = 'Sorry, this username is already taken, try again'
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors['email'] = 'Please enter a valid email address'
        if len(pw) < 8:
            errors['pword'] = 'Please enter a password greater than 7 characters'
        elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%_*?&])[A-Za-z\d@$!%_*?&]{3,}$", pw):
            errors['password'] = 'Please use a special character, one uppercase and one lowercase letter'
        if pw != confirmpw:
            errors['pwordmatch'] = 'Please make sure your passwords match!'
        return errors


    def login_validator(self, postData):
        errors = {}
        username = postData['username']
        password = postData['password']
        user_check = User.objects.filter(username=username)
        if len(user_check) < 1:
            errors['usernamenotfound'] = 'No username found'
        elif not bcrypt.checkpw(password.encode(), user_check[0].password.encode()):
            errors['passwordnotmatch'] = 'Username/Password does not match our records. Please try again'
        return errors

    def duplicateDataValidator(self, postData):
        errors = {}
        filenameCheck = ActData.objects.filter(file_name=postData)
        print(postData)
        print(filenameCheck)
        if len(filenameCheck) > 0:
            errors['dup_file'] = 'Sorry, this file has already been uploaded'
        print(errors['dup_file'])
        return errors





class User(models.Model):
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    username = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    password = models.CharField(max_length=90)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class ActData(models.Model):
    activityName = models.CharField(max_length=90)
    geography = models.CharField(max_length=90)
    productName = models.CharField(max_length=90)
    file_name = models.TextField()
    uploaded_file = models.TextField()
    system_model = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_uploaded = models.ForeignKey(User, related_name="datasets_uploaded", blank=True)
    objects = UserManager()
