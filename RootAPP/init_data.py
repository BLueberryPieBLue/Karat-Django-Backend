from webshell.models import *
from UserAPP.models import *
from django.contrib.auth.models import User as AUser
def init_webshell_scripts():
    if Script.objects.count() == 0:
        Script.objects.create(id="1",name="CMD",source="""import os\n\n\ncmd="help"\n\n\nfor i in os.popen(cmd):\n\tprint(i)\n""")
        Script.objects.create(id="2", name="Python", source="""print("HelloWord!")\n""")
    else:
        print('-->webshell_script exists. Skiped.')

def init_UserAPP_User():
    if User.objects.count() == 0:
        User.objects.create(id="0",username="Root",password="pbkdf2_sha256$120000$1Iee3dAEmCCO$fzhkT3no3IBzNOWMhbncbsyhrhNz1RmAzZkE1fRalgc=",Email="Root@Karat.com",verficationCode="pbkdf2_sha256$120000$1Iee3dAEmCCO$fzhkT3no3IBzNOWMhbncbsyhrhNz1RmAzZkE1fRalgc=",time1="0",time2="0",registState="1",errortimes="0",registtime="0",isroot="1")
    else:
        print('-->User exists. Skiped.')

def init_Auth_User():
    if AUser.objects.count() == 0:
        AUser.objects.create(id="0",password="pbkdf2_sha256$120000$Ra4Aw9UGaKN7$E/JGOzPhIaYKWas1sa8sPDb4hAxvMGiiPkIKbdTtrOE=",is_superuser=True,username="root",email='Root@karat.com',is_staff=True,is_active=True)
    else:
        print('-->User exists. Skiped.')

def init_datas():
    print('Initializing the data...')
    init_webshell_scripts()
    init_UserAPP_User()
    init_Auth_User()
    print('-->Done.')
