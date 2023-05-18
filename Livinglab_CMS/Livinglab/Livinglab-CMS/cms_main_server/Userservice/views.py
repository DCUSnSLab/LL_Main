from django.shortcuts import render, redirect

from Management.models import Shelter, Community, Daily_Board, Issue_Board, Comment, \
    Content

from .forms import AddCommentForm, AddCommentMediaForm, \
UploadContentForm, AddContentDescriptionForm

from Utility import utility

import os
from pathlib import Path

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# jmeter 실험 중 csrf 오류 발생 시 적용
# https://velog.io/@langssi/django-Forbidden-CSRF-cookie-not-set.-%EC%98%A4%EB%A5%98-%ED%95%B4%EA%B2%B0
@method_decorator(csrf_exempt, name='dispatch')
def AddCommunityComment(request, id):
    print("커뮤니티 댓글 달기")

    shelter = Shelter.objects.get(id=id)

    if request.method == 'POST':

        form = AddCommentForm(request.POST)
        media_form = AddCommentMediaForm(request.POST, request.FILES)  # 파일만 보내더라도 request.POST 적어야함

        print(form.is_valid(), media_form.is_valid())
        if form.is_valid() and media_form.is_valid():

            text = form.cleaned_data.get('text')
            email = form.cleaned_data.get('email')
            boardType = form.cleaned_data.get('boardType')
            image = media_form.cleaned_data.get('image')

            print("데이터 들어옴", text, image, email, boardType)

            comment = form.save(commit=False)

            community = Community.objects.get(shelterFK=shelter.id)
            print("커뮤니티 ID", community.id)

            if boardType == "Normal":
                board = Daily_Board.objects.get(communityFK=community.id)
                print("일상게시판 id", board.id)
                comment.dboardFK = board
                comment.comment_status = "대기"
                comment.save()

                media = media_form.save(commit=False)
                c_id = Comment.objects.last()
                media.commentFK = c_id
                media.save()

            elif boardType == "Issue":
                board = Issue_Board.objects.get(communityFK=community.id)
                print("이슈게시판 id", board.id)
                comment.iboardFK = board
                comment.comment_status = "대기"
                comment.save()

                media= media_form.save(commit=False)
                c_id = Comment.objects.last()
                media.commentFK = c_id
                media.save()

            return redirect('AddCommunityComment', shelter.id)
    else:

        form = AddCommentForm()
        media_form = AddCommentMediaForm()

    context = {
        'form': form,
        'media_form': media_form,
        'shelter': shelter
    }

    return render(request, 'Userservice/AddComment.html', context)

# jmeter 실험 중 csrf 오류 발생 시 적용
# https://velog.io/@langssi/django-Forbidden-CSRF-cookie-not-set.-%EC%98%A4%EB%A5%98-%ED%95%B4%EA%B2%B0
@method_decorator(csrf_exempt, name='dispatch')
def UploadContent(request, id):
    # print("콘텐츠 업로드")

    shelter = Shelter.objects.get(id=id)

    if request.method == 'POST':

        form = UploadContentForm(request.POST)
        addition_form = AddContentDescriptionForm(request.POST , request.FILES)  # 파일만 보내더라도 request.POST 적어야함

        # print(form.is_valid(), addition_form.is_valid())
        if form.is_valid() and addition_form.is_valid():

            title = form.cleaned_data.get('title')
            email = form.cleaned_data.get('email')
            author = form.cleaned_data.get('author')
            phonenum = form.cleaned_data.get('phonenum')
            upload_file = addition_form.cleaned_data.get('upload_file')
            description = addition_form.cleaned_data.get('description')

            content = form.save(commit=False)
            content.shelterFK = shelter

            # 실험땜에 일단 주석 처리!
            file = str(addition_form.cleaned_data.get('upload_file'))
            fname, fType = utility.FileTypeCheck(file)
            content.contentType = fType


            content.save()

            addition_content = addition_form.save(commit=False)
            c_id = Content.objects.last()
            addition_content.contentFK = c_id

            addition_content.save()

            content_id = Content.objects.last().id

            BASE_DIR = Path(__file__).resolve().parent.parent
            MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
            CONTENT_DIR = "{0}/Contents/CID-{1}/{2}/{3}".format(MEDIA_ROOT,content_id, fType, file)
            THUMBNAIL_DIR = "{0}/Contents/CID-{1}/Thumbnail/".format(MEDIA_ROOT, content_id)


            # print("fTypeCheck", file)
            # print("BASE_DIR", BASE_DIR)
            # print("MEDIA_ROOT", MEDIA_ROOT)
            # print("CONTENT_DIR", CONTENT_DIR)
            # print("Thumb", THUMBNAIL_DIR)


            if fType == "Image":
                fileInfo = utility.GetFileInfo(CONTENT_DIR, fType)

                addition_content.width = fileInfo['width']
                addition_content.height = fileInfo['height']
                addition_content.HVType = fileInfo['HVType']

            elif fType == "Video":
                fileInfo = utility.GetFileInfo(CONTENT_DIR, fType)

                addition_content.width = fileInfo['width']
                addition_content.height = fileInfo['height']
                addition_content.HVType = fileInfo['HVType']

                thumbPath = utility.createDirectory(THUMBNAIL_DIR)
                utility.GetThumbnail(CONTENT_DIR, thumbPath)

                addition_content.thumbnailPath = utility.CutFilePath(THUMBNAIL_DIR, "media/")

            addition_content.save()

            # print("콘텐츠 업로드 완료")

            return redirect('UploadContent', shelter.id)
    else:

        form = UploadContentForm()
        addition_form = AddContentDescriptionForm()

    context = {
        'form': form,
        'addition_form': addition_form,
        'shelter': shelter
    }

    return render(request, 'Userservice/UploadContent.html', context)
