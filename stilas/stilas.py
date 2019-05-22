import webbrowser, os, sys, shutil, glob, time, zipfile, subprocess, configparser
# import shutil
# import glob
# import time
# import zipfile

try:
    import httplib
except:
    import http.client as httplib

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False
        
print(have_internet())
exit;
#Folder name
folderName="stilas"

# Root folder path os.getcwd()
rootFolderPath = sys.argv[2] + "/stilas"

# Pendrive path
pendrivePath=sys.argv[1]

#~ # Check root RPI stilas folder is present or not on PD if not hen create 
if not os.path.isdir(pendrivePath+"/"+folderName):
    try:
        original_umask = os.umask(0)
        os.makedirs(pendrivePath+"/"+folderName)
    finally:
        os.umask(original_umask)

print(os.path.isfile(pendrivePath+"/"+folderName+"/stilas_readme.txt"))

# Check stilas_readme.txt file is present or not on PD if not hen create 
if not os.path.isfile(pendrivePath+"/"+folderName+"/stilas_readme.txt"): 
    shutil.copy(rootFolderPath+"/stilas_readme.txt", pendrivePath+"/"+folderName+"/stilas_readme.txt")

# Check stilas_config.ini file is present or not on PD if not hen create 
if not os.path.isfile(pendrivePath+"/"+folderName+"/stilas_config.ini"): 
    shutil.copy(rootFolderPath+"/stilas_config.ini", pendrivePath+"/"+folderName+"/stilas_config.ini")

configParser = configparser.RawConfigParser()   
#configFilePath = r'c:\abc.txt'
configParser.read(pendrivePath+"/"+folderName+"/stilas_config.ini")
useTimerUrl = configParser.get('stilas_config', 'USE_TIMER_URL')
timerUrl = configParser.get('stilas_config', 'TIMER_URL')
ssidName = configParser.get('stilas_config', 'WIFI_SSID_NAME')
ssidPsk = configParser.get('stilas_config', 'WIFI_SSID_PSK')
if ssidName and ssidPsk and have_internet() == False:
    subprocess.Popen(["/bin/sh", rootFolderPath + "/wifi-connect.sh", ssidName, ssidPsk])

# Check root RPI stilas folder is present or not on PD if not hen create 
if not os.path.isdir(pendrivePath+"/"+folderName+"/archived"):
    os.mkdir(pendrivePath+"/"+folderName+"/archived")

# Check root RPI stilas folder is present or not on PD if not hen create 
if not os.path.isdir(pendrivePath+"/"+folderName+"/live"):
    os.mkdir(pendrivePath+"/"+folderName+"/live")

allFiles = glob.glob(pendrivePath+"/"+folderName+"/*.zip")
print(useTimerUrl)
print(timerUrl)
if useTimerUrl=="yes" and timerUrl:
    defaultUrl = timerUrl
elif allFiles:
    # When zip file found

    # Get all zip file form stials
    latestFile = max(allFiles, key=os.path.getctime)

    # Get the latest modified zip file
    latestFileIndex = allFiles.index(latestFile)

    # Unzip latest zip file into live folder
    with zipfile.ZipFile(latestFile) as zf:
        zf.extractall(pendrivePath+"/"+folderName+"/live")

    # Check viewer.html file is present in live folder or not 
    if os.path.isfile(pendrivePath+"/"+folderName+"/live/viewer.html"): 
        defaultUrl=pendrivePath+"/"+folderName+"/live/viewer.html"

        # Opne the viewer.html file in browser with full screen
        #subprocess.Popen(["chromium-browser","--start-fullscreen",url,])

    del allFiles[latestFileIndex]

    for file in allFiles:
        target = pendrivePath+"/"+folderName+"/archived/"+os.path.basename(file)+"-"+time.strftime("%Y%m%d-%H%M%S")+".zip"
        shutil.move(file, target)
else:
    # Check stilas.jpg file is present or not on PD if not hen create 
    if os.path.isfile(pendrivePath+"/"+folderName+"/stilas.jpg"): 
        # Override the stilas.jpg file from RPI to pendrive
        shutil.copy(pendrivePath+"/"+folderName+"/stilas.jpg", rootFolderPath+"/stilas.jpg")

    # Opne the viewer.html file in browser with full screen
    # defaultImageUrl = pendrivePath+"/"+folderName+"/stilas.jpg"
    defaultUrl = rootFolderPath+"/stilas.jpg"
print(defaultUrl)

subprocess.Popen(["pkill", "-o", "chromium"])
subprocess.Popen(["sudo", "-u", "pi", "chromium-browser", "--start-fullscreen", defaultUrl])#, "--disable-gpu", "--disable-software-rasterizer"
# print("zip file not found")
