from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.


# Cohorts model
class Cohorts(models.Model):
    classname               = models.CharField(max_length=20,default='')
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.classname
    
class Lesson(models.Model):
    cohort                  = models.ForeignKey(Cohorts,on_delete=models.CASCADE)
    lesson_name             = models.CharField(max_length=20,default='')
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.lesson_name
    

class Score(models.Model):
    student                 = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    score                   = models.CharField(max_length=3,default=0)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.score
    # UC stands for Cohorts and User modal
class Linking_UC (models.Model):
    cohort                  = models.ForeignKey(Cohorts,on_delete=models.CASCADE)
    student                 = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-updated','-created']


# Tasks Models

def path_define(self, filename):
    lesson_classname        = self.lesson.cohort.classname
    lesson_name             = self.lesson.lesson_name
    task_name               = self.task_name

    return f'{lesson_classname}/{lesson_name}/{task_name}/{filename}'


# T1
class T1(models.Model):
    # task_name               = models.CharField(default='',null=True)
    task_name               = models.TextField(default='',null=True)
    audio1                  = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio2                  = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio3                  = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio4                  = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])

    opt_image1              = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    opt_image2              = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    opt_image3              = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    opt_image4              = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    
    
    answer                  = models.CharField(max_length=20,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name

# T2
class T2(models.Model):
    # task_name               = models.CharField(default='',null=True)
    task_name               = models.TextField(default='',null=True)
    audio1                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio2                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio3                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio4                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    
    opt_audio1                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    opt_audio2                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    opt_audio3                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    opt_audio4                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    
    
    answer                  = models.CharField(max_length=20,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name

# T3
class T3(models.Model):
    # task_name               = models.CharField(default='',null=True)
    task_name               = models.TextField(default='',null=True)
    task_img                = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    Option1                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    Option1_iscorrect       = models.BooleanField(default=False)
    Option2                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    Option2_iscorrect       = models.BooleanField(default=False)
    Option3                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    Option3_iscorrect       = models.BooleanField(default=False)
    Option4                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    Option4_iscorrect       = models.BooleanField(default=False)
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name
    
# T4
class T4(models.Model):
    # task_name               = models.CharField(default='',null=True)
    task_name               = models.TextField(default='',null=True)
    audio1                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio2                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio3                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio4                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    word1                   = models.CharField(max_length=20,default='')
    word2                   = models.CharField(max_length=20,default='')
    word3                   = models.CharField(max_length=20,default='')
    word4                   = models.CharField(max_length=20,default='')

    answer                  = models.CharField(max_length=20,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name



# T5
class T5(models.Model):
    # task_name               = models.CharField(default='',null=True)
    task_name               = models.TextField(default='',null=True)
    sound                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    image1                   = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    image2                   = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    image3                   = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    image4                   = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    
    answer                  = models.CharField(max_length=20,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name

# T6
class T6(models.Model):
    # task_name               = models.CharField(default='',null=True)
    task_name               = models.TextField(default='',null=True)
    audio1                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio2                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio3                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio4                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    answer                  = models.CharField(max_length=20,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name


# T7
class T7(models.Model):
    # task_name               = models.CharField(default='',null=True)
    task_name               = models.TextField(default='',null=True)
    text_blank              = models.TextField(default='')
    answer                  = models.CharField(max_length=20,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)

    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name
    
# T8
class T8(models.Model):
    # task_name               = models.CharField(default='',null=True)
    task_name               = models.TextField(default='',null=True)
    sound                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    answer                  = models.CharField(max_length=20,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name
    
    
    
# User Task Assign Model
class UserTask(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    task = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user.email}'s task: {self.task}"
    

