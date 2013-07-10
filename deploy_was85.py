#Automated Websphere deployment script

#!/usr/bin/eAnv python
import xml.etree.ElementTree as ET
import os
import time
import re
import zipfile
import logging
import sys


##########################################
# Websphere 8.5 install automation script
#
# Packages required for this script:
# 1)InstalMgr1.5.2_LNX_X86_WAS_8.5
# 2)disk1
# 3)disk2
# 4)disk3
# 5)response_file.xml
#
# Author: Phil Horrocks v 0.1
##########################################

filename = "/tmp/response_file.xml"


class installWAS():
    
    
    def __init__(self):
        
        self.defaultPath = '/apps/WebSphere/AppServer'
        self.response = '/tmp/response_file.xml'
    
    
    
    def createResponse(self):
        
        #Global Variables
        global newLoc
        global curLoc
        global locQ
         
        try:
            
            print "INFO: Loading the response XML file "

            
            #Parse the xml file
            tree = ET.parse(filename)
        
            root = tree.getroot()
        
            #get WAS install location
            for i in root.findall('profile'):
                
                                #set the current location
                                
                                curLoc = str(i.attrib).replace("'id': 'IBM WebSphere Application Server V8.5'", "").replace("'", "").replace("{", "").replace('}','').replace('installLocation:','').replace(',','')
                                
                                print "INFO: The current WAS 8.5 install location is:" + curLoc
                                                                                          
                                
                                locQ = raw_input("Do you wish to change the installation location: (y/n)")
                                
                                
                                if locQ == "y":
                                        
                                    newLoc = raw_input("Please enter yout new installation location: ")
                                
                                    #Take the new install location and update the repsonse xml file
                                    i.set("installLocation", newLoc)
                                    tree.write("/tmp/response_file.xml")
                                    print "INFO: The response file has been created "
                                 
                                    return newLoc
                                
                                else:
                                    
                                    print "INFO: No changes were made to the response file"
        except Exception:
            
            print "FAIL: Cound not find/open response file" 
  
        
 
 
    def checkDiskSpace(self):
        
        
        if locQ == "y":
        
            if os.path.exists(newLoc):
 
                s = os.statvfs(newLoc)
          
                size = s.f_bsize * s.f_bavail / 1024
          
                print "INFO: Free MB available on disk " + str(size)
                                
          
                if size > 1000000 :
                
                    print "INFO: You have 10GB or greater to install Websphere binaries"
                
                else:

                    print "FAIL: You need 10GB or greater to install Websphere binaries"   
        
            else:
                
                if os.path.exists(curLoc):
                    
                    s = os.statvfs(curLoc)
          
                    size = s.f_bsize * s.f_bavail / 1024
          
                    print "INFO: Free MB available on disk " + str(size)
                                
          
                    if size > 1000000 :
                
                        print "INFO: You have 10GB or greater to install Websphere binaries"
                
                    else:

                        print "FAIL: You need 10GB or greater to install Websphere binaries"   
                
                
                        sys.exit(0)
    
    
 
    def  installWASBinaries(self):
        
        global profile
        
            
        print "INFO: Preparing to install the binaries"
        print "INFO: Unpacking the installation manager"
        
        #Check if the zip files exist
        
        try:

            if os.path.isfile('InstalMgr1.5.2_LNX_X86_WAS_8.5.zip' | 'WAS_ND_V8.5_1_OF_1.zip' | 'WAS_ND_V8.5_1_OF_2.zip' | 'WAS_ND_V8.5_1_OF_3.zip' ):
                
                print "INFO: Checking if Websphere biniaries exist"
                
                while true:
                    
                        try:
                            
                            print "INFO: Uncompressing Websphere 8.5 packages ready for install"
                            
                            zip1 = zipfile.ZipFile('InstalMgr1.5.2_LNX_X86_WAS_8.5.zip')
                            zip2 = zipfile.ZipFile('WAS_ND_V8.5_1_OF_1.zip')
                            zip3 = zipfile.ZipFile('WAS_ND_V8.5_1_OF_2.zip')
                            zip4 = zipfile.ZipFile('WAS_ND_V8.5_1_OF_3.zip')
                            
                            print(dirs_in_zip(zip1))
                            print(dirs_in_zip(zip2))
                            print(dirs_in_zip(zip3))
                            print(dirs_in_zip(zip4))
                            
                            print "INFO: Successfully uncompressed the Websphere binaries"
                            
                                                       
                        except Exception:
                            
                            print "FAIL: Cannot uncompress the zip files... please check they are not corrupt"
                
                
                
                
        except Exception:
            
            print "FAIL: Cannot find Websphere binaries"
            print "FAIL: Please make sure you have the following packages in the root directory"
            print "**********REQUIRED PACKAGES FOR THIS INSTALLATION*************"
            print "InstalMgr1.5.2_LNX_X86_WAS_8,5.zip"
            print "WAS_ND_V8.5_1_OF_1"
            print "WAS_ND_V8.5_1_OF_2"
            print "WAS_ND_V8.5_1_OF_3"
        
        
        
        def createWASBinaries(self):
            print "INFO: Installing Websphere binaries" 
            print "INFO: Finding IM install directory"
            
            
            try:
                
                if os.path.exists('IM'):
                    
                    print "INFO ....the directory IM exists"
                
                    #Install the  Installation Manager
                    
                    try:

                        os.sysyem('./installc -acceptLicense')
                    
                        print "INFO: Installing IM"
                    
                        #Change to the IM directory and install the WAS binaries
                    
                        os.system('/opt/IBM/InstallationManager/eclipse/tools/imcl -acceptLicense -input response_file.xml')
                    
                    except Exception:
                    
                        print "FAIL: Error installinng IM"
                
            except Exception:
                
                
                print "FAIL: Could not find the IM path for installtion"
            
        
        
        
        
        def checkWASBinaryInstallation(self):
            
            print "Checking the Websphere 8.5 install binaries"
            
            
            output = os.popen(newLoc + '/bin/versionInfo.sh', 'r')
                
            while True:
                    
                    line = output.readlines()
                    
                    for i in line:
                        
                        newLine = ''.join(i.split())
                        
                        #check for Websphere version in the versionInfo output
                        result = re.match('Version8.5.0.0', newLine)
                        
                        if result:
                            
                            print 'INFO: Found ' + i.strip()
                            sys.exit(0)
                            
                        else:
                            
                            pass  
        
        
                
        def createDmgrProfile(self):
            print "INFO: Dmgr setup Tool"
        
            profile = raw_input("Is this a Deployment Manager profile installation? (y/n):")
    
            if profile == "y":
            
                print "This will install a Websphere Deployment Manager profile"
        
                #createDmgrProfile()
                 
                profileName = raw_input("What is the Deployment Manager profile name? eg Dmgr :")
                 
                nodeName = raw_input("What is the nodename for this profile? eg lonsl11001457Manager :")
                
                cellName = raw_input("What is the cell name for this profile? eg cifiCell01 :")
                
                hostName = raw_input ("What is the hostname for this profile? eg lonsl11001457 :")
                
                startPort = raw_input ("What wouold you like your starting port to be? eg 12000 :")
                
                print "INFO: Creating Dmgr profile on host " + hostName + "with cell name " + cellName
                          
                
                try:
                    
                    print "INFO: Running managerprofile command: manageprofiles.sh -create -profileName " + profileName + "-nodeName " + nodeName + "-startingPort " + startPort + " -templatePath " + newLoc + "/profileTemplates/cell/dmgr"
                    
                    os.system('./manageprofiles.sh -create -templatePath ' + newLoc + '/profileTemplates/cell/dmgr' + ' -profilePath ' + newLoc + '/profiles' + ' -profileName ' + profileName + ' -nodeName ' + nodeName + ' startingPort ' + startPort )
                    
                except Exception:
                    
                    print "FAIL: Could not run the manage profiles script."
                    sys.exit(1)
                 
            else:
        
                print "You have choosen not to install the Dmgr profile"
                #createAppSvrProfile
                sys.exit(0)
        
                
        
        
        
        def createAppSvrProfile(self):
            print "INFO: AppServer base setup Tool"
            

            profile = raw_input("Is this a Base Application server profile installation? (y/n):")
    
            if profile == "y":
            
                print "This will install a Websphere Base Application Server profile"
        
                #createAppServerProfile()
        
               
                profileName = raw_input("What is the Appserver profile name? eg Appsvr01 :")
                 
                nodeName = raw_input("What is the nodename for this profile? eg lonsl11001457 :")
                
                startPort = raw_input ("What wouold you like your starting port to be? eg 12050 :")
                
                hostName = raw_input ("What is the hostname for this profile? eg lonsl11001457 :")
                
                print "INFO: Creating AppServer profile on host " + hostName
                          
                
                try:
                    
                    print "INFO: Running managerprofile command: manageprofiles.sh -create -profileName " + profileName + "-nodeName " + nodeName + "-startingPort " + startPort + " -templatePath " + newLoc + "/profileTemplates/cell/default"
                    
                    os.system('./manageprofiles.sh -create -templatePath ' + newLoc + '/profileTemplates/default' + ' -profilePath ' + newLoc + '/profiles' + ' -profileName ' + profileName + ' -nodeName ' + nodeName + ' startingPort ' + startPort )
                    
                except Exception:
                    
                    print "FAIL: Could not run the manage profiles script."
                    sys.exit(1)
            
                     
            else:
        
                print "You have choosen not to install the Dmgr profile"
                #createAppSvrProfile
                sys.exit(0)
        
        
        
        def federateNode(self):
            pass
         



if __name__ == '__main__':
    
   
    print "##################################################"
    print "#    Websphere 8.5 Automated Install Script      #"
    print "#                  v 0.1                         #"
    print "#           *Please install as root*             #"
    print "##################################################"
     
    iw = installWAS()
    iw.createResponse()
    iw.checkDiskSpace()
    iw.installWASBinaries()
