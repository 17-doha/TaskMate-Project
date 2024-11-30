# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import Login

# @admin.register(Login)
# # Generating Custom user admin and make this consistent with the User in Django
# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email', 'password', 'username', 'age', 'phone_num', 'theme_is_light', 'badge_name')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     list_display = ('email', 'username', 'is_staff', 'is_active')
#     search_fields = ('email', 'username')
#     ordering = ('email',)
