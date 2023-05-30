from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from Authentication.models import CustomUser

from Management.models import Shelter, Shelter_media,\
    Community, Issue_Board, Daily_Board, Comment,Comment_media, \
    Advertisement, Advertisement_media, \
    Content, Content_Description

from Authentication.forms import UserSignUpForm, UserAdditionalSignUpForm

from .forms import ShelterRegisterForm, ShelterMediaForm, AdRegisterForm, AdMediaRegisterForm

from Utility import utility

import random

def GetSystemInfo():
    # all admin count
    admin = User.objects.all()
    adminCnt = admin.count()

    shelter = Shelter.objects.all()
    shelterCnt = shelter.count()

    community = Community.objects.all()
    communityCnt = community.count()

    advertisement = Advertisement.objects.all()
    advertisementCnt = advertisement.count()

    content = Content.objects.all()
    contentCnt = content.count()

    return adminCnt, shelterCnt, communityCnt, advertisementCnt, contentCnt


#-----------------------------------------CMS 관리자 대시보드-----------------------------------------#
def Dashboard(request):

    print("수퍼관리자 대시보드")

    adminCnt, shelterCnt, communityCnt, advertisementCnt, contentCnt = GetSystemInfo()

    context = {
        'adminCnt': adminCnt,
        'shelterCnt': shelterCnt,
        'communityCnt': communityCnt,
        'advertisementCnt': advertisementCnt,
        'contentCnt': contentCnt
    }

    return render(request, 'Management/dashboard.html', context)

def Dashboard_minor(request):

    print("쉘터관리자 대시보드")

    adminCnt, shelterCnt = GetSystemInfo()

    context = {
        'adminCnt': adminCnt,
        'shelterCnt': shelterCnt
    }

    return render(request, 'Management/dashboard_minor.html', adminCnt)
#-----------------------------------------CMS 관리자 대시보드-----------------------------------------#

#-----------------------------------------CMS 관리자 관리-----------------------------------------#
# 등록관리자 관리(권한 부여 authorization)
def Administration(request):

    print("관리자 관리")

    simple_admin = User.objects.all().values('id', 'username', 'email')
    simple_admin_additional = CustomUser.objects.all().values('user_auth', 'user_status')

    ziplist = zip(simple_admin, simple_admin_additional)

    context = {
        'ziplist': ziplist
    }

    return render(request, 'Management/Administration.html', context)

def AdminChange(request, id):

    simple_admin = User.objects.all().values('id', 'username', 'email')
    simple_admin_additional = CustomUser.objects.all().values('user_auth', 'user_status')

    ziplist = zip(simple_admin, simple_admin_additional)

    context = {
        'ziplist': ziplist
    }

    print("관리자 권한변경")
    if request.method == 'POST':

        auth = request.POST['user_auth']
        # admin = CustomUser.objects.filter(id=id).values('user_auth', 'user_status')
        print("id :", id)
        admin = CustomUser.objects.get(user_id=id)
        print(admin, id)

        if auth == "활성화":
            admin.user_status = "활성화"
            admin.save()

        elif auth == "탈퇴":
            print(admin.user_status)
            admin.user_status = "탈퇴"
            admin.save()

        elif auth == "대기":
            admin.user_status = "대기"
            admin.save()

        elif auth == "정지":
            admin.user_status = "정지"
            admin.save()

        return redirect('Admin')

    else:
        return render(request, 'Management/Administration.html', context)

def ShowDetailAdmin(request, id):
    print("자세히 페이지")

    adminInfo = User.objects.get(id=id)
    adminCustomInfo = CustomUser.objects.get(id=id)

    # 역참조
    shelter_admin = User.objects.get(id=id).shelter_admin.all().values('title')

    # 해야할 것
    # 유저가 관리하는 쉘터의 이름을 가져옴
    # 쉘터는 유저의 외래키를 가지고 있음
    # 유저 ID들 가지는 쉘터의 이름을 얻어야함


    print("id :", id, "adminInfo : ", adminInfo, "adminCustomInfo : ",
          adminCustomInfo, "shelter_admin :", shelter_admin)

    context = {
        'adminInfo': adminInfo,
        'adminCustomInfo': adminCustomInfo,
        'shelter_admin': shelter_admin
    }

    return render(request, 'Management/DetailAdmin.html', context)

