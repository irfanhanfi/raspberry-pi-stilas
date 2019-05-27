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
        
def update_hdmi_setting(bcPath, lcPath, pdsPath, rfPath):
    with open(bcPath, 'r') as f:
        config_string = '[dummy_section]\n' + f.read()
    oldConfig = configparser.ConfigParser()
    oldConfig.read_string(config_string)

    newConfig = configparser.RawConfigParser()   
    newConfig.read(lcPath)
    new_values = newConfig.items('hdmi_config')

    valuesChanged = False
    for attr, new_value in new_values:
        old_value = ""
        has_option = oldConfig.has_option('dummy_section', attr)
        if has_option == True:
            old_value = oldConfig.get('dummy_section', attr)
        if old_value != new_value:
            if not valuesChanged:
                shutil.copy(bcPath, pdsPath + "/backup/"+ os.path.splitext(os.path.basename(bcPath))[0] + "-" + time.strftime("%Y%m%d%H%M%S") +".txt")
                valuesChanged = True
            subprocess.Popen(["/bin/sh", rfPath + "/set_boot_config.sh", attr, new_value])
            time.sleep(.2)
    return valuesChanged
        
#Folder name
folderName       = "stilas"
# Root folder path os.getcwd()
rootFolderPath   = sys.argv[2] + "/stilas"
# Pendrive path
pendrivePath     = sys.argv[1]
# PD Stilas Folder
pdStilasFolder = pendrivePath + "/" + folderName

bootConfigFilePath= "/boot/config.txt"
localConfigFilePath=pdStilasFolder + "/stilas_config.ini"

#~ # Check root RPI stilas folder is present or not on PD if not hen create 
if not os.path.isdir(pdStilasFolder):
    try:
        original_umask = os.umask(0)
        os.makedirs(pdStilasFolder)
    finally:
        os.umask(original_umask)

# Check stilas_readme.txt file is present or not on PD if not hen create 
if not os.path.isfile(pdStilasFolder + "/stilas_readme.txt"): 
    shutil.copy(rootFolderPath+"/stilas_readme.txt", pdStilasFolder + "/stilas_readme.txt")

# Check stilas_config.ini file is present or not on PD if not hen create 
if not os.path.isfile(localConfigFilePath): 
    shutil.copy(rootFolderPath+"/stilas_config.ini", localConfigFilePath)
else:
    if not os.path.isdir(pdStilasFolder + '/backup'):
        try:
            original_umask = os.umask(0)
            os.makedirs(pdStilasFolder + '/backup')
        finally:
            os.umask(original_umask)
    shouldReboot=update_hdmi_setting(bootConfigFilePath, localConfigFilePath, pdStilasFolder, rootFolderPath)
    if (shouldReboot):
        print('restart')
        subprocess.Popen(["/bin/sh", "reboot", "-r", "now"])
        exit(); 
        
# Check root RPI stilas folder is present or not on PD if not hen create 
if not os.path.isdir(pdStilasFolder + "/archived"):
    os.mkdir(pdStilasFolder + "/archived")

# Check root RPI stilas folder is present or not on PD if not hen create 
if not os.path.isdir(pdStilasFolder + "/live"):
    os.mkdir(pdStilasFolder + "/live")
    
configParser = configparser.RawConfigParser()   
configParser.read(pdStilasFolder + "/stilas_config.ini")
useTimerUrl  = configParser.get('stilas_config', 'USE_TIMER_URL')
timerUrl     = configParser.get('stilas_config', 'TIMER_URL')
ssidName     = configParser.get('stilas_config', 'WIFI_SSID_NAME')
ssidPsk      = configParser.get('stilas_config', 'WIFI_SSID_PSK')
if ssidName and ssidPsk and have_internet() == False:
    subprocess.Popen(["/bin/sh", rootFolderPath + "/wifi-connect.sh", ssidName, ssidPsk])

allFiles = glob.glob(pdStilasFolder + "/*.zip")

if useTimerUrl=="yes" and timerUrl:
    defaultUrl = timerUrl
elif allFiles:
    # Get all zip file form stials
    latestFile = max(allFiles, key=os.path.getctime)

    # Get the latest modified zip file
    latestFileIndex = allFiles.index(latestFile)

    # Unzip latest zip file into live folder
    with zipfile.ZipFile(latestFile) as zf:
        zf.extractall(pdStilasFolder + "/live")

    # Check viewer.html file is present in live folder or not 
    if os.path.isfile(pdStilasFolder + "/live/viewer.html"): 
        defaultUrl=pdStilasFolder + "/live/viewer.html"

        # Opne the viewer.html file in browser with full screen
        #subprocess.Popen(["chromium-browser","--start-fullscreen",url,])

    del allFiles[latestFileIndex]

    for file in allFiles:
        target = pdStilasFolder +"/archived/"+os.path.basename(file)+"-"+time.strftime("%Y%m%d-%H%M%S")+".zip"
        shutil.move(file, target)
else:
    # Check stilas.jpg file is present or not on PD if not hen create 
    if os.path.isfile(pdStilasFolder + "/stilas.jpg"): 
        # Override the stilas.jpg file from RPI to pendrive
        shutil.copy(pdStilasFolder + "/stilas.jpg", rootFolderPath+"/stilas.jpg")
    defaultUrl = rootFolderPath+"/stilas.jpg"

print(defaultUrl)

subprocess.Popen(["pkill", "-o", "chromium"])
subprocess.Popen(["sudo", "-u", "pi", "chromium-browser", "--start-fullscreen", defaultUrl])#, "--disable-gpu", "--disable-software-rasterizer"

