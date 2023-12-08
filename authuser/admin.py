from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .utils import send_email_to_client,random_passowrd

class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'role', 'created', 'updated')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new user being added
            new_password = random_passowrd()  # Replace this with your logic to generate a temporary password
            request.session['your_password'] = new_password
            obj.set_password(new_password)
            print(f"Username: {obj.username}, Email: {obj.email}, Temporary Password: {new_password}")
        
        if ('email' in form.changed_data and obj.email != '' and obj.role == 'teacher') : 
            print('---------------here1',request.session['your_password'])
            if 'your_password' in request.session:
                print('---------------here2')
                   
                message = (f"Username: {obj.username},\n New Email: {obj.email},\n Temporary Password: {request.session['your_password']}\nYour Role: {obj.role}")
                send_email_to_client(message,obj.email)
                print('-----------------here3')
                del request.session['your_password']
        else:
                
            if ('role' in form.changed_data and obj.email != '' and obj.role == 'teacher') : 
                if request.session['your_password']:
                    message = (f"Username: {obj.username},\n New Email: {obj.email},\n Temporary Password: {request.session['your_password']} \nYour Role: {obj.role}")
                    send_email_to_client(message,obj.email)
                    del request.session['your_password']
                    
            
          
        super().save_model(request, obj, form, change)

admin.site.register(User, AccountAdmin)