def Mypage(request):
    print("마이페이지")

    current_user = request.user

    adminInfo = User.objects.get(id=current_user.id)
    adminCustomInfo = CustomUser.objects.get(id=current_user.id)

    # 역참조
    shelter_admin = User.objects.get(id=current_user.id).shelter_admin.all().values('title')

    context = {
        'adminInfo': adminInfo,
        'adminCustomInfo': adminCustomInfo,
        'shelter_admin': shelter_admin
    }

    return render(request, 'Management/Mypage.html', context)

# 가장 마지막에 수정
def EditMyinfo(request):

    print("내 정보 수정 페이지")

    current_user = request.user

    adminInfo = User.objects.get(id=current_user.id)
    adminCustomInfo = CustomUser.objects.get(id=current_user.id)

    print("id :", current_user.id, "adminInfo : ", adminInfo, "adminCustomInfo : ", adminCustomInfo)

    if request.method == 'POST':

        print("여긴가")

        form = UserSignUpForm(request.POST)
        additional_form = UserAdditionalSignUpForm(request.POST, request.FILES)

        print(form)
        print(additional_form)

        print(form.is_valid())
        print(additional_form.is_valid())

        if form.is_valid() and additional_form.is_valid():
            print("asdasd")

            adminInfo.username = form.cleaned_data['username']
            adminInfo.last_name = form.cleaned_data['last_name']
            adminInfo.first_name = form.cleaned_data['first_name']
            adminInfo.email = form.cleaned_data['email']
            print(adminInfo.username)
            print(adminInfo.last_name)
            print(adminInfo.first_name)
            print(adminInfo.email)

            adminInfo.save()

            adminCustomInfo.nickname = additional_form.cleaned_data['nickname']
            adminCustomInfo.user_profile = additional_form.cleaned_data['user_profile']
            adminCustomInfo.user_description = additional_form.cleaned_data['user_description']
            adminCustomInfo.save()

            context = {
                'adminInfo': adminInfo,
                'adminCustomInfo': adminCustomInfo,
                'form': form,
                'additional_form': additional_form
            }
            return redirect('/')
            # return render(request, 'Management/Mypage.html', context)

    else:
        print("정보 미입력")
        form = UserSignUpForm()
        additional_form = UserAdditionalSignUpForm()

    context = {
        'adminInfo': adminInfo,
        'adminCustomInfo': adminCustomInfo,
        'form': form,
        'additional_form': additional_form
    }

    return render(request, 'Management/EditMyInfo.html', context)
#-----------------------------------------CMS 관리자 관리-----------------------------------------#

#-----------------------------------------CMS 쉘터 관리-----------------------------------------#
def ViewShelter(request):

    print("쉘터관리 페이지")

    shelter = Shelter.objects.all()

    context = {
        'shelter': shelter
    }

    return render(request, 'Management/ViewShelter.html', context)

def UpdateShelterStatus(request, id):

    print("쉘터 권한변경")

    shelter = Shelter.objects.all()

    context = {
        'shelter': shelter
    }

    print("쉘터 권한변경")
    if request.method == 'POST':

        auth = request.POST['shelter_auth']
        shelter = Shelter.objects.get(id=id)
        print(shelter, id)

        if auth == "활성화":
            shelter.shelter_status = "활성화"
            shelter.save()

        elif auth == "대기":
            shelter.shelter_status = "대기"
            shelter.save()

        elif auth == "정지":
            shelter.shelter_status = "정지"
            shelter.save()

        return redirect('ViewShelter')

    else:
        return render(request, 'Management/ViewShelter.html', context)

