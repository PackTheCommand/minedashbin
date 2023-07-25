import hashlib
import json
import os
from getpass import getpass
from sys import argv
import bcrypt
from pymsgbox import password


def getcreadentials():

    if os.path.exists("mpix.credentials")&(not( "--fci"in argv)):

        with open("mpix.credentials") as f:

            try:
                j = json.load(f)
                return j["username"],j["paskey"]
            except KeyError:
                pass
            except json.decoder.JSONDecodeError:
                print("error in credentials file")
                pass
    username = input("Username: ")
    paskey = hashpas(getpass("Password: "))
    print("Credentials saved Successfully in 'mpix.credentials'")
    with open("mpix.credentials","w") as f:
        f.write(json.dumps({"username":username,"paskey":paskey}))

    return username, paskey


templade={"type":"extension","script?":False,"name":"test"}
from zipfile import ZipFile

def unzip(path,uid):


    # loading the temp.zip and creating a zip object
    with ZipFile(path, 'r') as zObject:
        if templade["type"]=="extension":

            for file in zObject.namelist():
                if file.startswith(uid+'/'):
                    zObject.extract(file, "extentions\\")

        elif templade["type"]=="module":


            for file in zObject.namelist():
                if file.startswith(uid+'/'):
                    zObject.extract(file, path="templades\\modules\\")


        else:
            print("moduletype",templade["type"],"not supported")
def registerIndex(type,version,uid,name,mc_target):

    with open("mpix.packages.index") as f:
        index=json.load(f)
        if type in index:
            index[type].append({"version":version,"uid":uid,"name":name,"mc-target":mc_target})
        f.close()
        print(index)
    with open("mpix.packages.index","w") as fs:
        json.dump(index,fs)
    print("reisterred")

def hashpas(password):
    hash=hashlib.sha256(password.encode("utf-8"))
    return hash.hexdigest()
def getinfo(path):
    global templade
    with ZipFile(path, 'r') as zObject:

        templade=json.loads(zObject.read(".install").decode("UTF-8"))
def delete_all_files_in_directory(directory_path):
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files in the directory have been deleted.")
    except OSError as e:
        print(f"Error occurred: {e}")
def Uninstall(uid):
    with open("mpix.packages.index") as f:
        index=json.load(f)
        for n,i in enumerate([]+index["module"]):
            if i["uid"]==uid:
                index["module"].pop(n)
                try:
                    delete_all_files_in_directory("templades\\modules\\"+uid)

                    os.remove("templades\\modules\\"+uid)
                except FileNotFoundError:
                    pass
                except PermissionError:
                    print("Access error: Please try again with administrator privileges")
                    exit(0)

                print("uninstalled successfully")
                with open("mpix.packages.index", "w") as fs:
                    json.dump(index, fs)
                return

        for n2,i in enumerate([]+index["extension"]):
            if i["uid"]==uid:
                index["extension"].pop(n2)
                delete_all_files_in_directory("extensions\\"+uid)

                os.remove("extensions\\"+uid)
                print("uninstalled successfully")
                with open("mpix.packages.index", "w") as fs:
                    json.dump(index, fs)
                return

        print("module or extension not found [uninstall failed]")






    with open("mpix.packages.index","w") as fs:
        json.dump(index,fs)


def do(path,uid):
    getinfo(path)
    registerIndex(templade["type"],templade["metadata"]["version"],uid,templade["name"],templade["metadata"]["mc-target"])
    unzip(path,uid)



protocol="http:"
adress=protocol+"//127.0.0.1:8078/"
username="test"
pasword="test1"


import requests
#argv=["","signup"]
#argv=["","cp","pythonic2"]
#argv=["","upload","pythonic2","modulefile/module.zip"]
#argv=["","install","pythonic2"]
#argv=["","uninstall","pythonic2"]

avg_len=len(argv)
if argv[1] == "install":
    if not("-local" in argv)&(avg_len>2):

        r=requests.get(adress+f"getpack?project="+argv[2])
        with open("temp/module.zipx", "wb") as f:
            f.write(r.content)
        print("downloaded successfully")
        do("temp/module.zipx",argv[2])
        os.rmdir("temp/module.zipx")
    elif avg_len>2:
        do(argv[2],argv[2])
elif (argv[1] == "uninstall")&(avg_len>2):
    Uninstall(argv[2])


elif (argv[1] == "cp")&(avg_len>2):
    username,paskey=getcreadentials()

    r=requests.get(adress+f"create-project?author={username}&paskey={paskey}&project="+argv[2])
    print(r.text)
elif (argv[1] == "signup")&(avg_len>1):

    print("Account creation started")
    username,paskey=getcreadentials()
    print("send:", paskey)
    paskey2 = hashpas(getpass("Password-again: "))
    if paskey != paskey2:
        print("Passwords don't match",paskey,paskey2)
        exit(1)
    r = requests.get(adress + f"/api-signup?username={username}&paskey={paskey}")
    print(r.text)


elif (argv[1] == "upload")&(avg_len>3):
    username,password=getcreadentials()
    with open(argv[3],"rb") as f:
        """form_data = {
                    "author": "test_author",
                    "project": "test_project",
                    "paskey": "test_paskey",
                }

                # Send the POST request with file upload

                files = {'file': f}
                response = requests.post(adress + f"upload", files=files, data=form_data)"""

        r=requests.post(adress + f"upload?author={username}&paskey={password}&project="+argv[2],files={"upload_file":f} ,timeout=5)

        print(r.text)

