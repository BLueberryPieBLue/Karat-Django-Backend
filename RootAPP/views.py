import json
import os
import zipfile
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from RootAPP.models import PathItem, FileItem
from UserAPP.models import User
#####################################################################################################################################
pwd="pbkdf2_sha256$120000$nyq1h3VaCf8A$OSlCRiR1x9xWVnSAENlDpyov8hI9B98wSCZ4vVCpKH0="
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rooturl=os.path.join(BASE_DIR, 'RootAPP/static/Root/')
prturl=os.path.join(BASE_DIR, 'RootAPP/static/Root/Prt/')
tempurl=os.path.join(BASE_DIR, 'RootAPP/static/Root/Temp/')
def Code(request):
    try:
        id = request.session.get("id")
        if id != None:
            per = User.objects.get(id=id)
            if per.isroot == '1':
                a=request.GET.get("a")
                b=request.GET.get("b")
                response = HttpResponse(json.dumps({"code": "1","pwd":make_password(a),"flag":check_password(a,b)}))
            else:
                response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
        else:
            response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    except Exception as e:
        print(e)
        response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def LoginRoot(request):
    try:
        id = request.session.get("id")
        if id != None:
            per = User.objects.get(id=id)
            if per.isroot=='1':
                a = request.GET.get("a")
                b = request.GET.get("b")
                if check_password(a,b):
                    request.session['root'] = pwd
                    response = HttpResponse(json.dumps({"code": "1"}))
            else:
                response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
        else:
            response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    except Exception as e:
        print(e)
        response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
def LogoutRoot(request):
    try:
        del request.session["root"]
        response = HttpResponse(json.dumps({"code": "1"}))
    except Exception as e:
        print(e)
        response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

#####################################################################################################################################

def DelDir(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

def Prt(request):
    try:
        id = request.session.get("id")
        root = request.session.get("root")
        if id != None and root!=None:
            per = User.objects.get(id=id)
            if per.isroot=='1'and root==pwd:
                import time
                from PIL import ImageGrab
                try:
                    os.makedirs(prturl)
                except:
                    pass
                time=time.time()
                url=prturl+str(time)+'.jpg'
                ImageGrab.grab().save(url)
                response = HttpResponse("<img src='/static/Root/Prt/"+str(time)+".jpg'/>")
            else:
                response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
        else:
            response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    except Exception as e:
        print(e)
        response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def Del(request):
    try:
        id = request.session.get("id")
        root = request.session.get("root")
        if id != None and root != None:
            per = User.objects.get(id=id)
            if per.isroot == '1' and root == pwd:
                path=rooturl
                DelDir(path)
                response = HttpResponse("OK")
            else:
                response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
        else:
            response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    except Exception as e:
        print(e)
        response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
#####################################################################################################################################################
def CMD(request):
    try:
        id = request.session.get("id")
        root = request.session.get("root")
        if id != None and root != None:
            per = User.objects.get(id=id)
            if per.isroot == '1' and root == pwd:
                cmd=request.GET.get("cmd")
                result = os.popen(cmd)
                response = HttpResponse(result)
            else:
                response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
        else:
            response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    except Exception as e:
        print(e)
        response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
#################################################################################################################################################
def FTP(request, url):
    try:
        id = request.session.get("id")
        root = request.session.get("root")
        if id != None and root != None:
            per = User.objects.get(id=id)
            if per.isroot == '1' and root == pwd:
                current = url
                context_dic = {}
                context_dic['current'] = current
                ps = os.listdir(current)
                path = []
                file = []
                for n in ps:
                    v = os.path.join(current, n)
                    if os.path.isdir(v):
                        p = PathItem(n, current)
                        path.append(p)
                    else:
                        f = FileItem(n, current)
                        file.append(f)
                context_dic['path'] = path
                context_dic['file'] = file
                return render(request, 'FTP.html', context_dic)
            else:
                response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
        else:
            response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    except Exception as e:
        print(e)
        response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
#################################################################################################################################################
def FTPDownload(request, url):
    try:
        id = request.session.get("id")
        root = request.session.get("root")
        if id != None and root != None:
            per = User.objects.get(id=id)
            if per.isroot == '1' and root == pwd:
                filepath = url
                file = open(filepath, 'rb')
                response = FileResponse(file)
                response['Content-Type'] = 'application/octet-stream'
            else:
                response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
        else:
            response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    except Exception as e:
        print(e)
        response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
#################################################################################################################################################
def dfs_get_zip_file(input_path,result):
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path+'/'+file):
            dfs_get_zip_file(input_path+'/'+file,result)
        result.append(input_path+'/'+file)

def zip_path(input_path,output_path,output_name):
    f = zipfile.ZipFile(output_path+'/'+output_name,'w',zipfile.ZIP_DEFLATED)
    filelists = []
    dfs_get_zip_file(input_path,filelists)
    for file in filelists:
        f.write(file)
    f.close()
    return output_path+r"/"+output_name

def FTPDownloadDir(request, url):
    try:
        id = request.session.get("id")
        root = request.session.get("root")
        if id != None and root != None:
            per = User.objects.get(id=id)
            if per.isroot == '1' and root == pwd:
                import time
                time = time.time()
                try:
                    os.makedirs(tempurl)
                except:
                    pass
                zip_path(url, tempurl, str(time)+'.zip')
                filepath = os.path.join(tempurl,str(time)+'.zip')
                file = open(filepath, 'rb')
                response = FileResponse(file)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="Download.zip"'
            else:
                response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
        else:
            response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    except Exception as e:
        print(e)
        response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def Upload(request,url):
    try:
        id = request.session.get("id")
        if id != None:
            per = User.objects.get(id=id)
            if per.isroot == '1':
                if request.method == "POST":
                    myFile = request.FILES.get("myfile", None)
                    if not myFile:
                        response = HttpResponse("no files for upload!")
                    else:
                        destination = open(os.path.join(url, myFile.name), 'wb+')
                        for chunk in myFile.chunks():
                            destination.write(chunk)
                        destination.close()
                        response = response = HttpResponse("upload over!")
                else:
                    response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>", status=404)
            else:
                response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
        else:
            response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    except Exception as e:
        print(e)
        response = HttpResponse("<h1>Not Found</h1><p>The requested resource was not found on this server.</p>",status=404)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