def RegisterShelter(request):

    print("쉘터등록")
    admin_list = User.objects.all()

    if request.method == 'POST':

        form = ShelterRegisterForm(request.POST)
        media_form = ShelterMediaForm(request.POST, request.FILES) # 파일만 보내더라도 request.POST 적어야함

        if form.is_valid() and media_form.is_valid():

            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('shelter_description')
            states = form.cleaned_data.get('add_states')
            city = form.cleaned_data.get('add_city')
            town = form.cleaned_data.get('add_town')
            last = form.cleaned_data.get('add_last')

            profile = media_form.cleaned_data.get('shelter_profile')

            status = request.POST['shelter_auth']
            admin = request.POST['admin_list']

            community_title = title + " " + "커뮤니티"
            print(title, description, profile, states, city, town, last, status, admin, community_title)

            shelter = form.save(commit=False)
            shelter.shelter_status = status

            admin_user = User.objects.get(id=admin[0])
            shelter.userFK = admin_user

            acess_num = random.randrange(1111111, 9999999)  # 사이니지 인증번호 랜덤 생성
            shelter.access_number = str(acess_num)
            shelter.save()

            shelter_media = media_form.save(commit=False)
            shelter_id = Shelter.objects.last()
            shelter_media.shelterFK = shelter_id
            print("dd", shelter_media.shelterFK)


            # 쉘터 QR 코드 생성 및 경로 저장
            contSavePath, comSavePath, adSavePath = utility.MakeQRcode(shelter.id)

            contSavePathSplit = contSavePath.split('/media/')
            comSavePathSplit = comSavePath.split('/media/')
            adSavePathSplit = adSavePath.split('/media/')
            print(contSavePathSplit)
            print(comSavePathSplit)
            print(adSavePathSplit)
            

            shelter_media.contentQR = contSavePathSplit[1]
            shelter_media.communityQR = comSavePathSplit[1]
            shelter_media.advertisementQR = adSavePathSplit[1]
            

            shelter_media.save()

            # 쉘터 등록 시 커뮤니티도 같이 등록
            RegisterCommunity(community_title, shelter_id)
            RegisterDailyBoard()
            RegisterIssueBoard()

            return redirect('ViewShelter')
    else:

        form = ShelterRegisterForm()
        media_form = ShelterMediaForm()

    context = {
        'form': form,
        'media_form': media_form,
        'admin_list': admin_list
    }

    return render(request, 'Management/RegisterShelter.html', context)



def ShowDetailShelter(request, id):
    print("자세히 페이지")

    shelter = Shelter.objects.get(id=id)
    
    shelter_media = Shelter_media.objects.get(id=id)

    print(shelter, shelter_media)

    context = {
        'shelter': shelter,
        'shelter_media': shelter_media,
    }

    return render(request, 'Management/DetailShelter.html', context)

# 가장 마지막에 수정
def UpdateShelter(request):
    pass

#-----------------------------------------CMS 쉘터 관리-----------------------------------------#

#-----------------------------------------CMS 콘텐츠 관리-----------------------------------------#

def ViewContent(request):

    print("콘텐츠 페이지")

    content = Content.objects.all()
    condes = Content_Description.objects.all()

    print(content, condes)

    context = {
        'content': content,
        'condes': condes
    }

    return render(request, 'Management/ViewContent.html', context)

def UpdateContentStatus(request, id):

    print("콘텐츠 심사")

    content = Content.objects.all()

    context = {
        'content': content
    }

    if request.method == 'POST':

        auth = request.POST['content_auth']
        content = Content.objects.get(id=id)

        print(content, id)

        if auth == "승인":
            content.content_status = "승인"
            content.save()

        elif auth == "대기":
            content.content_status = "대기"
            content.save()

        elif auth == "반려":
            content.content_status = "반려"
            content.save()

        return redirect('ViewContent')

    else:
        return render(request, 'Management/ViewContent.html', context)

