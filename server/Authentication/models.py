from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

def profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print("user : 사용자 ID", instance.user.id)
    print("user : 파일명", filename)

    return 'Admin_Profile/UID-{0}/{1}'.format(instance.user.id, filename)

SYSTEM_AUTHORITY = (
        ('최고관리자', 'Super_Admin'),
        ('쉘터관리자', 'Shelter_Admin'),
    )

STATUS = (
    ('활성화', 'ACTIVATE'),
    ('탈퇴', 'STOPED'),
    ('대기', 'PAUSED'),
    ('정지', 'BANNED'),

)

class CustomUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=0)
    nickname = models.CharField(max_length=50, null=True, default="여기에 입력 하시오.")
    user_description = models.TextField(max_length=500, blank=True, null=True, default="여기에 입력 하시오.")
    user_profile = models.FileField(null=True, upload_to=profile_directory_path, blank=True, \
                                    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    user_auth = models.CharField(max_length=200, choices=SYSTEM_AUTHORITY, null=True, default=0)
    user_status = models.CharField(max_length=20, choices=STATUS, null=True, default="대기")

    def __str__(self):
        return self.nickname


