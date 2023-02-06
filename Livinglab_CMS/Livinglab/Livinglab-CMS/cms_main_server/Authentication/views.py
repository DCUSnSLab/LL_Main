from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from .forms import UserAdditionalSignUpForm, UserSignUpForm
from .models import CustomUser
from django.contrib.auth.models import User

def Main(request):

    print("메인페이지 뷰")
    return render(request, 'Authentication/Main.html')

def Login(request):

    print("로그인 뷰")

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']


        # get login info
        loginUser = list(User.objects.filter(username=username).values_list('id', flat=True))
        print(loginUser)

        # get user Auth
        getuserAuth = list(CustomUser.objects.filter(id=loginUser[0]).values_list('user_auth', flat=True))
        print(getuserAuth)

        # check user Auth
        checkuserAuth = list(CustomUser.objects.filter(id=loginUser[0]).values_list('user_status', flat=True))
        print(checkuserAuth)

        user = auth.authenticate(request, username=username, password=password)

        if (user is not None) and checkuserAuth[0] == "활성화":
            print("??")

            auth.login(request, user)

            print("login success")
            print("current user " + str(user))

            if getuserAuth[0] == "쉘터관리자":
                return redirect('Dashboard_minor')

            elif getuserAuth[0] == "최고관리자":
                return redirect('Dashboard')

        # else:
        #     error_msg = 'username or password is incorrect.'
        #     return render(request, 'user/login.html', {'error': error_msg})

    else:
        return render(request, 'Authentication/Login.html')

def Signup(request):
    print("회원가입 뷰")

    if request.method == 'POST':

        form = UserSignUpForm(request.POST)
        additional_form = UserAdditionalSignUpForm(request.POST, request.FILES)


        if form.is_valid() and additional_form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = form.save()

            customuser = additional_form.save(commit=False)
            customuser.user = user
            customuser.save()

            user = authenticate(username=username, password=password)
            auth.login(request, user)

            return redirect('/')
    else:
        form = UserSignUpForm()
        additional_form = UserAdditionalSignUpForm()

    context = {
        'form': form,
        'additional_form': additional_form
    }

    return render(request, 'Authentication/Signup.html', context)

def Logout(request):
    print("로그아웃 뷰")

    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')

    # logout으로 GET 요청이 들어왔을 때, 로그인 화면을 띄워준다.
    auth.logout(request)
    return redirect('/')