def ShowDetailContent(request, id):
    print("자세히 페이지")

    content = Content.objects.get(id=id)
    addition_content = Content_Description.objects.get(id=id)

    print(content, addition_content)

    context = {
        'content': content,
        'addition_content': addition_content,
    }

    return render(request, 'Management/DetailContent.html', context)

# 가장 마지막에 수정
def Updateontent(request):
    pass

#-----------------------------------------CMS 콘텐츠 관리-----------------------------------------#

#-----------------------------------------CMS 커뮤니티 관리-----------------------------------------#
# 커뮤니티 등록하기@!!!

def ViewCommunity(request):

    print("뷰 커뮤니티")

    community = Community.objects.all()

    # 여기에 현재 커뮤니티에 연결되어있는 모든 게시판의 댓글을 보여준다
    context = {
        'community': community
    }

    return render(request, 'Management/ViewCommunity.html', context)

def RegisterCommunity(title, shelter):
    print("커뮤니티 자동 등록")
    Community.objects.create(name=title, shelterFK=shelter)

def RegisterDailyBoard():

    print("데일리 보드 자동 등록")
    community_id = Community.objects.last()
    Daily_Board.objects.create(name="일상 게시판", communityFK=community_id)

def RegisterIssueBoard():

    print("이슈 보드 자동 등록")
    community_id = Community.objects.last()
    Issue_Board.objects.create(name="이슈 게시판", communityFK=community_id)

def GetCommunityInfo(id):
    community = Community.objects.get(id=id)
    # print("커뮤니티 ", community, "id", community.id)

    dboard = Daily_Board.objects.get(communityFK=community)
    # print("현재 커뮤니티에 해당하는 daily 보드", dboard)

    iboard = Issue_Board.objects.get(communityFK=community)
    # print("현재 커뮤니티에 해당하는 issue 보드", iboard)

    daily_comment = Comment.objects.filter(dboardFK=dboard)
    # print("현재 커뮤니티에 해당하는  daily_comment", daily_comment)

    issue_comment = Comment.objects.filter(iboardFK=iboard)
    # print("현재 커뮤니티에 해당하는  issue_comment", issue_comment)

    daily_comment_id = list(Comment.objects.filter(dboardFK=dboard).values_list('id', flat=True))
    # print("daily_comment_id", daily_comment_id)

    issue_comment_id = list(Comment.objects.filter(iboardFK=iboard).values_list('id', flat=True))
    # print("issue_comment_id", issue_comment_id)

    daily_media_list = list()
    issue_media_list = list()
    for m in daily_comment_id:
        # print('m',m)
        media = Comment_media.objects.get(commentFK=m)
        # print("미디어 id", media.id)
        daily_media_list.append(media)

    for i in issue_comment_id:
        # print('i', i)
        media = Comment_media.objects.get(commentFK=i)
        # print("미디어 id", media.id)
        issue_media_list.append(media)

    # print(daily_media_list)
    # print(issue_media_list)

    daily_ziplist = zip(daily_comment, daily_media_list)
    issue_ziplist = zip(issue_comment, issue_media_list)

    return community, daily_ziplist, issue_ziplist

def ShowDetailCommunity(request, id):
    print("커뮤니티 세부")

    community, daily_ziplist, issue_ziplist = GetCommunityInfo(id)

    context = {
        'community': community,
        'daily_ziplist': daily_ziplist,
        'issue_ziplist': issue_ziplist
    }

    return render(request, 'Management/DetailCommunity.html', context)

def UpdateCommentStatus(request, comuId, comenId):
    print("댓글 권한 변경")

    if request.method == 'POST':

        auth = request.POST['comment_auth']
        comment = Comment.objects.get(id=comenId)
        print(comment, comenId)

        if auth == "활성화":
            comment.comment_status = "활성화"
            comment.save()

        elif auth == "대기":
            comment.comment_status = "대기"
            comment.save()

        elif auth == "반려":
            comment.comment_status = "반려"
            comment.save()

        return redirect('ShowDetailCommunity', comuId)

    # else:
    #     return render(request, 'Management/DetailCommunity.html', context)



