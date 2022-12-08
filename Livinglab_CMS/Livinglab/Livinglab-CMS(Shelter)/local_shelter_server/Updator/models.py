from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings
from tinymce.models import HTMLField

def profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    shelter_id = Shelter.objects.last().id
    print("shelter : 쉘터 ID", shelter_id)
    print("user : 파일명", filename)

    return 'Shelter_Profile/SID-{0}/{1}'.format(shelter_id, filename)

def Advertisement_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    advertisement_id = Advertisement.objects.last().id
    print("shelter : 광고 ID", advertisement_id)
    print("user : 파일명", filename)

    return 'Advertisement/AID-{0}/{1}'.format(advertisement_id, filename)

def Community_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    comment_id = Comment.objects.last().id
    print("shelter : 댓글 ID", comment_id)
    print("user : 파일명", filename)

    return 'Community/CID-{0}/{1}'.format(comment_id, filename)

def user_directory_path(instance, filename):
    content_id = Content.objects.last().id
    cType = Content.objects.last().contentType
    print("content : 콘텐츠 ID", content_id)
    print("filetype : 파일타입", cType)
    print("file : 파일명", filename)

    return 'Contents/CID-{0}/{1}/{2}'.format(content_id, cType, filename)

STATUS = (
    ('활성화', 'ACTIVATE'),
    ('대기', 'PAUSED'),
    ('정지', 'BANNED'),
)

class Shelter(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=True)  # 이름
    shelter_description = models.TextField(max_length=500, blank=True, null=True, default="여기에 입력 하시오.")
    shelter_status = models.CharField(max_length=20, choices=STATUS, null=True, default="대기") #상태

    add_states = models.CharField(max_length=50, null=True)  # 도/시
    add_city = models.CharField(max_length=50, null=True) # 시/군/구
    add_town = models.CharField(max_length=50, null=True) # 읍/면/동
    add_last = models.CharField(max_length=50, null=True) # 나머지 상세주소

    access_number = models.CharField(max_length=10, null=False, default="0000000") # 인증번호
    createDate = models.DateTimeField(auto_now_add=True)  # 등록일자
    lastEditDate = models.DateTimeField(auto_now=True)  # 수정일자
    localupdateDate = models.DateTimeField(auto_now=True)  # 로컬쉘터서버 업데이트 일자

    def __str__(self):
        return self.title

