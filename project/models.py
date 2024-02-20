from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator,MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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
    score                   = models.CharField(max_length=4,default=0)
    content_type            = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id               = models.PositiveIntegerField()
    task                    = GenericForeignKey('content_type', 'object_id')

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
    # task_name               = models.CharField(max_length=255,default='',null=True)
    task_name               = models.CharField(max_length=255,default='',null=True)
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
    # task_name               = models.CharField(max_length=255,default='',null=True)
    task_name               = models.CharField(max_length=255,default='',null=True)
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
    # task_name               = models.CharField(max_length=255,default='',null=True)
    task_name               = models.CharField(max_length=255,default='',null=True)
    task_img                = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    Option1                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    
    Option2                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    
    Option3                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    
    Option4                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    answer                  = models.CharField(max_length=20,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name
    
# T4
class T4(models.Model):
    # task_name               = models.CharField(max_length=255,default='',null=True)
    task_name               = models.CharField(max_length=255,default='',null=True)
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
    # task_name               = models.CharField(max_length=255,default='',null=True)
    task_name               = models.CharField(max_length=255,default='',null=True)
    sound1                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    sound2                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    sound3                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    sound4                   = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    sound5                   = models.FileField(null=True,blank=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    sound6                   = models.FileField(null=True,blank=True, upload_to=path_define,
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
    image5                   = models.ImageField(null=True,blank=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    image6                   = models.ImageField(null=True, blank=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    
    number_of_life           = models.IntegerField(null=True,validators=[MinValueValidator(1, message="Minimum value should be 1.")])
    total_pairs             = models.IntegerField(null=True,validators=[MinValueValidator(1, message="Minimum value should be 1.")])
    
    answer                  = models.CharField(max_length=255,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name

# T6
class T6(models.Model):
    # task_name               = models.CharField(max_length=255,default='',null=True)
    task_name               = models.CharField(max_length=255,default='',null=True)
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
    audio5                   = models.FileField(null=True,blank=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    audio6                   = models.FileField(null=True,blank=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    answer                  = models.CharField(max_length=20,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name


# T7
# Blanks Count added for multiple blanks
class T7(models.Model):
    # task_name               = models.CharField(max_length=255,default='',null=True)
    task_name               = models.CharField(max_length=255,default='',null=True)
    text_blank              = models.TextField(default='')
    option1                 = models.CharField(max_length=255,default='',null=True)
    option2                 = models.CharField(max_length=255,default='',null=True)
    option3                 = models.CharField(max_length=255,default='',null=True)
    option4                 = models.CharField(max_length=255,default='',null=True)
    blanks_count            = models.IntegerField(null=True,validators=[MinValueValidator(1, message="Minimum value should be 1.")])
    answer                  = models.CharField(max_length=255,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)

    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name
    
# T8
class T8(models.Model):
    # task_name               = models.CharField(max_length=255,default='',null=True)
    task_name               = models.CharField(max_length=255,default='',null=True)
    image                   = models.ImageField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
                                ])
    answer                  = models.CharField(max_length=20,default='')
    lesson                  = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name
    
# Keith Added 4-1-24
# SpeechQuestion
class SpeechQuestion(models.Model):
    # task_name               = models.CharField(max_length=255,default='',null=True)
    task_name               = models.CharField(max_length=255,default='',null=True)
    sound_1                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    sound_2                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    sound_3                 = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    text_answer             = models.CharField(max_length=255,default='',null=True)
    student_best_sound      = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
    student_recent_sound    = models.FileField(null=True, upload_to=path_define,
                                validators=[ FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
                                ])
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
    

@receiver(pre_delete, sender=T1)
def delete_related_objects_t1(sender, instance, **kwargs):
    # Delete related objects associated with T1 instance
    Score.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()
    UserTask.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()

@receiver(pre_delete, sender=T2)
def delete_related_objects_t2(sender, instance, **kwargs):
    # Delete related objects associated with T2 instance
    Score.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()
    UserTask.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()

@receiver(pre_delete, sender=T3)
def delete_related_objects_t3(sender, instance, **kwargs):
    # Delete related objects associated with T3 instance
    Score.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()
    UserTask.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()

@receiver(pre_delete, sender=T4)
def delete_related_objects_t4(sender, instance, **kwargs):
    # Delete related objects associated with T4 instance
    Score.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()
    UserTask.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()

@receiver(pre_delete, sender=T5)
def delete_related_objects_t5(sender, instance, **kwargs):
    # Delete related objects associated with T5 instance
    Score.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()
    UserTask.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()

@receiver(pre_delete, sender=T6)
def delete_related_objects_t6(sender, instance, **kwargs):
    # Delete related objects associated with T6 instance
    Score.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()
    UserTask.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()

@receiver(pre_delete, sender=T7)
def delete_related_objects_t7(sender, instance, **kwargs):
    # Delete related objects associated with T7 instance
    Score.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()
    UserTask.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()

@receiver(pre_delete, sender=T8)
def delete_related_objects_t8(sender, instance, **kwargs):
    # Delete related objects associated with T8 instance
    Score.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()
    UserTask.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()

# Keith Added 4-1-24
@receiver(pre_delete, sender=SpeechQuestion)
def delete_related_objects_SpeechQuestion(sender, instance, **kwargs):
    # Delete related objects associated with T8 instance
    Score.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()
    UserTask.objects.filter(content_type=ContentType.objects.get_for_model(instance), object_id=instance.id).delete()
