from django.forms import ModelForm
from .models import *



class T1form(ModelForm):
    class Meta:
        model=T1
        fields=['task_name','audio1','audio2','audio3','audio4','opt_image1','opt_image2','opt_image3','opt_image4','answer']

class T2form(ModelForm):
    class Meta:
        model=T2
        fields=['task_name','audio1','audio2','audio3','audio4','opt_audio1','opt_audio2','opt_audio3','opt_audio4','answer']


class T3form(ModelForm):
    class Meta:
        model=T3
        fields=['task_name','task_img','Option1','Option2','Option3','Option4','answer']


class T4form(ModelForm):
    class Meta:
        model=T4
        fields=['task_name','audio1','audio2','audio3','audio4','word1','word2','word3','word4','answer']

class T5form(ModelForm):
    class Meta:
        model=T5
        fields=['task_name','sound1','sound2','sound3','sound4','sound5','sound6',
                'image1','image2','image3','image4','image5','image6',
                'number_of_life','total_images', 'answer']

class T6form(ModelForm):
    class Meta:
        model=T6
        fields=['task_name','audio1','audio2','audio3','audio4','audio5','audio6','answer']

class T7form(ModelForm):
    class Meta:
        model=T7
        fields=['task_name','text_blank','option1','option2','option3','option4','blanks_count','answer']


class T8form(ModelForm):
    class Meta:
        model=T8
        fields=['task_name','image','answer']

class SpeechQuestionform(ModelForm):
    class Meta:
        model=SpeechQuestion
        fields=['task_name','sound_1','sound_2','sound_3',"text_answer"]