class Shelter_media(models.Model):
    id = models.AutoField(primary_key=True)

    shelter_profile = models.FileField(null=True, upload_to=profile_directory_path, blank=True, \
                                       validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    contentQR = models.CharField(max_length=200, null=True)
    communityQR = models.CharField(max_length=200, null=True)

    shelterFK = models.ForeignKey(Shelter, on_delete=models.CASCADE, db_column="shelterFK", null=True, blank=True)

class Community(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    createDate = models.DateTimeField(auto_now_add=True)
    lastEditDate = models.DateTimeField(auto_now=True)
    isUpdate = models.BooleanField(default=False)  # 로컬쉘터서버 업데이트 여부

    community_status = models.CharField(max_length=20, choices=STATUS, null=True, default="대기")  # 상태

    shelterFK = models.ForeignKey(Shelter, on_delete=models.CASCADE,
                                  db_column="shelterFK", null=True, blank=True, related_name='Shelter_Community')

    def __str__(self):
        return self.name

class Daily_Board(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    board_status = models.CharField(max_length=20, choices=STATUS, null=True, default="대기")  # 상태

    createDate = models.DateTimeField(auto_now_add=True)
    lastEditDate = models.DateTimeField(auto_now=True)
    isUpdate = models.BooleanField(default=False)  # 로컬쉘터서버 업데이트 여부

    communityFK = models.ForeignKey(Community, on_delete=models.CASCADE,
                                    db_column="communityFK", null=True, blank=True, related_name='Community_Dboard')

    def __str__(self):
        return self.name

class Issue_Board(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    board_status = models.CharField(max_length=20, choices=STATUS, null=True, default="대기")  # 상태

    createDate = models.DateTimeField(auto_now_add=True)
    lastEditDate = models.DateTimeField(auto_now=True)
    isUpdate = models.BooleanField(default=False)  # 로컬쉘터서버 업데이트 여부

    communityFK = models.ForeignKey(Community, on_delete=models.CASCADE,
                                    db_column="communityFK", null=True, blank=True, related_name='Community_Iboard')

    def __str__(self):
        return self.name

Board_Type = (
    ('Normal', '일상게시판'),
    ('Issue', '이슈게시판'),
)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    email = models.EmailField(max_length=128, verbose_name="사용자 이메일", null=True, blank=True)
    comment_status = models.CharField(max_length=20, choices=STATUS, null=True, default="대기")  # 상태
    boardType = models.CharField(max_length=10, choices=Board_Type, null=True, blank=True)

    dboardFK = models.ForeignKey(Daily_Board, on_delete=models.CASCADE, db_column="dboardFK",
                                null=True, blank=True, related_name='Dboard_Comment')

    iboardFK = models.ForeignKey(Issue_Board, on_delete=models.CASCADE, db_column="iboardFK",
                                 null=True, blank=True, related_name='Iboard_Comment')

    createDate = models.DateTimeField(auto_now_add=True)
    lastEditDate = models.DateTimeField(auto_now_add=True)
    isUpdate = models.BooleanField(default=False)  # 로컬쉘터서버 업데이트 여부

    def __str__(self):
        return self.text

class Comment_media(models.Model):
    image = models.FileField(null=True,
                             upload_to=Community_directory_path,
                             blank=True,
                             validators=[
                                 FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

    commentFK = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                        db_column="commentFK", null=True, blank=True, related_name='Comment_media')


# (공익캠페인, 일반광고) -> 전체쉘터배포, 쉘터 광고 -> 지정쉘터
Ad_Type = (
    ('일반광고', '일반광고'),
    ('공익광고', '공익광고'),
    ('지역광고', '지역광고'),
)

class Advertisement(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    adType = models.CharField(max_length=10, choices=Ad_Type)
    company = models.CharField(max_length=20)
    advertiser = models.CharField(max_length=20)             # 광고사 관계자
    email = models.EmailField(max_length=128, verbose_name="사용자 이메일")
    phone = models.CharField(max_length=20)
    advertisement_status = models.CharField(max_length=20, choices=STATUS, null=True, default="대기")  # 상태

    createDate = models.DateTimeField(auto_now_add=True)
    lastEditDate = models.DateTimeField(auto_now=True)
    isUpdate = models.BooleanField(default=False)  # 로컬쉘터서버 업데이트 여부

    shelterFK = models.ForeignKey(Shelter, on_delete=models.CASCADE,
                                  db_column="shelterFK", null=True, blank=True, related_name='Shelter_Advertisement')

    def __str__(self):
        return self.name

class Advertisement_media(models.Model):
    content = models.FileField(null=True, upload_to=Advertisement_directory_path, blank=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'mp4', 'avi'])])
    type = models.CharField(max_length=10)

    advertisementFK = models.ForeignKey(Advertisement, on_delete=models.CASCADE,
                                  db_column="advertisementFK", null=True, blank=True, related_name='Ad_Media')

class Content(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=128, verbose_name="사용자 이메일", null=True, blank=True)

    content_status = models.CharField(max_length=5, null=True, default="대기")  # 상태
    contentType = models.CharField(max_length=10, null=True)
    hits = models.DecimalField(max_digits=11, decimal_places=0, default=0, null=True)   # 조회수
    likes = models.DecimalField(max_digits=11, decimal_places=0, default=0, null=True)   # 좋아요수

    createDate = models.DateTimeField(auto_now_add=True)
    lastEditDate = models.DateTimeField(auto_now=True)
    isUpdate = models.BooleanField(default=False)  # 로컬쉘터서버 업데이트 여부

    shelterFK = models.ForeignKey(Shelter,
                                  on_delete=models.CASCADE,
                                  db_column="shelterFK",
                                  null=True,
                                  blank=True,
                                  related_name='Shelter_Content')

    def __str__(self):
        return self.title

class Content_Description(models.Model):
    id = models.AutoField(primary_key=True)
    upload_file = models.FileField(null=True,
                                   upload_to=user_directory_path,
                                   blank=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'mp4'])])

    description = HTMLField(null=True, blank=True)
    width = models.CharField(max_length=10, null=True)
    height = models.CharField(max_length=10, null=True)
    HVType = models.CharField(max_length=10, null=True)  # 가로형 세로형 horizontal, vertical
    thumbnailPath = models.CharField(max_length=200, null=True)

    contentFK = models.ForeignKey(Content, on_delete=models.CASCADE, db_column="contentFK", null=True, blank=True, \
                                  related_name='Content_Description')