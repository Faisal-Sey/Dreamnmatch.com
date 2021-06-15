import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json, requests, re, string
from random import SystemRandom
from django.http import JsonResponse
from .forms import CreateUserForm, ProfileForm, QualityForm, PaymentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib import messages
from .models import Profile, Qualities, MessageDetail, Messaging, Status, StatusImage
from django.views.generic import ListView, View, DetailView, TemplateView
from django.db.models import F
from django.db.models import Q
from django.template.defaulttags import register
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    profile = Profile.objects.all()
    context = {'profile': profile}
    return render(request, 'base.html', context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                user1 = Profile.objects.get(user=user)
                login(request, user)
                return redirect('page')
            except:
                login(request, user)
                return redirect('profile')

        else:
            messages.info(request, "Email or Password is incorrect")
            return redirect('login')

    context = {}

    return render(request, 'accounts/Login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('home')


def Signup(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request, "SignUp successful")
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/Signup.html', context)

def contact(request):
    return render(request, 'contact.html')

def profile(request):
    profile0 = Profile.objects.filter(user=request.user)
    if profile0.exists():
        return redirect('page')

    else:

        if request.method == "POST":
          full_name = request.POST.get('full_name')
          DOB = request.POST.get('DOB')
          Country = "Ghana"
          Region = request.POST.get('Region')
          Phone = request.POST.get('phone')
          Gender = request.POST.get('gender1')
          r = SystemRandom()
          single_letter = r.sample(string.ascii_lowercase, 2)
          letters = full_name.split()[0][0:2] + full_name.split()[0][-1] + ''.join(single_letter)
          img = Profile(
              user=request.user,
              First_name=full_name.split()[0],
              Last_name=full_name.split()[-1],
              Date_of_Birth=DOB,
              Country=Country,
              Region=Region,
              Phone=Phone,
              Gender=Gender,
              slug=letters,
              subscription="Free"

          )
          img.save()
          return redirect('qualities')

    return render(request, 'Profile.html')


def qualities(request):
    model1 = Profile.objects.filter(user=request.user)
    form = QualityForm(request.POST or None)
    if form.is_valid():
        looking = Profile.objects.get(user=request.user)

        add = Qualities(user=request.user, Age_group=request.POST.get('Age_group'), Region=request.POST.get('Region'),
                        Purpose=request.POST.get('Purpose'),
                        Gender=request.POST.get('gender1'))
        add.save()

        looking.other = add
        looking.save()
        form.save()
        return redirect('page')

    context = {'model': model1}
    return render(request, 'Qualities.html', context)


def policy(request):
    context = {}
    return render(request, 'Policy.html', context)


def success(request):
    context = {}
    return render(request, 'success.html', context)


def recieve_msg(request):
    from_details = Profile.objects.get(user=request.user)
    messages = MessageDetail.objects.filter(
        Q(slug__startswith=from_details.slug) | Q(slug__endswith=from_details.slug)).order_by("time")
    msg = {}


    for detail in messages:
        pers = ''
        mg = ''
        slug_main = ''
        new_slug = detail.slug[5:10] + detail.slug[0:5]
        msgs = MessageDetail.objects.filter(
            Q(slug=detail.slug) | Q(slug=new_slug)).order_by("time")

        for message in msgs:
            time = message.time
            if message.From == f'{request.user}':
                pers = "You"
                slug_main = message.slug[5:10]
            else:
                pers = message.From
                slug_main = message.slug[0:5]

            mg = message.message

        tr = time.date()
        new_time = ''
        if tr == datetime.now().date():
            new_time = str(time.time())[0:5]
            time_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
            if str(time.time())[0:2] in time_list:
                new_time += " AM"
            else:
                new_time += " PM"

        elif str(tr)[0:4] == str(datetime.now().date())[0:4]:
            if int(str(tr)[8:10]) == (int(str(datetime.now().date())[8:10]) - 1):
                new_time = "Yesterday"

        else:
            new_time = str(tr)

        msg[slug_main] = [pers, mg, new_time]

    return JsonResponse(msg)


def page(request):
    if request.method == "GET":
        profile__details = Profile.objects.filter(user=request.user)
        user_detail = Profile.objects.get(user=request.user)
        slug_user = user_detail.slug
        unread = 0
        if user_detail.other.Region == "Any":
            if user_detail.other.Age_group == "Any":
                results = Profile.objects.filter(
                    Q(Gender=user_detail.other.Gender)).exclude(
                    user=request.user
                )
            else:
                results = Profile.objects.filter(
                    Q(other__Age_group=user_detail.other.Age_group) & Q(Gender=user_detail.other.Gender)).exclude(
                    user=request.user
                )
        else:
            if user_detail.other.Age_group == "Any":
                results = Profile.objects.filter(
                    Q(Gender=user_detail.other.Gender) & Q(
                    Region=user_detail.other.Region)).exclude(
                    user=request.user
                )
            else:
                results = Profile.objects.filter(
                    Q(other__Age_group=user_detail.other.Age_group) & Q(Gender=user_detail.other.Gender) & Q(
                    Region=user_detail.other.Region)).exclude(
                    user=request.user
                )

        may_like = Profile.objects.filter(
                    Q(Gender=user_detail.other.Gender)).exclude(
                    user=request.user
        )
        may_like_list = []
        close = ""
        if user_detail.subscription == "Free":
            close = "yes"
        elif user_detail.subscription == "Amateur":
            if datetime.today().year == (user_detail.created).today().year:
                if datetime.today().month - 1 >= (user_detail.created).today().month:
                    if datetime.today().day >= (user_detail.created).today().day:
                        close = "yes"
                    else:
                        close = "no"
                else:
                    close = "no"
            else:
                close = "yes"
        elif user_detail.subscription == "VIP":
            if datetime.today().year == (user_detail.created).today().year:
                if datetime.today().month - 3 >= (user_detail.created).today().month:
                    if datetime.today().day >= (user_detail.created).today().day:
                        close = "yes"
                    else:
                        close = "no"
                else:
                    close = "no"
            else:
                close = "yes"
        elif user_detail.subscription == "VVIP":
            if datetime.today().year == (user_detail.created).today().year:
                if datetime.today().month - 6 >= (user_detail.created).today().month:
                    if datetime.today().day >= (user_detail.created).today().day:
                        close = "yes"
                    else:
                        close = "no"
                else:
                    close = "no"
            else:
                close = "yes"

        else:
            if datetime.today().year == (user_detail.created).today().year:
                if datetime.today().day >= (user_detail.created).today().day:
                    close = "yes"
                else:
                    close = "no"
            else:
                close = "yes"

        if user_detail.subscription == "Free":
            if len(results) == 0:
                may_like_list = may_like[0:2]
            elif len(results) == 1:
                may_like_list = may_like[0:1]
            else:
                may_like_list = []

        elif user_detail.subscription == "Amateur":
            if len(results) == 0:
                may_like_list = may_like[0:4]
            elif len(results) == 1:
                may_like_list = may_like[0:3]
            elif len(results) == 1:
                may_like_list = may_like[0:2]
            elif len(results) == 1:
                may_like_list = may_like[0:1]
            else:
                may_like_list = []

        elif user_detail.subscription == "VIP":
            if len(results) == 0:
                may_like_list = may_like[0:9]
            elif len(results) == 1:
                may_like_list = may_like[0:8]
            elif len(results) == 1:
                may_like_list = may_like[0:7]
            elif len(results) == 1:
                may_like_list = may_like[0:6]
            elif len(results) == 1:
                may_like_list = may_like[0:5]
            elif len(results) == 1:
                may_like_list = may_like[0:4]
            elif len(results) == 1:
                may_like_list = may_like[0:3]
            elif len(results) == 1:
                may_like_list = may_like[0:2]
            elif len(results) == 1:
                may_like_list = may_like[0:1]
            else:
                may_like_list = []

        else:
            may_like_list = []

        name = request.user
        from_details = Profile.objects.get(user=request.user)
        messages = MessageDetail.objects.filter(
            Q(slug__startswith=from_details.slug) | Q(slug__endswith=from_details.slug)).order_by("time")
        final = {}
        images = {}
        msg = {}

        if messages.exists():
            x = ''

            for detail in messages:
                pers = ''
                mg = ''
                slug_main = ''
                new_slug = detail.slug[5:10] + detail.slug[0:5]
                msgs = MessageDetail.objects.filter(
                    Q(slug=detail.slug) | Q(slug=new_slug)).order_by("time")

                for message in msgs:
                    time = message.time
                    if message.From == f'{name}':
                        pers = "You"
                        slug_main = message.slug[5:10]
                    else:
                        pers = message.From
                        slug_main = message.slug[0:5]
                    mg = message.message

                tr = time.date()
                new_time = ''
                if tr == datetime.now().date():
                    new_time = str(time.time())[0:5]
                    time_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
                    if str(time.time())[0:2] in time_list:
                        new_time += " AM"
                    else:
                        new_time += " PM"

                elif str(tr)[0:4] == str(datetime.now().date())[0:4]:
                    if int(str(tr)[8:10]) == (int(str(datetime.now().date())[8:10]) - 1):
                        new_time = "Yesterday"

                else:
                    new_time = time.date()

                msg[slug_main] = [pers, mg, new_time]

                if detail.From == f"{name}":
                    final[detail.To] = [detail.slug, detail.slug[5:10]]
                    person = Profile.objects.get(slug=f"{detail.slug[5:10]}")
                    images[detail.slug[5:10]] = person.Profile_pic


                else:
                    final[detail.From] = [detail.slug, detail.slug[0:5]]
                    person = Profile.objects.get(slug=f"{detail.slug[0:5]}")
                    images[detail.slug[0:5]] = person.Profile_pic

            unread = 0
            for fin in msg:
                if msg[fin][0] == "You":
                    pass
                else:
                    unread += 1

            @register.filter
            def get_item(dict, key):
                return dict.get(key).url

            @register.filter
            def get_msg(dict, key):
                return dict.get(key)[1]

            @register.filter
            def get_person(dict, key):
                return dict.get(key)[0]

            @register.filter
            def get_time(dict, key):
                return dict.get(key)[2]

            @register.filter
            def check(val, key):
                var = key
                return ''

        else:
            @register.filter
            def get_item(dict, key):
                return ''

            @register.filter
            def get_msg(dict, key):
                return ''

            @register.filter
            def get_person(dict, key):
                return ''

            @register.filter
            def get_time(dict, key):
                return ''

            @register.filter
            def check(val, key):
                var = key
                return ''


        values = []
        for val in final.values():
            values.append(val)

        context = {
            'name': slug_user,
            'results': results,
            'profiles': profile__details,
            'may_like': may_like,
            'may_like_list': may_like_list,
            'name_1': name,
            'final': final,
            'close': close,
            'images': images,
            'url': '.url',
            'msg': msg,
            'unread': unread,
            'user_slug': user_detail.slug
        }

        return render(request, 'page.html', context)

    if request.method == "POST":
        if request.FILES:
            Profile.objects.filter(user=request.user).update(Profile_pic=request.FILES['Profile_pic'])

            return redirect('page')

        elif 'phone' in request.POST:
            phone = request.POST.get('phone')
            email = request.POST.get('email')

            if phone == '':
                current = Profile.objects.get(user=request.user)
                phone = current.Phone
            else:
                phone = request.POST.get('phone')

            if email == '':
                current = Profile.objects.get(user=request.user)
                email = current.Email
            else:
                email = request.POST.get('email')

            Profile.objects.filter(user=request.user).update(Email=email, Phone=phone)
            return redirect('page')

        elif 'description' in request.POST:
            desc = request.POST.get('description')

            if desc == '':
                current = Profile.objects.get(user=request.user)
                desc = current.Description
            else:
                desc = request.POST.get('description')

            Profile.objects.filter(user=request.user).update(Description=desc)
            return redirect('page')

        elif 'other_gender' in request.POST:
            other_gender = request.POST.get('other_gender')
            purpose = request.POST.get('purpose')
            age_group = request.POST.get('age_group')
            region = request.POST.get('region')

            qlty = Profile.objects.get(user=request.user)
            if other_gender == '':
                qlty.other.Gender = qlty.other.Gender
            else:
                qlty.other.Gender = other_gender
            if purpose == '':
                qlty.other.Purpose = qlty.other.Purpose
            else:
                qlty.other.Purpose = purpose
            if age_group == '':
                qlty.other.Age_group = qlty.other.Age_group
            else:
                qlty.other.Age_group = age_group
            if region == '':
                qlty.other.Region = qlty.other.Region
            else:
                qlty.other.Region = region

            qlty.other.save()

            return redirect('page')
        elif list(request.POST.keys())[1][0:5] == "check":
            prof = Profile.objects.get(user=request.user)
            if 'check1' in request.POST:
                prof.other.check1 = request.POST.get("check1")
            else:
                prof.other.check1 = ""

            if 'check2' in request.POST:
                prof.other.check2 = request.POST.get("check2")
            else:
                prof.other.check2 = ''

            if 'check3' in request.POST:
                prof.other.check3 = request.POST.get("check3")
            else:
                prof.other.check3 = ''

            if 'check5' in request.POST:
                prof.other.check5 = request.POST.get("check5")
            else:
                prof.other.check5 = ''

            if 'check6' in request.POST:
                prof.other.check6 = request.POST.get("check6")
            else:
                prof.other.check6 = ''

            if 'check7' in request.POST:
                prof.other.check7 = request.POST.get("check7")
            else:
                prof.other.check7 = ''

            if 'check8' in request.POST:
                prof.other.check8 = request.POST.get("check8")
            else:
                prof.other.check8 = ''

            if 'check9' in request.POST:
                prof.other.check9 = request.POST.get("check9")
            else:
                prof.other.check9 = ''

            if 'check10' in request.POST:
                prof.other.check10 = request.POST.get("check10")
            else:
                prof.other.check10 = ''

            if 'check11' in request.POST:
                prof.other.check11 = request.POST.get("check11")
            else:
                prof.other.check11 = ''

            if 'check12' in request.POST:
                prof.other.check12 = request.POST.get("check12")
            else:
                prof.other.check12 = ''

            if 'check13' in request.POST:
                prof.other.check13 = request.POST.get("check13")
            else:
                prof.other.check13 = ''

            if 'check14' in request.POST:
                prof.other.check14 = request.POST.get("check14")
            else:
                prof.other.check14 = ''

            if 'check15' in request.POST:
                prof.other.check15 = request.POST.get("check15")
            else:
                prof.other.check15 = ''

            if 'check16' in request.POST:
                prof.other.check16 = request.POST.get("check16")
            else:
                prof.other.check16 = ''

            if 'check17' in request.POST:
                prof.other.check17 = request.POST.get("check17")
            else:
                prof.other.check17 = ''
            if 'check18' in request.POST:
                prof.other.check18 = request.POST.get("check18")
            else:
                prof.other.check18 = ''

            if 'check19' in request.POST:
                prof.other.check19 = request.POST.get("check19")
            else:
                prof.other.check19 = ''

            if 'check20' in request.POST:
                prof.other.check20 = request.POST.get("check20")
            else:
                prof.other.check20 = ''

            if 'check21' in request.POST:
                prof.other.check21 = request.POST.get("check21")
            else:
                prof.other.check21 = ''

            if 'check22' in request.POST:
                prof.other.check22 = request.POST.get("check22")
            else:
                prof.other.check22 = ''

            if 'check23' in request.POST:
                prof.other.check23 = request.POST.get("check23")
            else:
                prof.other.check23 = ''

            if 'check24' in request.POST:
                prof.other.check24 = request.POST.get("check24")
            else:
                prof.other.check24 = ''

            if 'check25' in request.POST:
                prof.other.check25 = request.POST.get("check25")
            else:
                prof.other.check25 = ''

            prof.other.save()
            return redirect('page')


class MatchDetail(View):
    def get(self, *args, **kwargs):
        slug = kwargs['slug']
        main_person = Profile.objects.filter(user=self.request.user)
        match_person = Profile.objects.filter(slug=slug)
        context = {
            'match_person': match_person,
            'main_person': main_person
        }
        return render(self.request, "match_detail.html", context)


def subscription(request):
    context = {}
    return render(request, 'membership.html', context)


class Payment(View):
    def get(self, *args, **kwargs):
        amount = kwargs['slug']
        det = Profile.objects.get(user=self.request.user)
        context = {'email': det.Email, 'amount': amount}
        return render(self.request, 'payment.html', context)

    def post(self, *args, **kwargs):
        secret_key = 'sk_live_3fb48355e5f79301a460cc414ad9a0dd6f521589'
        url = 'https://api.paystack.co/transaction/initialize'
        req_amount = self.request.POST.get('Amount')
        req_email = self.request.POST.get('Email')
        print(req_email)
        print(req_amount)
        email = req_email
        amount = float(req_amount) * 100

        payload = {
            'amount': f'{amount}',
            'email': f'{email}',
            "callback_url": "http://localhost:8000/redirect/"
        }

        payload_json = json.dumps(payload)

        headers = {
            'Authorization': f'Bearer {secret_key}',
            "Content-Type": "application/json"
        }
        req = requests.post(url, headers=headers, data=payload_json)

        data = json.loads(req.content)
        print(data)
        redirect_link = json.loads(req.content)["data"]["authorization_url"]
        print(redirect_link)
        html = "<!doctype html><html lang='en'><head>  <meta charset='utf-8'>  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'> <title>Redirect</title>  <link rel='canonical' href='https://getbootstrap.com/docs/4.5/examples/sign-in/'>  <!-- Bootstrap core CSS --><!-- CSS only --><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1' crossorigin='anonymous'><style>  .arrage{ margin-top: 250px; } .bd-placeholder-img {    font-size: 1.125rem;    text-anchor: middle;    -webkit-user-select: none;    -moz-user-select: none;    -ms-user-select: none;    user-select: none;  }  @media (min-width: 768px) {    .bd-placeholder-img-lg {      font-size: 3.5rem;    }  }</style><!-- Custom styles for this template --></head><body class='text-center'><div class='arrage'><h1 class='h3 mb-3 font-weight-normal'>Go to pay</h1>" + f"<a class='btn btn-lg btn-primary btn-block' href={redirect_link}>Continue to validate</a></div></body></html>"
        return HttpResponse(html)


class Matches(ListView):
    def get(self, *args, **kwargs):
        user_detail = Profile.objects.get(user=self.request.user)
        slug_user = user_detail.slug
        if user_detail.other.Region == "Any":
            results = Profile.objects.filter(Q(other__Age_group=user_detail.other.Age_group) & Q(Gender=user_detail.other.Gender)).exclude(
                user=self.request.user
            )
        else:
            results = Profile.objects.filter(
                Q(other__Age_group=user_detail.other.Age_group) & Q(Gender=user_detail.other.Gender) & Q(Region=user_detail.other.Region)).exclude(
                user=self.request.user
            )

        if user_detail.subscription == "Free":
            list_person = results[2::]
        elif user_detail.subscription == "Amateur":
            list_person = results[4::]
        elif user_detail == "VIP":
            list_person = results[9::]
        else:
            list_person = []

        context = {
            'name': slug_user,
            'results': results,
            'subscription': list_person
        }
        return render(self.request, "matches.html", context)


def redirect_page(request):
    data = request.GET
    mod_json = (data.dict())
    print(mod_json)

    reference = mod_json["reference"]

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        'Authorization': "Bearer sk_live_3fb48355e5f79301a460cc414ad9a0dd6f521589"
    }

    req = requests.get(url, headers=headers)
    req_data = json.loads(req.content)
    network = req_data["data"]["authorization"]["bank"]
    amount = float(req_data["data"]["amount"]) / 100

    if req_data["data"]["status"] == "success":
        if amount == "10":
            data = Profile.objects.get(user=request.user)
            data.subscription = "Amateur"
            data.save()
        elif amount == "30":
            data = Profile.objects.get(user=request.user)
            data.subscription = "VIP"
            data.save()
        elif amount == "60":
            data = Profile.objects.get(user=request.user)
            data.subscription = "VVIP"
            data.save()
    else:
        messages.success(request, "Payment was unsuccessful")
        return render(request, "payment.html")
    return render(request, 'page.html')


@csrf_exempt
def send(request):
    if request.method == "POST":
        data = request.body
        data_resp = json.loads(data.decode('utf-8'))
        Reciever = data_resp["send_to"]
        message = data_resp["message"]
        time = datetime.now()
        to_details = Profile.objects.get(user__username=Reciever)
        from_details = Profile.objects.get(user=request.user)
        slug2 = from_details.slug + to_details.slug
        client_1 = MessageDetail(
            From=request.user,
            To=Reciever,
            message=message,
            time=time,
            slug=slug2
        )
        client_1.save()

        return JsonResponse({})


def receive(request, slug):
    slug1 = slug[5:10] + slug[0:5]
    current = MessageDetail.objects.filter(Q(slug=slug) | Q(slug=slug1)).order_by("time")
    data_dict = {}
    for val in current:
        data_dict[str(val.time)] = [val.From, val.To, val.time, val.message]

    data = data_dict
    return JsonResponse(data)


class Chat(ListView):
    def get(self, *args, **kwargs):
        name = self.request.user
        from_details = Profile.objects.get(user=self.request.user)
        messages = MessageDetail.objects.filter(Q(slug__startswith=from_details.slug) | Q(slug__endswith=from_details.slug))
        final = {}
        images = {}
        msg = {}

        if messages.exists():
            x = ''

            for detail in messages:
                pers = ''
                mg = ''
                slug_main = ''
                new_slug = detail.slug[5:10] + detail.slug[0:5]
                msgs = MessageDetail.objects.filter(
                    Q(slug=detail.slug) | Q(slug=new_slug))

                for message in msgs:
                    time = message.time
                    if message.From == f'{name}':
                        pers = "You"
                        slug_main = message.slug[5:10]
                    else:
                        pers = message.From
                        slug_main = message.slug[0:5]
                    mg = message.message


                tr = time.date()
                new_time = ''
                if tr == datetime.now().date():
                    new_time = str(time.time())[0:5]

                elif str(tr)[0:4] == str(datetime.now().date())[0:4]:
                    if int(str(tr)[8:10]) == (int(str(datetime.now().date())[8:10]) - 1):
                        new_time = "Yesterday"

                else:
                    new_time = str(tr)

                msg[slug_main] = [pers, mg, new_time]

                if detail.From == f"{name}":
                    final[detail.To] = [detail.slug, detail.slug[5:10]]
                    person = Profile.objects.get(slug=f"{detail.slug[5:10]}")
                    images[detail.slug[5:10]] = person.Profile_pic


                else:
                    final[detail.From] = [detail.slug, detail.slug[0:5]]
                    person = Profile.objects.get(slug=f"{detail.slug[0:5]}")
                    images[detail.slug[0:5]] = person.Profile_pic


            
            @register.filter
            def get_item(dict, key):
                return dict.get(key).url


            @register.filter
            def get_msg(dict, key):
                return dict.get(key)[1]

            @register.filter
            def get_person(dict, key):
                return dict.get(key)[0]

            @register.filter
            def get_time(dict, key):
                return dict.get(key)[2]



            context = {
                'name': name,
                'final': final,
                'images': images,
                'url': '.url',
                'msg': msg
            }
            return render(self.request, "chat.html", context)

        else:
            @register.filter
            def get_item(dict, key):
                return ''

            @register.filter
            def get_msg(dict, key):
                return ''

            @register.filter
            def get_person(dict, key):
                return ''

            @register.filter
            def get_time(dict, key):
                return ''
            return render(self.request, "chat.html")


class ChatListView(TemplateView):
    model = MessageDetail
    template_name = "current_chat.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ChatListView, self).get_context_data(**kwargs)
        slugF = kwargs["slug"]
        mod_slug = slugF[0:10]
        user_slug = slugF[0:5]
        print(slugF[5:10])
        slugL = mod_slug[5:10] + mod_slug[0:5]
        send_reciever = slugF[10::]
        details = Profile.objects.get(slug=slugF[5:10])
        user_detail = Profile.objects.get(user=self.request.user)
        if user_detail.subscription == "Free":
            subs = "Locked"

        elif user_detail.subscription == "Amateur":
            msgs = MessageDetail.objects.filter(Q(slug__startswith=user_detail.slug) | Q(slug__endswith=user_detail.slug))
            if len(msgs) >= 30:
                print("yes")
                subs = "Amateur_lock"
            else:
                subs = "Amateur_open"

        elif user_detail.subscription == "VIP":
            msgs = MessageDetail.objects.filter(Q(slug__startswith=user_detail.slug) | Q(slug__endswith=user_detail.slug))
            if len(msgs) >= 90:
                subs = "VIP_lock"
            else:
                subs = "VIP_open"

        elif user_detail.subscription == "VVIP":
            subs = "Open_always"
        try:
            context['name'] = f"{self.request.user}"
            flter = MessageDetail.objects.filter(Q(slug=mod_slug) | Q(slug=slugL)).order_by("time")
            list_msg = {}
            list_snd = []
            list_message = []
            list_from = []
            for mssag in flter:
                if mssag.From in list_snd:
                    mod = mssag.From + "1"
                    list_snd.append(mod)
                    list_msg[mod] = mssag.message
                else:
                    list_snd.append(mssag.From)
                    list_msg[mssag.From] = mssag.message
                list_message.append(mssag.message)

            for val in list_msg.keys():
                chck = re.search(rf"{self.request.user}", f"{val}")
                if chck:
                    list_from.append(list_msg[val])

            name_from = ''
            for val in flter:
                if val.From == f"{self.request.user}":
                    pass
                else:
                    name_from = val.From
            context['msg_list'] = list_message
            context['msg_from'] = list_from
            context['name_from'] = name_from
            context['slug1'] = mod_slug
            context['pass_slug'] = send_reciever
            context['person'] = details
            context['subs'] = subs
            return context

        except ObjectDoesNotExist:
            crete = Profile.objects.get(user=self.request.user)
            new = Messaging(
                slug=crete.slug,
                user=crete.user,
            )
            new.save()

def about(request):
    return render(request, "about.html")

def community(request):
    return render(request, "community.html")

def profile_setting(request):
    if request.method == "GET":
        detail = Profile.objects.filter(user=request.user)
        context = {'profile': detail}
        return render(request, "profile_setting.html", context)

    if request.method == "POST":
        if request.FILES:
            pic = request.FILES['pic']
            Profile.objects.filter(user=request.user).update(Profile_pic=pic)
        else:
            pass
        email = request.POST.get('email')
        description = request.POST.get('description')
        region = request.POST.get('region')
        occupation = request.POST.get('occupation')
        status = request.POST.get('status')
        birthplace = request.POST.get('birthplace')
        interest_shows = request.POST.get('interest_shows')
        interest_bands = request.POST.get('interest_bands')
        interest_movies = request.POST.get('interest_movies')
        interest_games = request.POST.get('interest_games')
        job_title = request.POST.get('job_title')
        job_started = request.POST.get('job_started')
        job_end = request.POST.get('job_end')
        job_description = request.POST.get('job_description')
        job_title1 = request.POST.get('job_title1')
        job_started1 = request.POST.get('job_started1')
        job_end1 = request.POST.get('job_end1')
        job_description1 = request.POST.get('job_description1')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        body_type = request.POST.get('body_type')
        languages = request.POST.get('languages')
        eye_color = request.POST.get('eye_color')
        hair_color = request.POST.get('hair_color')
        ethnicity = request.POST.get('ethnicity')

        if email is not None:
            Profile.objects.filter(user=request.user).update(Email=email)
        else:
            pass

        if description == "":
            pass
        else:
            Profile.objects.filter(user=request.user).update(Description=description)

        if region is not None:
            Profile.objects.filter(user=request.user).update(Region=region)
        else:
            pass

        if occupation is not None:
            Profile.objects.filter(user=request.user).update(Occupation=occupation)
        else:
            pass

        if status is not None:
            Profile.objects.filter(user=request.user).update(Status=status)
        else:
            pass

        if birthplace is not None:
            Profile.objects.filter(user=request.user).update(Birthplace=birthplace)
        else:
            pass

        if interest_shows == "":
            pass
        else:
            Profile.objects.filter(user=request.user).update(Interest_shows=interest_shows)

        if interest_bands == "":
            pass
        else:
            Profile.objects.filter(user=request.user).update(Interest_bands=interest_bands)

        if interest_games == "":
            pass
        else:
            Profile.objects.filter(user=request.user).update(Interest_games=interest_games)

        if interest_movies == "":
            pass
        else:
            Profile.objects.filter(user=request.user).update(Interest_movies=interest_movies)

        if job_title is not None:
            Profile.objects.filter(user=request.user).update(Jobs_title=job_title)
        else:
            pass

        if job_started is not None:
            Profile.objects.filter(user=request.user).update(Jobs_started=job_started)
        else:
            pass

        if job_end is not None:
            Profile.objects.filter(user=request.user).update(Jobs_end=job_end)
        else:
            pass

        if job_description == "":
            pass
        else:
            Profile.objects.filter(user=request.user).update(Jobs_description=job_description)

        if job_title1 is not None:
            Profile.objects.filter(user=request.user).update(Jobs_title1=job_title1)
        else:
            pass

        if job_started1 is not None:
            Profile.objects.filter(user=request.user).update(Jobs_started1=job_started1)
        else:
            pass

        if job_end1 is not None:
            Profile.objects.filter(user=request.user).update(Jobs_end1=job_end1)
        else:
            pass

        if job_description1 == "":
            pass
        else:
            Profile.objects.filter(user=request.user).update(Jobs_description1=job_description1)

        if height is not None:
            Profile.objects.filter(user=request.user).update(Height=height)

        else:
            pass

        if weight is not None:
            Profile.objects.filter(user=request.user).update(Weight=weight)

        else:
            pass

        if eye_color is not None:
            Profile.objects.filter(user=request.user).update(Eye_color=eye_color)

        else:
            pass

        if hair_color is not None:
            Profile.objects.filter(user=request.user).update(Hair_color=hair_color)

        else:
            pass

        if body_type is not None:
            Profile.objects.filter(user=request.user).update(Body_type=body_type)

        else:
            pass

        if ethnicity is not None:
            Profile.objects.filter(user=request.user).update(Ethnicity=ethnicity)

        else:
            pass

        if languages == "":
            pass
        else:
            Profile.objects.filter(user=request.user).update(language=languages)

        return redirect("setting")

def profile_detail(request):
    detail = Profile.objects.filter(user=request.user)
    context = {'profile': detail}
    return render(request, "profile_detail.html", context)


def account_info(request):
    if request.method == "GET":
        detail = Profile.objects.filter(user=request.user)
        context = {'profile': detail}
        return render(request, "account_info.html", context)

    if request.method == "POST":
        email = request.POST.get('email')
        region = request.POST.get('region')
        occupation = request.POST.get('occupation')
        status = request.POST.get('status')
        birthplace = request.POST.get('birthplace')
        rec_email = request.POST.get('rec_email')
        rec_phone = request.POST.get('rec_phone')
        Sec_1 = request.POST.get('Sec_1')
        Answer_1 = request.POST.get('Answer_1')
        Sec_2 = request.POST.get('Sec_2')
        Answer_2 = request.POST.get('Answer_2')

        if email is not None:
            Profile.objects.filter(user=request.user).update(Email=email)
        else:
            pass

        if region is not None:
            Profile.objects.filter(user=request.user).update(Region=region)
        else:
            pass

        if occupation is not None:
            Profile.objects.filter(user=request.user).update(Occupation=occupation)
        else:
            pass

        if status is not None:
            Profile.objects.filter(user=request.user).update(Status=status)
        else:
            pass

        if birthplace is not None:
            Profile.objects.filter(user=request.user).update(Birthplace=birthplace)
        else:
            pass

        if rec_phone is not None:
            Profile.objects.filter(user=request.user).update(Recovery_phone=rec_phone)
        else:
            pass

        if rec_email is not None:
            Profile.objects.filter(user=request.user).update(Recovery_email=rec_email)
        else:
            pass

        if Sec_1 is not None:
            Profile.objects.filter(user=request.user).update(Question_1=Sec_1)
        else:
            pass

        if Sec_2 is not None:
            Profile.objects.filter(user=request.user).update(Question_2=Sec_2)
        else:
            pass

        if Answer_1 is not None:
            Profile.objects.filter(user=request.user).update(Answer_1=Answer_1)
        else:
            pass

        if Answer_2 is not None:
            Profile.objects.filter(user=request.user).update(Answer_2=Answer_2)
        else:
            pass

        return redirect('account_info')


def pass_change(request):
    if request.method == "POST":
        new_pass1 = request.POST.get('new_pass1')
        new_pass2 = request.POST.get('new_pass2')
        current_pass = request.POST.get('current_pass')
        user = authenticate(request, username=request.user.username, password=current_pass)

        if user is not None:
            if new_pass1 == new_pass2:
                user1 = User.objects.get(username=request.user.username)
                user1.set_password(f'{new_pass1}')
                user1.save()
                new_user = authenticate(username=request.user.username, password=new_pass1)
                login(request,new_user)
            else:
                messages.error(request, "Passwords does not match")
        else:
            messages.error(request, "Incorrect Password")

        return redirect('pass_change')
    return render(request, 'pass_change.html')


def close_account(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = authenticate(request, username=request.user.username, password=password)
        profle = Profile.objects.get(user=request.user)
        qualities = Qualities.objects.get(user=request.user)
        if user is not None:
            user1 = User.objects.get(username=request.user.username)
            profle.delete()
            qualities.delete()
            user1.delete()
            return redirect('home')
        else:
            messages.error(request, "Password Incorrect")
            return redirect('close_account')

    return render(request, "close_account.html")


def status(request):
    if request.method == "GET":
        user = Profile.objects.filter(user=request.user)
        stats = Status.objects.all()
        imgs = StatusImage.objects.all()

        profile__details = Profile.objects.filter(user=request.user)
        user_detail = Profile.objects.get(user=request.user)
        slug_user = user_detail.slug
        unread = 0
        if user_detail.other.Region == "Any":
            if user_detail.other.Age_group == "Any":
                results = Profile.objects.filter(
                    Q(Gender=user_detail.other.Gender)).exclude(
                    user=request.user
                )
            else:
                results = Profile.objects.filter(
                    Q(other__Age_group=user_detail.other.Age_group) & Q(Gender=user_detail.other.Gender)).exclude(
                    user=request.user
                )
        else:
            if user_detail.other.Age_group == "Any":
                results = Profile.objects.filter(
                    Q(Gender=user_detail.other.Gender) & Q(
                        Region=user_detail.other.Region)).exclude(
                    user=request.user
                )
            else:
                results = Profile.objects.filter(
                    Q(other__Age_group=user_detail.other.Age_group) & Q(Gender=user_detail.other.Gender) & Q(
                        Region=user_detail.other.Region)).exclude(
                    user=request.user
                )

        may_like = Profile.objects.filter(
            Q(Gender=user_detail.other.Gender)).exclude(
            user=request.user
        )
        may_like_list = []
        close = ""
        if user_detail.subscription == "Free":
            close = "yes"
        elif user_detail.subscription == "Amateur":
            if datetime.today().year == (user_detail.created).today().year:
                if datetime.today().month - 1 >= (user_detail.created).today().month:
                    if datetime.today().day >= (user_detail.created).today().day:
                        close = "yes"
                    else:
                        close = "no"
                else:
                    close = "no"
            else:
                close = "yes"
        elif user_detail.subscription == "VIP":
            if datetime.today().year == (user_detail.created).today().year:
                if datetime.today().month - 3 >= (user_detail.created).today().month:
                    if datetime.today().day >= (user_detail.created).today().day:
                        close = "yes"
                    else:
                        close = "no"
                else:
                    close = "no"
            else:
                close = "yes"
        elif user_detail.subscription == "VVIP":
            if datetime.today().year == (user_detail.created).today().year:
                if datetime.today().month - 6 >= (user_detail.created).today().month:
                    if datetime.today().day >= (user_detail.created).today().day:
                        close = "yes"
                    else:
                        close = "no"
                else:
                    close = "no"
            else:
                close = "yes"

        else:
            if datetime.today().year == (user_detail.created).today().year:
                if datetime.today().day >= (user_detail.created).today().day:
                    close = "yes"
                else:
                    close = "no"
            else:
                close = "yes"

        if user_detail.subscription == "Free":
            if len(results) == 0:
                may_like_list = may_like[0:2]
            elif len(results) == 1:
                may_like_list = may_like[0:1]
            else:
                may_like_list = []

        elif user_detail.subscription == "Amateur":
            if len(results) == 0:
                may_like_list = may_like[0:4]
            elif len(results) == 1:
                may_like_list = may_like[0:3]
            elif len(results) == 1:
                may_like_list = may_like[0:2]
            elif len(results) == 1:
                may_like_list = may_like[0:1]
            else:
                may_like_list = []

        elif user_detail.subscription == "VIP":
            if len(results) == 0:
                may_like_list = may_like[0:9]
            elif len(results) == 1:
                may_like_list = may_like[0:8]
            elif len(results) == 1:
                may_like_list = may_like[0:7]
            elif len(results) == 1:
                may_like_list = may_like[0:6]
            elif len(results) == 1:
                may_like_list = may_like[0:5]
            elif len(results) == 1:
                may_like_list = may_like[0:4]
            elif len(results) == 1:
                may_like_list = may_like[0:3]
            elif len(results) == 1:
                may_like_list = may_like[0:2]
            elif len(results) == 1:
                may_like_list = may_like[0:1]
            else:
                may_like_list = []

        else:
            may_like_list = []

        name = request.user
        from_details = Profile.objects.get(user=request.user)
        messages = MessageDetail.objects.filter(
            Q(slug__startswith=from_details.slug) | Q(slug__endswith=from_details.slug)).order_by("time")
        final = {}
        images = {}
        msg = {}

        if messages.exists():
            x = ''

            for detail in messages:
                pers = ''
                mg = ''
                slug_main = ''
                new_slug = detail.slug[5:10] + detail.slug[0:5]
                msgs = MessageDetail.objects.filter(
                    Q(slug=detail.slug) | Q(slug=new_slug)).order_by("time")

                for message in msgs:
                    time = message.time
                    if message.From == f'{name}':
                        pers = "You"
                        slug_main = message.slug[5:10]
                    else:
                        pers = message.From
                        slug_main = message.slug[0:5]
                    mg = message.message

                tr = time.date()
                new_time = ''
                if tr == datetime.now().date():
                    new_time = str(time.time())[0:5]
                    time_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
                    if str(time.time())[0:2] in time_list:
                        new_time += " AM"
                    else:
                        new_time += " PM"

                elif str(tr)[0:4] == str(datetime.now().date())[0:4]:
                    if int(str(tr)[8:10]) == (int(str(datetime.now().date())[8:10]) - 1):
                        new_time = "Yesterday"

                else:
                    new_time = time.date()

                msg[slug_main] = [pers, mg, new_time]

                if detail.From == f"{name}":
                    final[detail.To] = [detail.slug, detail.slug[5:10]]
                    person = Profile.objects.get(slug=f"{detail.slug[5:10]}")
                    images[detail.slug[5:10]] = person.Profile_pic


                else:
                    final[detail.From] = [detail.slug, detail.slug[0:5]]
                    person = Profile.objects.get(slug=f"{detail.slug[0:5]}")
                    images[detail.slug[0:5]] = person.Profile_pic

            unread = 0
            for fin in msg:
                if msg[fin][0] == "You":
                    pass
                else:
                    unread += 1

            @register.filter
            def get_item(dict, key):
                return dict.get(key).url

            @register.filter
            def get_msg(dict, key):
                return dict.get(key)[1]

            @register.filter
            def get_person(dict, key):
                return dict.get(key)[0]

            @register.filter
            def get_time(dict, key):
                return dict.get(key)[2]

            @register.filter
            def check(val, key):
                var = key
                return ''

        else:
            @register.filter
            def get_item(dict, key):
                return ''

            @register.filter
            def get_msg(dict, key):
                return ''

            @register.filter
            def get_person(dict, key):
                return ''

            @register.filter
            def get_time(dict, key):
                return ''

            @register.filter
            def check(val, key):
                var = key
                return ''

        values = []
        for val in final.values():
            values.append(val)

        context = {
            'name': slug_user,
            'results': results,
            'profiles': profile__details,
            'may_like': may_like,
            'may_like_list': may_like_list,
            'name_1': name,
            'final': final,
            'images': images,
            'close': close,
            'msg': msg,
            'unread': unread,
            'user_slug': user_detail.slug,
            'user_main': user,
            'stats': stats,
            'imgs': imgs
        }

        return render(request, 'status.html', context)

    if request.method == "POST":
        r = random.SystemRandom()
        numbers = r.randint(0000000000, 9999999999)
        letters = r.sample(string.ascii_lowercase, 7)
        slug = str(numbers) + ''.join(letters)
        if request.FILES:
            status = request.POST.get("status")
            time = datetime.today()
            user = request.user.username
            user_profile = Profile.objects.get(user=request.user)
            new_stats = Status(
                user=user,
                time=time,
                status=status,
                slug=slug,
                name=user_profile.First_name + " " + user_profile.Last_name,
                image=user_profile.Profile_pic
            )
            new_stats.save()

            for img in request.FILES.getlist("image_files"):
                pers_stats = Status.objects.get(slug=slug)
                pic = StatusImage(
                    image=img
                )
                pic.save()
                pers_stats.stats.add(pic)
                pers_stats.save()

            return redirect('status')

        else:
            status = request.POST.get("status")
            time = datetime.today()
            user = request.user.username
            user_profile = Profile.objects.get(user=request.user)
            new_stats = Status(
                user=user,
                time=time,
                status=status,
                slug=slug,
                image=user_profile.Profile_pic,
                name=user_profile.First + " " + user_profile.Last_name,
            )
            new_stats.save()
            return redirect('status')

    return render(request, "status.html")


def forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        profile = Profile.objects.filter(Email=email)
        r = SystemRandom()
        number = r.randint(00000, 99999)
        if profile.exists():
            send_mail(
                'Change Password - Dreamnmatch.com',
                f'Your reset code from Dreamnmatch.com for your password change is {number}',
                'phaisalsey6@gmail.com',
                [f'{email}'],
                fail_silently=False
            )
            return redirect('forget_password')
        else:
            messages.info(request, "Email is incorrect")
            return redirect('forget_password')

    return render(request, "accounts/forget_password.html")