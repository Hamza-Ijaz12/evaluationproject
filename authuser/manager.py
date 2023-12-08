from django.contrib.auth.models import UserManager
from django.core.mail import send_mail
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver



class CustomUserManager(UserManager):
    def _create_user(self,email,password,**extrafields):
        print("===============Create user called")
        if not email:
            raise ValueError('You have not provided a Valid email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        # Calling set_password method
       
        user.set_password(password)  # Sets the raw password
        print("pasword===============",password)
        print("pasword+++++++++++++++++++",user.password)
            

        # Saving the user
        # if your have a sepereate database for user saving
        user.save(using =self.db)
        # simple
        # user.save()
       
        return user
    
    def create_user(self,email=None,password = None, **extrafields):
        extrafields.setdefault('role','student')
        extrafields.setdefault('is_staff',False)
        extrafields.setdefault('is_superuser',False)
        return self._create_user(email,password, **extrafields)

    def create_superuser(self,email=None,password = None, **extrafields):
        extrafields.setdefault('role','admin')
        extrafields.setdefault('is_staff',True)
        extrafields.setdefault('is_superuser',True)
        return self._create_user(email,password, **extrafields)


   
    