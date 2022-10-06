import json
import datetime
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from wishlist.models import BarangWishlist
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
        'list_barang': data_barang_wishlist,
        'nama': 'Gabriel Edgar Firdausyah Nugroho', 
        'last_login': request.COOKIES['last_login'],
        
    }
    return render(request, "wishlist.html", context)

@login_required(login_url='/wishlist/login/')
def show_ajax(request):
    data = BarangWishlist.objects.all()
    context = {
        'list_barang' : data,
        'last_login': request.COOKIES['last_login'],
        
    }
    return render(request, "wishlist_ajax.html", context)

def submit(request):
    if request.method == 'POST':
        nama_barang = request.POST['nama_barang']
        deskripsi = request.POST['deskripsi']
        harga_barang = request.POST['harga_barang']
        wishlist_instance = BarangWishlist(nama_barang=nama_barang, deskripsi=deskripsi, harga_barang=harga_barang)
        wishlist_instance.save()
        data = {
            "message": 'Successfully submitted'
        }
        json_object = json.dumps(data, indent = 4) 

        return JsonResponse(json.loads(json_object))
    
    return render(request, 'submit_wishlist.html')

def show_xml(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('wishlist:login')