def UpdateCommunityStatus(request, id):
    print("쉘터 권한변경")

    community = Community.objects.all()

    context = {
        'community': community
    }

    if request.method == 'POST':

        auth = request.POST['community_auth']
        community = Community.objects.get(id=id)
        print(community, id)

        if auth == "활성화":
            community.community_status = "활성화"
            community.save()

        elif auth == "정지":
            community.community_status = "정지"
            community.save()

        return redirect('ViewCommunity')

    else:
        return render(request, 'Management/ViewCommunity.html', context)

#-----------------------------------------CMS 커뮤니티 관리-----------------------------------------#

#-----------------------------------------CMS 광고 관리-----------------------------------------#

def ViewAdvertisement(request):
    print("뷰 광고")

    advertisement = Advertisement.objects.all()

    context = {
        'advertisement': advertisement
    }

    return render(request, 'Management/ViewAdvertisement.html', context)

def RegisterAdvertisement(request):
    print("광고등록")
    shelter_list = Shelter.objects.all()

    if request.method == 'POST':

        form = AdRegisterForm(request.POST)
        media_form = AdMediaRegisterForm(request.POST, request.FILES) # 파일만 보내더라도 request.POST 적어야함

        if form.is_valid() and media_form.is_valid():

            name = form.cleaned_data.get('name')
            adType = form.cleaned_data.get('adType')
            company = form.cleaned_data.get('company')
            advertiser = form.cleaned_data.get('advertiser')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            advertisement_auth = request.POST['advertisement_auth']  # form 데이터 아님
            shelter = request.POST['shelter_list']                   # form 데이터 아님
            content = media_form.cleaned_data.get('content')

            advertisement = form.save(commit=False)
            advertisement.advertisement_status = advertisement_auth

            if shelter != "해당없음":
                shelter_id = Shelter.objects.get(id=shelter[0])
                advertisement.shelterFK = shelter_id

            advertisement.save()

            advertisement_media = media_form.save(commit=False)
            advertisement_id = Advertisement.objects.last()
            advertisement_media.advertisementFK = advertisement_id

            contentPath = str(media_form.cleaned_data.get('content'))

            filename, filetype = utility.FileTypeCheck(contentPath)
            advertisement_media.type = filetype
            advertisement_media.save()

            return redirect('ViewAdvertisement')
    else:

        form = AdRegisterForm()
        media_form = AdMediaRegisterForm()

    context = {
        'form': form,
        'media_form': media_form,
        'shelter_list': shelter_list
    }

    return render(request, 'Management/RegisterAdvertisement.html', context)

def ShowDetailAdvertisement(request, id):
    print("광고 세부")

    advertisement = Advertisement.objects.get(id=id)
    ad_media = Advertisement_media.objects.get(id=id)

    context = {
        'advertisement': advertisement,
        'ad_media': ad_media
    }

    return render(request, 'Management/DetailAdvertisement.html', context)

def UpdateAdvertisementStatus(request, id):
    print("광고 권한변경")

    advertisement = Advertisement.objects.all()

    context = {
        'advertisement': advertisement
    }

    if request.method == 'POST':

        auth = request.POST['advertisement_auth']
        advertisement = Advertisement.objects.get(id=id)
        print(advertisement, id, auth)

        if auth == "활성화":
            advertisement.advertisement_status = "활성화"
            advertisement.save()

        elif auth == "정지":
            advertisement.advertisement_status = "정지"
            advertisement.save()

        return redirect('ViewAdvertisement')

    else:
        return render(request, 'Management/ViewAdvertisement.html', context)

# 가장 마지막에 수정
def UpdateAdvertisement(request):
    pass



#-----------------------------------------CMS 광고 관리-----------------------------------------#
