# total hours i speend here : 8472.1
# contact me if u add more detections
# Mohamed Alzhrani
# https://github.com/MazX0p
import sys
import csv
import re
from netaddr import *
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime , timezone
from dateutil.parser import parse
from dateutil.parser import isoparse
from pytz import timezone
import html
import base64
import codecs
import copy
import random
import sigma_manager
from time import sleep

try:
    from evtx import PyEvtxParser
    has_evtx = True
except ImportError:
    has_evtx = False

try:
    from lxml import etree
    has_lxml = True
except ImportError:
    has_lxml = False

try:
    import pandas as pd
    has_pandas = True
except ImportError:
    has_pandas = False


class bcolor:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CBLACK = '\33[30m'
    CRED = '\33[31m'
    RED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    BLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

#=======================
# Initiate list of JSON containing matched rules

Susp_exe=["\\mshta.exe","\\regsvr32.exe","\\csc.exe",'whoami.exe','\\pl.exe','\\nc.exe','nmap.exe','psexec.exe','plink.exe','mimikatz','procdump.exe',' dcom.exe',' Inveigh.exe',' LockLess.exe',' Logger.exe',' PBind.exe',' PS.exe',' Rubeus.exe',' RunasCs.exe',' RunAs.exe',' SafetyDump.exe',' SafetyKatz.exe',' Seatbelt.exe',' SExec.exe',' SharpApplocker.exe',' SharpChrome.exe',' SharpCOM.exe',' SharpDPAPI.exe',' SharpDump.exe',' SharpEdge.exe',' SharpEDRChecker.exe',' SharPersist.exe',' SharpHound.exe',' SharpLogger.exe',' SharpPrinter.exe','EfsPotato.exe',' SharpSC.exe',' SharpSniper.exe',' SharpSocks.exe',' SharpSSDP.exe',' SharpTask.exe',' SharpUp.exe',' SharpView.exe',' SharpWeb.exe',' SharpWMI.exe',' Shhmon.exe',' SweetPotato.exe',' Watson.exe',' WExec.exe','7zip.exe', 'HOSTNAME.EXE', 'hostname.exe']

Susp_commands=['FromBase64String','DomainPasswordSpray','PasswordSpray','Password','Get-WMIObject','Get-GPPPassword','Get-Keystrokes','Get-TimedScreenshot','Get-VaultCredential','Get-ServiceUnquoted','Get-ServiceEXEPerms','Get-ServicePerms','Get-RegAlwaysInstallElevated','Get-RegAutoLogon','Get-UnattendedInstallFiles','Get-Webconfig','Get-ApplicationHost','Get-PassHashes','Get-LsaSecret','Get-Information','Get-PSADForestInfo','Get-KerberosPolicy','Get-PSADForestKRBTGTInfo','Get-PSADForestInfo','Get-KerberosPolicy','Invoke-Command','Invoke-Expression','iex(','Invoke-Shellcode','Invoke--Shellcode','Invoke-ShellcodeMSIL','Invoke-MimikatzWDigestDowngrade','Invoke-NinjaCopy','Invoke-CredentialInjection','Invoke-TokenManipulation','Invoke-CallbackIEX','Invoke-PSInject','Invoke-DllEncode','Invoke-ServiceUserAdd','Invoke-ServiceCMD','Invoke-ServiceStart','Invoke-ServiceStop','Invoke-ServiceEnable','Invoke-ServiceDisable','Invoke-FindDLLHijack','Invoke-FindPathHijack','Invoke-AllChecks','Invoke-MassCommand','Invoke-MassMimikatz','Invoke-MassSearch','Invoke-MassTemplate','Invoke-MassTokens','Invoke-ADSBackdoor','Invoke-CredentialsPhish','Invoke-BruteForce','Invoke-PowerShellIcmp','Invoke-PowerShellUdp','Invoke-PsGcatAgent','Invoke-PoshRatHttps','Invoke-PowerShellTcp','Invoke-PoshRatHttp','Invoke-PowerShellWmi','Invoke-PSGcat','Invoke-Encode','Invoke-Decode','Invoke-CreateCertificate','Invoke-NetworkRelay','EncodedCommand','New-ElevatedPersistenceOption','wsman','Enter-PSSession','DownloadString','DownloadFile','Out-Word','Out-Excel','Out-Java','Out-Shortcut','Out-CHM','Out-HTA','Out-Minidump','HTTP-Backdoor','Find-AVSignature','DllInjection','ReflectivePEInjection','Base64','System.Reflection','System.Management','Restore-ServiceEXE','Add-ScrnSaveBackdoor','Gupt-Backdoor','Execute-OnTime','DNS_TXT_Pwnage','Write-UserAddServiceBinary','Write-CMDServiceBinary','Write-UserAddMSI','Write-ServiceEXE','Write-ServiceEXECMD','Enable-DuplicateToken','Remove-Update','Execute-DNSTXT-Code','Download-Execute-PS','Execute-Command-MSSQL','Download_Execute','Copy-VSS','Check-VM','Create-MultipleSessions','Run-EXEonRemote','Port-Scan','Remove-PoshRat','TexttoEXE','Base64ToString','StringtoBase64','Do-Exfiltration','Parse_Keys','Add-Exfiltration','Add-Persistence','Remove-Persistence','Find-PSServiceAccounts','Discover-PSMSSQLServers','Discover-PSMSExchangeServers','Discover-PSInterestingServices','Discover-PSMSExchangeServers','Discover-PSInterestingServices','Mimikatz','powercat','powersploit','PowershellEmpire','GetProcAddress','ICM','.invoke',' -e ','hidden','-w hidden','Invoke-Obfuscation-master','Out-EncodedWhitespaceCommand','Out-Encoded',"-EncodedCommand","-enc","-w hidden","[Convert]::FromBase64String","iex(","New-Object","Net.WebClient","-windowstyle hidden","DownloadFile","DownloadString","Invoke-Expression","Net.WebClient","-Exec bypass" ,"-ExecutionPolicy bypass"]

Susp_Arguments=["-EncodedCommand","-enc","-w hidden","[Convert]::FromBase64String","iex(","New-Object","Net.WebClient","-windowstyle hidden","DownloadFile","DownloadString","Invoke-Expression","Net.WebClient","-Exec bypass" ,"-ExecutionPolicy bypass"]

all_suspicious=["\\csc.exe",'whoami.exe','\\pl.exe','\\nc.exe','nmap.exe','psexec.exe','plink.exe','kali','mimikatz','procdump.exe',' dcom.exe',' Inveigh.exe',' LockLess.exe',' Logger.exe',' PBind.exe',' PS.exe',' Rubeus.exe',' RunasCs.exe',' RunAs.exe',' SafetyDump.exe',' SafetyKatz.exe',' Seatbelt.exe',' SExec.exe',' SharpApplocker.exe',' SharpChrome.exe',' SharpCOM.exe',' SharpDPAPI.exe',' SharpDump.exe',' SharpEdge.exe',' SharpEDRChecker.exe',' SharPersist.exe',' SharpHound.exe',' SharpLogger.exe',' SharpPrinter.exe',' SharpRoast.exe',' SharpSC.exe',' SharpSniper.exe',' SharpSocks.exe',' SharpSSDP.exe',' SharpTask.exe',' SharpUp.exe',' SharpView.exe',' SharpWeb.exe',' SharpWMI.exe',' Shhmon.exe',' SweetPotato.exe',' Watson.exe',' WExec.exe','7zip.exe','FromBase64String','DomainPasswordSpray','PasswordSpray','Password','Get-WMIObject','Get-GPPPassword','Get-Keystrokes','Get-TimedScreenshot','Get-VaultCredential','Get-ServiceUnquoted','Get-ServiceEXEPerms','Get-ServicePerms','Get-RegAlwaysInstallElevated','Get-RegAutoLogon','Get-UnattendedInstallFiles','Get-Webconfig','Get-ApplicationHost','Get-PassHashes','Get-LsaSecret','Get-Information','Get-PSADForestInfo','Get-KerberosPolicy','Get-PSADForestKRBTGTInfo','Get-PSADForestInfo','Get-KerberosPolicy','Invoke-Command','Invoke-Expression','iex(','Invoke-Shellcode','Invoke--Shellcode','Invoke-ShellcodeMSIL','Invoke-MimikatzWDigestDowngrade','Invoke-NinjaCopy','Invoke-CredentialInjection','Invoke-TokenManipulation','Invoke-CallbackIEX','Invoke-PSInject','Invoke-DllEncode','Invoke-ServiceUserAdd','Invoke-ServiceCMD','Invoke-ServiceStart','Invoke-ServiceStop','Invoke-ServiceEnable','Invoke-ServiceDisable','Invoke-FindDLLHijack','Invoke-FindPathHijack','Invoke-AllChecks','Invoke-MassCommand','Invoke-MassMimikatz','Invoke-MassSearch','Invoke-MassTemplate','Invoke-MassTokens','Invoke-ADSBackdoor','Invoke-CredentialsPhish','Invoke-BruteForce','Invoke-PowerShellIcmp','Invoke-PowerShellUdp','Invoke-PsGcatAgent','Invoke-PoshRatHttps','Invoke-PowerShellTcp','Invoke-PoshRatHttp','Invoke-PowerShellWmi','Invoke-PSGcat','Invoke-Encode','Invoke-Decode','Invoke-CreateCertificate','Invoke-NetworkRelay','EncodedCommand','New-ElevatedPersistenceOption','wsman','Enter-PSSession','DownloadString','DownloadFile','Out-Word','Out-Excel','Out-Java','Out-Shortcut','Out-CHM','Out-HTA','Out-Minidump','HTTP-Backdoor','Find-AVSignature','DllInjection','ReflectivePEInjection','Base64','System.Reflection','System.Management','Restore-ServiceEXE','Add-ScrnSaveBackdoor','Gupt-Backdoor','Execute-OnTime','DNS_TXT_Pwnage','Write-UserAddServiceBinary','Write-CMDServiceBinary','Write-UserAddMSI','Write-ServiceEXE','Write-ServiceEXECMD','Enable-DuplicateToken','Remove-Update','Execute-DNSTXT-Code','Download-Execute-PS','Execute-Command-MSSQL','Download_Execute','Copy-VSS','Check-VM','Create-MultipleSessions','Run-EXEonRemote','Port-Scan','Remove-PoshRat','TexttoEXE','Base64ToString','StringtoBase64','Do-Exfiltration','Parse_Keys','Add-Exfiltration','Add-Persistence','Remove-Persistence','Find-PSServiceAccounts','Discover-PSMSSQLServers','Discover-PSMSExchangeServers','Discover-PSInterestingServices','Discover-PSMSExchangeServers','Discover-PSInterestingServices','Mimikatz','powercat','powersploit','PowershellEmpire','GetProcAddress','ICM','.invoke',' -e ','hidden','-w hidden','Invoke-Obfuscation-master','Out-EncodedWhitespaceCommand','Out-Encoded',"-EncodedCommand","-enc","-w hidden","[Convert]::FromBase64String","iex(","New-Object","Net.WebClient","-windowstyle hidden","DownloadFile","DownloadString","Invoke-Expression","Net.WebClient","-Exec bypass" ,"-ExecutionPolicy bypass","-EncodedCommand","-enc","-w hidden","[Convert]::FromBase64String","iex(","New-Object","Net.WebClient","-windowstyle hidden","DownloadFile","DownloadString","Invoke-Expression","Net.WebClient","-Exec bypass" ,"-ExecutionPolicy bypass"]


Susp_Path=['\\temp\\',' C:\Windows\System32\mshta.exe','/temp/','//windows//temp//','/windows/temp/','\\windows\\temp\\','\\appdata\\','/appdata/','//appdata//','//programdata//','\\programdata\\','/programdata/']

Usual_Path=['\\Windows\\','/Windows/','//Windows//','Program Files','\\Windows\\SysWOW64\\','/Windows/SysWOW64/','//Windows//SysWOW64//','\\Windows\\Cluster\\','/Windows/Cluster/','//Windows//Cluster//']

#=======================
#Regex for security logs
MatchedRulesAgainstLogs = dict()

EventID_rex = re.compile('<EventID.*>(.*)<\/EventID>', re.IGNORECASE)

Logon_Type_rex = re.compile('<Data Name=\"LogonType\">(.*)</Data>|<LogonType>(.*)</LogonType>', re.IGNORECASE)

#======================
# My Regex For Sysmon Logs
User_Name_rex = re.compile('<Data Name=\"User\">(.*)</Data>|<User>(.*)</User>', re.IGNORECASE)
ProcessId_rex = re.compile('<Data Name=\"ProcessId\">(.*)</Data>|<ProcessId>(.*)</ProcessId>', re.IGNORECASE)
DestinationIp_rex = re.compile('<Data Name=\"DestinationIp\">(.*)</Data>|<DestinationIp>(.*)</DestinationIp>', re.IGNORECASE)
Destination_Is_Ipv6_rex = re.compile('<Data Name=\"DestinationIsIpv6\">(.*)</Data>|<DestinationIsIpv6>(.*)</DestinationIsIpv6>', re.IGNORECASE)
Source_Ip_Address_rex = re.compile('<Data Name=\"SourceIp\">(.*)</Data>|<SourceIp>(.*)</SourceIp>', re.IGNORECASE)
# UtcTime_rex = re.compile('<Data Name=\"UtcTime\">(.*)</Data>|<UtcTime>(.*)</UtcTime>|<TimeCreated SystemTime=\"(.*)\n    </TimeCreated>', re.IGNORECASE)
UtcTime_rex = re.compile('<TimeCreated SystemTime=\"(.*)\">\n    </TimeCreated>', re.IGNORECASE)
Protocol_rex = re.compile('<Data Name=\"Protocol\">(.*)</Data>|<Protocol>(.*)</Protocol>', re.IGNORECASE)
SourcePort_rex = re.compile('<Data Name=\"SourcePort\">(.*)</Data>|<SourcePort>(.*)</SourcePort>', re.IGNORECASE)
DestinationPort_rex = re.compile('<Data Name=\"DestinationPort\">(.*)</Data>|<DestinationPort>(.*)</DestinationPort>', re.IGNORECASE)
SourceHostname_rex = re.compile('<Data Name=\"SourceHostname\">(.*)</Data>|<SourceHostname>(.*)</SourceHostname>', re.IGNORECASE)
FileVersion_rex = re.compile('<Data Name=\"FileVersion\">(.*)</Data>|<FileVersion>(.*)</FileVersion>', re.IGNORECASE)
Description_rex = re.compile('<Data Name=\"Description\">(.*)</Data>|<Description>(.*)</Description>', re.IGNORECASE)
Hashes_rex = re.compile('<Data Name=\"Hashes\">(.*)</Data>|<Hashes>(.*)</Hashes>', re.IGNORECASE)
Computer_Name_rex = re.compile('<Computer>(.*)</Computer>', re.IGNORECASE)
ParentProcessId_rex = re.compile('<Data Name=\"ParentProcessId\">(.*)</Data>|<ParentProcessId>(.*)</ParentProcessId>', re.IGNORECASE)
ParentImage_rex = re.compile('<Data Name=\"ParentImage\">(.*)</Data>|<ParentImage>(.*)</ParentImage>', re.IGNORECASE)
ParentCommandLine_rex = re.compile('<Data Name=\"ParentCommandLine\">(.*)</Data>|<ParentCommandLine>(.*)</ParentCommandLine>', re.IGNORECASE)
GrandparentCommandLine_rex = re.compile('<Data Name=\"GrandparentCommandLine\">(.*)</Data>|<GrandparentCommandLine>(.*)</GrandparentCommandLine>', re.IGNORECASE)
Signed_rex = re.compile('<Data Name=\"Signed\">(.*)</Data>|<Signed>(.*)</Signed>', re.IGNORECASE)
Signature_rex = re.compile('<Data Name=\"Signature\">(.*)</Data>|<Signature>(.*)</Signature>', re.IGNORECASE)
State_rex = re.compile('<Data Name=\"State\">(.*)</Data>|<State>(.*)</State>', re.IGNORECASE)
Status_rex = re.compile('<Data Name=\"Status\">(.*)</Data>|<Status>(.*)</Status>', re.IGNORECASE)
# My Regex For Event Logs
Channel_rex = re.compile('<Channel.*>(.*)<\/Channel>', re.IGNORECASE)
Provider_rex = re.compile('<Provider Name=\"(.*)\" Guid', re.IGNORECASE)
EventSourceName_rex = re.compile('EventSourceName=\"(.*)\"', re.IGNORECASE)
ServiceName_rex = re.compile('<Data Name=\"ServiceName\">(.*)</Data>|<ServiceName>(.*)</ServiceName>', re.IGNORECASE)
Service_Image_Path_rex = re.compile('<Data Name=\"ImagePath\">(.*)</Data>|<ImagePath>(.*)</ImagePath>', re.IGNORECASE)
ServiceType_rex = re.compile('<Data Name=\"ServiceType\">(.*)</Data>|<ServiceType>(.*)</ServiceType>', re.IGNORECASE)
Service_Account_Name_rex = re.compile('<Data Name=\"AccountName\">(.*)</Data>|<AccountName>(.*)</AccountName>', re.IGNORECASE)
ServiceStartType_rex = re.compile('<Data Name=\"StartType\">(.*)</Data>|<StartType>(.*)</StartType>', re.IGNORECASE)
# My Regex for Security logs
AccountName_rex = re.compile('<Data Name=\"SubjectUserName\">(.*)</Data>|<SubjectUserName>(.*)</SubjectUserName>', re.IGNORECASE)
AccountDomain_rex = re.compile('<Data Name=\"SubjectDomainName\">(.*)</Data>|<SubjectDomainName>(.*)</SubjectDomainName>', re.IGNORECASE)
# My NetWork Regex
Source_IP_Address_rex = re.compile('<Data Name=\"IpAddress\">(.*)</Data>|<IpAddress>(.*)</IpAddress>', re.IGNORECASE)
Source_Port_rex = re.compile('<Data Name=\"IpPort\">(.*)</Data>|<IpPort>(.*)</IpPort>', re.IGNORECASE)
# My AD regex
ShareName_rex = re.compile('<Data Name=\"ShareName\">(.*)</Data>|<shareName>(.*)</shareName>', re.IGNORECASE)
ShareLocalPath_rex = re.compile('<Data Name=\"ShareLocalPath\">(.*)</Data>|<ShareLocalPath>(.*)</ShareLocalPath>', re.IGNORECASE)
RelativeTargetName_rex = re.compile('<Data Name=\"RelativeTargetName\">(.*)</Data>|<RelativeTargetName>(.*)</RelativeTargetName>', re.IGNORECASE)
AccountName_Target_rex = re.compile('<Data Name=\"TargetUserName\">(.*)</Data>|<TargetUserName>(.*)</TargetUserName>', re.IGNORECASE)
# My Task regex
TaskName_rex=re.compile('<Data Name=\"TaskName\">(.*)</Data>|<TaskName>(.*)</TaskName>', re.IGNORECASE)
TaskContent_rex = re.compile('<Data Name=\"TaskContent\">([^"]*)</Data>|<TaskContent>([^"]*)</TaskContent>', re.IGNORECASE)
TaskContent2_rex = re.compile('<Arguments>(.*)</Arguments>', re.IGNORECASE)
# My PowerShell regex
Powershell_Command_rex= re.compile('<Data Name=\"ScriptBlockText\">(.*)</Data>', re.IGNORECASE)
# My process Command Line Regex
Process_Command_Line_rex=re.compile('<Data Name=\"CommandLine\">(.*)</Data>|<CommandLine>(.*)</CommandLine>', re.IGNORECASE)
# My New Process Name regex
New_Process_Name_rex=re.compile('<Data Name=\"NewProcessName\">(.*)</Data>', re.IGNORECASE)
# My Regex
TokenElevationType_rex=re.compile('<Data Name=\"TokenElevationType\">(.*)</Data>', re.IGNORECASE)
# My PipeName Regex
PipeName_rex=re.compile("<Data Name=\"PipeName\">(.*)</Data>")
# My ImageName Regex
Image_rex=re.compile("<Data Name=\"Image\">(.*)</Data>")
#
ServicePrincipalNames_rex=re.compile("<Data Name=\"ServicePrincipalNames\">(.*)</Data>")
#
SamAccountName_rex=re.compile("<Data Name=\"SamAccountName\">(.*)</Data>")
#
NewTargetUserName_rex=re.compile("<Data Name=\"NewTargetUserName\">(.*)</Data>")
#
OldTargetUserName_rex=re.compile("<Data Name=\"OldTargetUserName\">(.*)</Data>")
# My Call Trace regex
CallTrace_rex=re.compile("<Data Name=\"CallTrace\">(.*)</Data>")
# My GrantedAccess Regex
GrantedAccess_rex=re.compile("<Data Name=\"GrantedAccess\">(.*)</Data>")
# My TargetImage Regex
TargetImage_rex=re.compile("<Data Name=\"TargetImage\">(.*)</Data>")
# My SourceImage Regex
SourceImage_rex=re.compile("<Data Name=\"SourceImage\">(.*)</Data>")


SourceProcessId_rex=re.compile("<Data Name=\"SourceProcessId\">(.*)</Data>")
#
SourceProcessGuid_rex=re.compile("<Data Name=\"SourceProcessGuid\">(.*)</Data>")
#
TargetProcessGuid_rex=re.compile("<Data Name=\"TargetProcessGuid\">(.*)</Data>")
#
TargetProcessId_rex=re.compile("<Data Name=\"TargetProcessId\">(.*)</Data>")
#
PowershellUserId_rex=re.compile("UserId=(.*)")
#
PowershellHostApplication_rex=re.compile("HostApplication=(.*)")
#
Powershell_ContextInfo= re.compile('<Data Name=\"ContextInfo\">(.*)</Data>', re.IGNORECASE)
#
Powershell_Payload= re.compile('<Data Name=\"Payload\">(.*)</Data>', re.IGNORECASE)
#
Powershell_Path= re.compile('<Data Name=\"Path\">(.*)</Data>', re.IGNORECASE)
#
Command_Name_rex = re.compile('CommandName = (.*)')
#
PowerShellCommand_rex = re.compile('<Data>[\s\S]*?</\Data>') # i will come back continue

#j
CommandLine_powershell_rex = re.compile('CommandLine= (.*)')
#
ScriptName_rex = re.compile('ScriptName=(.*)')
#
ErrorMessage_rex = re.compile('ErrorMessage=(.*)')

#======================

Security_ID_rex = re.compile('<Data Name=\"SubjectUserSid\">(.*)</Data>|<SubjectUserSid>(.*)</SubjectUserSid>', re.IGNORECASE)
Security_ID_Target_rex = re.compile('<Data Name=\"TargetUserSid\">(.*)</Data>|<TargetUserSid>(.*)</TargetUserSid>', re.IGNORECASE)


Account_Domain_Target_rex = re.compile('<Data Name=\"TargetDomainName\">(.*)</Data>|<TargetDomainName>(.*)</TargetDomainName>', re.IGNORECASE)

Workstation_Name_rex = re.compile('<Data Name=\"WorkstationName\">(.*)</Data>|<WorkstationName>(.*)</WorkstationName>', re.IGNORECASE)

Logon_Process_rex = re.compile('<Data Name=\"LogonProcessName\">(.*)</Data>|<LogonProcessName>(.*)</LogonProcessName>', re.IGNORECASE)

Key_Length_rex = re.compile('<Data Name=\"KeyLength\">(.*)</Data>|<KeyLength>(.*)</KeyLength>', re.IGNORECASE)

AccessMask_rex = re.compile('<Data Name=\"AccessMask\">(.*)</Data>|<AccessMask>(.*)</AccessMask>', re.IGNORECASE)

TicketOptions_rex=re.compile('<Data Name=\"TicketOptions\">(.*)</Data>|<TicketOptions>(.*)</TicketOptions>', re.IGNORECASE)
TicketEncryptionType_rex=re.compile('<Data Name=\"TicketEncryptionType\">(.*)</Data>|<TicketEncryptionType>(.*)</TicketEncryptionType>', re.IGNORECASE)

Group_Name_rex=re.compile('<Data Name=\"TargetUserName\">(.*)</Data>|<TargetUserName>(.*)</TargetUserName>', re.IGNORECASE)

Process_Name_sec_rex = re.compile('<Data Name=\"CallerProcessName\">(.*)</Data>|<CallerProcessName>(.*)</CallerProcessName>|<Data Name=\"ProcessName\">(.*)</Data>|<Data Name=\"NewProcessName\">(.*)</Data>', re.IGNORECASE)

Parent_Process_Name_sec_rex=re.compile('<Data Name=\"ParentProcessName\">(.*)</Data>|<ParentProcessName>(.*)</ParentProcessName>', re.IGNORECASE)


Category_sec_rex= re.compile('<Data Name=\"CategoryId\">(.*)</Data>|<CategoryId>(.*)</CategoryId>', re.IGNORECASE)

Subcategory_rex= re.compile('<Data Name=\"SubcategoryId\">(.*)</Data>|<SubcategoryId>(.*)</LogonType>', re.IGNORECASE)

Changes_rex= re.compile('<Data Name=\"AuditPolicyChanges\">(.*)</Data>|<AuditPolicyChanges>(.*)</AuditPolicyChanges>', re.IGNORECASE)

Member_Name_rex = re.compile('<Data Name=\"MemberName\">(.*)</Data>|<MemberName>(.*)</MemberName>', re.IGNORECASE)
Member_Sid_rex = re.compile('<Data Name=\"MemberSid\">(.*)</Data>|<MemberSid>(.*)</MemberSid>', re.IGNORECASE)

Object_Name_rex = re.compile('<Data Name=\"ObjectName\">(.*)</Data>|<ObjectName>(.*)</ObjectName>', re.IGNORECASE)

ObjectType_rex = re.compile('<Data Name=\"ObjectType\">(.*)</Data>|<ObjectType>(.*)</ObjectType>', re.IGNORECASE)

ObjectServer_rex = re.compile('<Data Name=\"ObjectServer\">(.*)</Data>|<ObjectServer>(.*)</ObjectServer>', re.IGNORECASE)


#=======================
#Regex for windows defender logs

Name_rex = re.compile('<Data Name=\"Threat Name\">(.*)</Data>|<Threat Name>(.*)</Threat Name>', re.IGNORECASE)

Severity_rex = re.compile('<Data Name=\"Severity Name\">(.*)</Data>|<Severity Name>(.*)</Severity Name>', re.IGNORECASE)

Category_rex = re.compile('<Data Name=\"Category Name\">(.*)</Data>|<Category Name>(.*)</Category Name>', re.IGNORECASE)

Path_rex = re.compile('<Data Name=\"Path\">(.*)</Data>|<Path>(.*)</Path>', re.IGNORECASE)

Defender_Remediation_User_rex = re.compile('<Data Name=\"Remediation User\">(.*)</Data>|<Remediation User>(.*)</Remediation User>', re.IGNORECASE)

Defender_User_rex = re.compile('<Data Name=\"User\">(.*)</Data>|<User>(.*)</User>', re.IGNORECASE)

Process_Name_rex = re.compile('<Data Name=\"Process Name\">(.*)</Data>|<Process Name>(.*)</Process Name>', re.IGNORECASE)

Action_rex = re.compile('<Data Name=\"Action ID\">(.*)</Data>|<Action ID>(.*)</Action ID>', re.IGNORECASE)

#=======================
#Regex for system logs


#=======================
#Regex for task scheduler logs
Task_Name = re.compile('<Data Name=\"TaskName\">(.*)</Data>|<TaskName>(.*)</TaskName>', re.IGNORECASE)
Task_Registered_User_rex = re.compile('<Data Name=\"UserContext\">(.*)</Data>|<UserContext>(.*)</UserContext>', re.IGNORECASE)
Task_Deleted_User_rex = re.compile('<Data Name=\"UserName\">(.*)</Data>|<UserName>(.*)</UserName>', re.IGNORECASE)


#======================
#Regex for powershell operational logs
Powershell_ContextInfo= re.compile('<Data Name=\"ContextInfo\">(.*)</Data>', re.IGNORECASE)
Powershell_Payload= re.compile('<Data Name=\"Payload\">(.*)</Data>', re.IGNORECASE)
Powershell_Path= re.compile('<Data Name=\"Path\">(.*)</Data>', re.IGNORECASE)

Host_Application_rex = re.compile('Host Application = (.*)')
Command_Name_rex = re.compile('Command Name = (.*)')
Command_Type_rex = re.compile('Command Type = (.*)')
Engine_Version_rex = re.compile('Engine Version = (.*)')
User_rex = re.compile('User = (.*)')
Error_Message_rex = re.compile('Error Message = (.*)')

#======================
#Regex for powershell logs
HostApplication_rex = re.compile('HostApplication=(.*)')
CommandLine_rex = re.compile('CommandLine=(.*)')
ScriptName_rex = re.compile('ScriptName=(.*)')
EngineVersion_rex = re.compile('EngineVersion=(.*)')
UserId_rex = re.compile('UserId=(.*)')
ErrorMessage_rex = re.compile('ErrorMessage=(.*)')
#======================
#TerminalServices Local Session Manager Logs
#Source_Network_Address_Terminal_rex= re.compile('Source Network Address: (.*)')
#Source_Network_Address_Terminal_rex= re.compile('<Address>(.*)</Address>')
Source_Network_Address_Terminal_rex= re.compile('<Address>((\d{1,3}\.){3}\d{1,3})</Address>')
Source_Network_Address_Terminal_NotIP_rex= re.compile('<Address>(.*)</Address>')
User_Terminal_rex=re.compile('User>(.*)</User>')
Session_ID_rex=re.compile('<SessionID>(.*)</SessionID>')
#======================
#Microsoft-Windows-WinRM logs
Connection_rex=re.compile('<Data Name=\"connection\">(.*)</Data>|<connection>(.*)</connection>', re.IGNORECASE)
Winrm_UserID_rex=re.compile('<Security UserID=\"(.*)\"', re.IGNORECASE)

#User_ID_rex=re.compile("""<Security UserID=\'(?<UserID>.*)\'\/><\/System>""")
#src_device_rex=re.compile("""<Computer>(?<src>.*)<\/Computer>""")
#======================
#Sysmon Logs
Sysmon_CommandLine_rex=re.compile("<Data Name=\"CommandLine\">(.*)</Data>")
Sysmon_ProcessGuid_rex=re.compile("<Data Name=\"ProcessGuid\">(.*)</Data>")
Sysmon_ProcessId_rex=re.compile("<Data Name=\"ProcessId\">(.*)</Data>")
Sysmon_FileName_rex=re.compile("<Data Name=\"FileName\">(.*)</Data>")
Sysmon_ImageFileName_rex=re.compile("<Data Name=\"ImageFileName\">(.*)</Data>")
Sysmon_Initiated_rex=re.compile("<Data Name=\"Initiated\">(.*)</Data>")
Sysmon_FileVersion_rex=re.compile("<Data Name=\"FileVersion\">(.*)</Data>")
Sysmon_Company_rex=re.compile("<Data Name=\"Company\">(.*)</Data>")
Sysmon_Product_rex=re.compile("<Data Name=\"Product\">(.*)</Data>")
Sysmon_Description_rex=re.compile("<Data Name=\"Description\">(.*)</Data>")
Sysmon_User_rex=re.compile("<Data Name=\"User\">(.*)</Data>")
Sysmon_LogonGuid_rex=re.compile("<Data Name=\"LogonGuid\">(.*)</Data>")
Sysmon_TerminalSessionId_rex=re.compile("<Data Name=\"TerminalSessionId\">(.*)</Data>")
Sysmon_Hashes_MD5_rex=re.compile("<Data Name=\"MD5=(.*),")
Sysmon_Hashes_SHA256_rex=re.compile("<Data Name=\"SHA256=(.*)")
Sysmon_IntegrityLevel_rex=re.compile("<Data Name=\"IntegrityLevel\">(.*)</Data>")
Sysmon_ParentProcessGuid_rex=re.compile("<Data Name=\"ParentProcessGuid\">(.*)</Data>")
Sysmon_ParentProcessId_rex=re.compile("<Data Name=\"ParentProcessId\">(.*)</Data>")
Sysmon_ParentCommandLine_rex=re.compile("<Data Name=\"ParentCommandLine\">(.*)</Data>")
Sysmon_ParentUser_rex=re.compile("<Data Name=\"ParentUser\">(.*)</Data>")
Sysmon_ProviderName_rex=re.compile("<Data Name=\"ProviderName\">(.*)</Data>")
Sysmon_CurrentDirectory_rex=re.compile("<Data Name=\"CurrentDirectory\">(.*)</Data>")
Sysmon_OriginalFileName_rex=re.compile("<Data Name=\"OriginalFileName\">(.*)</Data>")
Sysmon_TargetObject_rex=re.compile("<Data Name=\"TargetObject\">(.*)</Data>")
#########
#Sysmon  event ID 3
Sysmon_Protocol_rex=re.compile("<Data Name=\"Protocol\">(.*)</Data>")
Sysmon_SourceIp_rex=re.compile("<Data Name=\"SourceIp\">(.*)</Data>")
Sysmon_SourceHostname_rex=re.compile("<Data Name=\"SourceHostname\">(.*)</Data>")
Sysmon_SourcePort_rex=re.compile("<Data Name=\"SourcePort\">(.*)</Data>")
Sysmon_DestinationIp_rex=re.compile("<Data Name=\"DestinationIp\">(.*)</Data>")
Sysmon_DestinationHostname_rex=re.compile("<Data Name=\"DestinationHostname\">(.*)</Data>")
Sysmon_DestinationPort_rex=re.compile("<Data Name=\"DestinationPort\">(.*)</Data>")

#########
#Sysmon  event ID 8
Sysmon_StartFunction_rex=re.compile("<Data Name=\"StartFunction\">(.*)</Data>")
Sysmon_StartModule_rex=re.compile("<Data Name=\"StartModule\">(.*)</Data>")

#########
Sysmon_ImageLoaded_rex=re.compile("<Data Name=\"ImageLoaded\">(.*)</Data>")
Sysmon_Details_rex=re.compile("<Data Name=\"Details\">(.*)</Data>")
Sysmon_GrantedAccess_rex=re.compile("<Data Name=\"GrantedAccess\">(.*)</Data>")
Sysmon_CallTrace_rex=re.compile("<Data Name=\"CallTrace\">(.*)</Data>")

##########

Security_Authentication_Summary=[{'User':[],'SID':[],'Number of Successful Logins':[]}]
Logon_Events=[{'Date and Time':[],'timestamp':[],'Event ID':[],'Account Name':[],'Account Domain':[],'Logon Type':[],'Logon Process':[],'Source IP':[],'Workstation Name':[],'Computer Name':[],'Channel':[],'Original Event Log':[]}]

EVTX_HEADER = b"\x45\x6C\x66\x46\x69\x6C\x65\x00"
evtx_list = []
user_list = []
user_list_2 = []
sourceIp_list = []
sourceIp_list_2 = []
#cve-2021-42287 Detect
REQUEST_TGT_CHECK_list = []
New_Target_User_Name_Check_list = []
SAM_ACCOUNT_NAME_CHECK_list = []
ATTACK_REPLAY_CHECK_list = []


# IPv4 regex
IPv4_PATTERN = re.compile(r"\A\d+\.\d+\.\d+\.\d+\Z", re.DOTALL)

# IPv6 regex
IPv6_PATTERN = re.compile(r"\A(::(([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})){0,5})?|([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(::(([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})){0,4})?|:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(::(([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})){0,3})?|:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(::(([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})){0,2})?|:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(::(([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3}))?)?|:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})(::([0-9a-f]|[1-9a-f][0-9a-f]{1,3})?|(:([0-9a-f]|[1-9a-f][0-9a-f]{1,3})){3}))))))\Z", re.DOTALL)


evtx_list2 = ["/mnt/c/Users/ahmad/Desktop/biz/project/downloads/EVTX-ATTACK-SAMPLES-master/Discovery/discovery_psloggedon.evtx"]

#detect base64 commands
def isBase64(command):
    try:
        return base64.b64encode(base64.b64decode(command)) == command
    except Exception:
        return False


def to_lxml(record_xml):
    rep_xml = record_xml.replace("xmlns=\"http://schemas.microsoft.com/win/2004/08/events/event\"", "")
    fin_xml = rep_xml.encode("utf-8")
    parser = etree.XMLParser(resolve_entities=False)
    return etree.fromstring(fin_xml, parser)


def xml_records(filename):
    evtx = None
    if evtx is None:
        with open(filename, "rb") as evtx:
            parser = PyEvtxParser(evtx)
            for record in parser.records():
                try:
                    yield to_lxml(record["data"]), None
                except etree.XMLSyntaxError as e:
                    yield record["data"], e

def checker(check):
    if check == "REQUEST_TGT_CHECK":
        REQUEST_TGT_CHECK_list.append("True")
    if check == "New_Target_User_Name_Check":
        New_Target_User_Name_Check_list.append("True")
    if check == "SAM_ACCOUNT_NAME_CHECK":
        SAM_ACCOUNT_NAME_CHECK_list.append("True")
    if check == "ATTACK_REPLAY_CHECK":
        ATTACK_REPLAY_CHECK_list.append("True")

def event_sanity_check(field):
    if isinstance(field,list):
        if len(field) == 0:
            return field
        else:
            if isinstance(field[0],tuple):
                return field[0][0]
            else:
                return field[0]
    elif isinstance(field,tuple):
        return field[0]
    elif isinstance(field,str):
        return field

def field_filter(field,key):
    # add logic here to filter fields and troubleshoot
    if key == "Hashes":
        md5 = ""
        sha1 = ""
        sha256 = ""
        imphash = ""
        if len(field) == 0:
            return md5, sha1, sha256, imphash
        else:
            hashes = field.split(",")
            for hash in hashes:
                if hash.startswith("MD5="):
                    md5 = hash.strip("MD5=")
                if hash.startswith("SHA1="):
                    sha1 = hash.strip("SHA1=")
                if hash.startswith("SHA256="):
                    sha256 = hash.strip("SHA256=")
                if hash.startswith("IMPHASH="):
                    imphash = hash.strip("IMPHASH=")
            return md5, sha1, sha256, imphash

def detect_events_security_log(file_name):
    for file in file_name:
        parser = PyEvtxParser(file)
        for record in parser.records():
            EventID = EventID_rex.findall(record['data'])
            #Parsing starts here
            if len(EventID) > 0:
                Logon_Type = Logon_Type_rex.findall(record['data'])

                #=====================
                # Mine

                UtcTime = UtcTime_rex.findall(record['data'])
                User_Name = User_Name_rex.findall(record['data'])
                Source_IP_2 = Source_Ip_Address_rex.findall(record['data'])
                Destination_IP_2 = DestinationIp_rex.findall(record['data'])
                SourcePort_2 = SourcePort_rex.findall(record['data'])
                DestinationPort_2 = DestinationPort_rex.findall(record['data'])
                SourceHostname_2 = SourceHostname_rex.findall(record['data'])
                Process_Id = ProcessId_rex.findall(record['data'])
                Destination_IP = DestinationIp_rex.findall(record['data'])
                Protocol_2 = Protocol_rex.findall(record['data'])
                Command_line = Process_Command_Line_rex.findall(record['data'])
                FileVersion = FileVersion_rex.findall(record['data'])
                Hashes = Hashes_rex.findall(record['data'])
                Description = Description_rex.findall(record['data'])
                Computer_Name = Computer_Name_rex.findall(record['data'])
                ParentProcessId = ParentProcessId_rex.findall(record['data'])
                ParentImage = ParentImage_rex.findall(record['data'])
                ParentCommandLine = ParentCommandLine_rex.findall(record['data'])
                ParentCommandLine = ParentCommandLine_rex.findall(record['data'])
                Computer = Computer_Name_rex.findall(record['data'])
                Channel = Channel_rex.findall(record['data'])
                Provider_Name = Provider_rex.findall(record['data'])
                EventSource_Name = EventSourceName_rex.findall(record['data'])
                ServiceName = ServiceName_rex.findall(record['data'])
                Service_Image_Path = Service_Image_Path_rex.findall(record['data'])
                ServiceType = ServiceType_rex.findall(record['data'])
                ServiceStartType = ServiceStartType_rex.findall(record['data'])
                Service_Account_Name = Service_Account_Name_rex.findall(record['data'])
                Account_Name = AccountName_rex.findall(record['data'])
                Account_Domain = AccountDomain_rex.findall(record['data'])
                Source_IP = Source_IP_Address_rex.findall(record['data'])
                Source_Port = Source_Port_rex.findall(record['data'])
                ShareName = ShareName_rex.findall(record['data'])
                ShareLocalPath = ShareLocalPath_rex.findall(record['data'])
                RelativeTargetName = RelativeTargetName_rex.findall(record['data'])
                Task_Name = TaskName_rex.findall(record['data'])
                Task_Content = TaskContent_rex.findall(record['data'])
                TargetAccount_Name = AccountName_Target_rex.findall(record['data'])
                Target_Account_Domain=Account_Domain_Target_rex.findall(record['data'])
                Workstation_Name = Workstation_Name_rex.findall(record['data'])
                PowerShell_Command = Powershell_Command_rex.findall(record['data'])
                New_Process_Name = New_Process_Name_rex.findall(record['data'])
                TokenElevationType = TokenElevationType_rex.findall(record['data'])
                PipeName2 = PipeName_rex.findall(record['data'])
                ImageName2 = Image_rex.findall(record['data'])
                ServicePrincipalNames = ServicePrincipalNames_rex.findall(record['data'])
                SamAccountName = SamAccountName_rex.findall(record['data'])
                NewTargetUserName = NewTargetUserName_rex.findall(record['data'])
                OldTargetUserName = OldTargetUserName_rex.findall(record['data'])
                TargetProcessId = TargetProcessId_rex.findall(record['data'])
                TargetProcessGuid = TargetProcessGuid_rex.findall(record['data'])
                SourceProcessGuid = SourceProcessGuid_rex.findall(record['data'])
                SourceProcessId = SourceProcessId_rex.findall(record['data'])
                SourceImage = SourceImage_rex.findall(record['data'])
                TargetImage = TargetImage_rex.findall(record['data'])
                GrantedAccess = GrantedAccess_rex.findall(record['data'])
                CallTrace = CallTrace_rex.findall(record['data'])
                PowershellUserId = PowershellUserId_rex.findall(record['data'])
                PowershellHostApplication = PowershellHostApplication_rex.findall(record['data'])
                Command_Name = Command_Name_rex.findall(record['data'])
                CommandLine_powershell = CommandLine_powershell_rex.findall(record['data'])
                PowerShellCommand = PowerShellCommand_rex.findall(record['data'])
                PowerShellCommand_All = record['data']
                ScriptName = ScriptName_rex.findall(record['data'])
                #====================

                Logon_Process = Logon_Process_rex.findall(record['data'])

                Key_Length = Key_Length_rex.findall(record['data'])

                Security_ID = Security_ID_rex.findall(record['data'])

                Group_Name = Group_Name_rex.findall(record['data'])

                Member_Name =  Member_Name_rex.findall(record['data'])



                Member_Sid =Member_Sid_rex.findall(record['data'])

                Process_Name=Process_Name_sec_rex.findall(record['data'])

                Parent_Process_Name = Parent_Process_Name_sec_rex.findall(record['data'])

                Category=Category_sec_rex.findall(record['data'])

                Subcategory=Subcategory_rex.findall(record['data'])

                Changes=Changes_rex.findall(record['data'])

                Process_Command_Line = Process_Command_Line_rex.findall(record['data'])


                Object_Name = Object_Name_rex.findall(record['data'])

                Object_Type = ObjectType_rex.findall(record['data'])
                ObjectServer = ObjectServer_rex.findall(record['data'])
                AccessMask = AccessMask_rex.findall(record['data'])

                PASS = False
                PASS1 = False

                ##The function will probably be called here . Just adding the comment for now.

                ### Create JSON of Event
                Event = {
                    "Timestamp" : UtcTime_rex.findall(record['data']),
                    "EventID" : EventID_rex.findall(record['data']),
                    "Computer" : Computer_Name_rex.findall(record['data']),
                    "AccessMask" : AccessMask_rex.findall(record['data']),
                    "AccountName" : Service_Account_Name_rex.findall(record['data']),
                    "Action" : Action_rex.findall(record['data']),
                    "AuditPolicyChanges" : Changes_rex.findall((record['data'])),
                    "CallTrace" : CallTrace_rex.findall(record['data']),
                    "CallerProcessName":Process_Name_sec_rex.findall(record['data']),
                    "Channel" : Channel_rex.findall(record['data']),
                    "CommandLine" : Sysmon_CommandLine_rex.findall(record['data']),
                    "Company" : Sysmon_Company_rex.findall(record['data']),
                    "ContextInfo" : Powershell_ContextInfo.findall(record['data']),
                    "CurrentDirectory" : Sysmon_CurrentDirectory_rex.findall(record['data']),
                    "Description" : Description_rex.findall(record['data']),
                    "DestinationHostname" : Sysmon_DestinationHostname_rex.findall(record['data']),
                    "DestinationIp" : DestinationIp_rex.findall(record['data']),
                    "DestinationIsIpv6" : Destination_Is_Ipv6_rex.findall(record['data']),
                    "DestinationPort" : DestinationPort_rex.findall(record['data']),
                    "Details" : Sysmon_Details_rex.findall(record['data']),
                    "EngineVersion" : EngineVersion_rex.findall(record['data']),
                    "FileName" : Sysmon_FileName_rex.findall(record['data']),
                    "FileVersion" : FileVersion_rex.findall(record['data']),
                    "GrantedAccess" : GrantedAccess_rex.findall(record['data']),
                    "GrandparentCommandLine" : GrandparentCommandLine_rex.findall(record['data']),
                    "Hashes" : Hashes_rex.findall(record['data']),
                    "HostApplication" : HostApplication_rex.findall(record['data']),
                    "Image" : Image_rex.findall(record['data']),
                    "ImageFileName" : Sysmon_ImageFileName_rex.findall(record['data']),
                    "ImageLoaded" : Sysmon_ImageLoaded_rex.findall(record['data']),
                    "ImagePath" : Service_Image_Path_rex.findall(record['data']),
                    "Initiated" : Sysmon_Initiated_rex.findall(record['data']),
                    "IntegrityLevel" : Sysmon_IntegrityLevel_rex.findall(record['data']),
                    "IpAddress" : Source_IP_Address_rex.findall(record['data']),
                    "KeyLength" : Key_Length_rex.findall(record['data']),
                    "LogonProcessName" : Logon_Process_rex.findall(record['data']),
                    "LogonType" : Logon_Type_rex.findall(record['data']),
                    "NewTargetUserName" : NewTargetUserName_rex.findall(record['data']),
                    "ObjectName" : Object_Name_rex.findall(record['data']),
                    "ObjectServer" : ObjectServer_rex.findall(record['data']),
                    "ObjectType" : ObjectType_rex.findall(record['data']),
                    "OldTargetUserName" : OldTargetUserName_rex.findall(record['data']),
                    "OriginalFileName" : Sysmon_OriginalFileName_rex.findall(record['data']),
                    "ParentCommandLine" : ParentCommandLine_rex.findall(record['data']),
                    "ParentImage" : ParentImage_rex.findall(record['data']),
                    "ParentUser" : Sysmon_ParentUser_rex.findall(record['data']),
                    "Path" : Path_rex.findall(record['data']),
                    "Payload" : Powershell_Payload.findall(record['data']),
                    "PipeName" : PipeName_rex.findall(record['data']),
                    "ProcessId" : ProcessId_rex.findall(record['data']),
                    "Product" : Sysmon_Product_rex.findall(record['data']),
                    "Protocol" : Protocol_rex.findall(record['data']),
                    "ProviderName" : Provider_rex.findall(record['data']),
                    "Provider_Name" : Provider_rex.findall(record['data']),
                    "RelativeTargetName" : RelativeTargetName_rex.findall(record['data']),
                    "SamAccountName" : SamAccountName_rex.findall(record['data']),
                    "ScriptBlockText" : Powershell_Command_rex.findall(record['data']),
                    "ServiceName" : ServiceName_rex.findall(record['data']),
                    "ServicePrincipalNames" : ServicePrincipalNames_rex.findall(record['data']),
                    "ServiceStartType" : ServiceStartType_rex.findall(record['data']),
                    "ServiceType" : ServiceType_rex.findall(record['data']),
                    "ShareName" : ShareName_rex.findall(record['data']),
                    "Signed" : Signed_rex.findall(record['data']),
                    "Signature" : Signature_rex.findall(record['data']),
                    "SourceImage" : SourceImage_rex.findall(record['data']),
                    "SourceIp" : Source_Ip_Address_rex.findall(record['data']),
                    "SourcePort" : SourcePort_rex.findall(record['data']),
                    "Source_Name" : EventSourceName_rex.findall(record['data']),
                    "StartFunction" : Sysmon_StartFunction_rex.findall(record['data']),
                    "StartModule" : Sysmon_StartModule_rex.findall(record['data']),
                    "State" : State_rex.findall(record['data']),
                    "Status" : Status_rex.findall(record['data']),
                    "SubjectDomainName" : AccountDomain_rex.findall(record['data']),
                    "SubjectUserName" : AccountName_rex.findall(record['data']),
                    "SubjectUserSid" : Security_ID_rex.findall(record['data']),
                    "TargetImage" : TargetImage_rex.findall(record['data']),
                    "TargetObject" : Sysmon_TargetObject_rex.findall(record['data']),
                    "TargetUserName" : AccountName_Target_rex.findall(record['data']),
                    "TargetUserSid" : Security_ID_Target_rex.findall(record['data']),
                    "Task_Name" : TaskName_rex.findall(record['data']),
                    "TicketEncryptionType" : TicketEncryptionType_rex.findall(record['data']),
                    "TicketOptions" : TicketOptions_rex.findall(record['data']),
                    "User" : User_Name_rex.findall(record['data']),
                    "UserName" : Task_Deleted_User_rex.findall(record['data']),
                    "WorkstationName" : Workstation_Name_rex.findall(record['data']),
                }
                for key in Event:
                    Event[key] = event_sanity_check(Event[key])
                # minor field corrections
                Event["md5"], Event["sha1"], Event["sha256"], Event["Imphash"] = field_filter(Event["Hashes"], "Hashes")
                #check for matched rules
                #Loader function

                Matched_Rules = sigma_manager.MatchRules(Event)

                if len(Matched_Rules) == 0:
                    pass
                else:
                    for matched_rule in range(0,len(Matched_Rules)):
                        rule_title = Matched_Rules[matched_rule]["title"]
                        if "falsepositives" in Matched_Rules[matched_rule]:
                            rule_fp = Matched_Rules[matched_rule]["falsepositives"]
                        else:
                            rule_fp = ["None"]
                        if rule_title in MatchedRulesAgainstLogs.keys():
                            MatchedRulesAgainstLogs[rule_title]["Events"].append(Event)
                        else:
                            MatchedRulesAgainstLogs[rule_title] = {
                                "falsepositives" : rule_fp,
                                "Events" : list()
                            }
                            MatchedRulesAgainstLogs[rule_title]["Events"].append(Event)

                #Detect any log that contain suspicious process name or argument
                if EventID[0]=="3":
                    try:
                        if len(User_Name[0][0])>0:
                            UserName_2 = User_Name[0][0].strip()
                            source_ip = Source_IP_2[0][0].strip()
                            Source_Port = SourcePort_2[0][0].strip()
                            Process_id = Process_Id[0][0].strip()
                            Destination_ip = Destination_IP[0][0].strip()
                            Destination_Port = DestinationPort_2[0][0].strip()
                            Source_Hostname = SourceHostname_2[0][0].strip()
                            Protocol_22 = Protocol_2[0][0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        if len(User_Name[0][1])>0:
                            UserName_2 = User_Name[0][1]
                            source_ip = Source_IP_2[0][1].strip()
                            Source_Port = SourcePort_2[0][1].strip()
                            Process_id = Process_Id[0][1].strip()
                            Destination_ip = Destination_IP[0][1].strip()
                            Destination_Port = DestinationPort_2[0][1].strip()
                            Source_Hostname = SourceHostname_2[0][1].strip()
                            Protocol_22 = Protocol_2[0][1].strip()
                            UtcTime1 = UtcTime[0][1].strip()


                        for i in Susp_exe:

                           if i in record['data'].lower():

                               print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                               print(" [+] \033[0;31;47mFound Suspicios "+ i +" Process Make TCP Connection \033[0m\n ", end='')
                               print(" [+] Source IP : ( %s ) \n " % source_ip, end='')
                               print(" [+] Source Port : ( %s ) \n " % Source_Port, end='')
                               print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                               print(" [+] Host Name : ( %s ) \n " % Source_Hostname, end='')
                               print(" [+] Destination IP : ( %s ) \n " % Destination_ip, end='')
                               print(" [+] Destination port : ( %s ) \n " % Destination_Port, end='')
                               print(" [+] Protocol : ( %s ) \n " % Protocol_22, end='')
                               print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                               print("____________________________________________________\n")

                               PASS = True
                               Suspicios_Event3 = i

                    except Exception as e:
                        pass


                elif EventID[0]=="1" and PASS== True:
                    try:
                        if len(User_Name[0][0])>0:
                            UserName_2 = User_Name[0][0].strip()
                            Process_id = Process_Id[0][0].strip()
                            Command_line_2 = Command_line[0][0].strip()
                            Fileversion = FileVersion[0][0].strip()
                            hashes = Hashes[0][0].strip()
                            description = Description[0][0].strip()
                            computer = Computer_Name[0].strip()
                            ParentProcessid = ParentProcessId[0][0].strip()
                            Parentimage = ParentImage[0][0].strip()
                            ParentCommandline = ParentCommandLine[0][0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        if len(User_Name[0][1])>0:
                            UserName_2 = User_Name[0][1]
                            Process_id = Process_Id[0][1].strip()
                            Command_line_2 = Command_line[0][1].strip()
                            Fileversion = FileVersion[0][1].strip()
                            hashes = Hashes[0][1].strip()
                            description = Description[0][1].strip()
                            computer = Computer_Name[1].strip()
                            ParentProcessid = ParentProcessId[0][1].strip()
                            Parentimage = ParentImage[0][1].strip()
                            ParentCommandline = ParentCommandLine[0][1].strip()
                            UtcTime1 = UtcTime[0][1].strip()


                        hashes = re.findall(r'(?i)(?<![a-z0-9])[a-f0-9]{32}(?![a-z0-9])', hashes)
                        MD5 = hashes[0].strip()
                        print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                        print(" [+] \033[0;31;47mThe Creation Process from "+ Suspicios_Event3 +" \033[0m\n ", end='')
                        print(" [+] Command Line : ( %s ) \n " % Command_line_2 , end='')
                        print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                        print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                        print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                        print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                        print(" [+] description : ( %s ) \n " % description, end='')
                        print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                        print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                        print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                        print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                        print("____________________________________________________\n")

                        # Detect LethHTA
                        if "mshta.exe" in Command_line_2 and "svchost.exe -k DcomLaunch" in ParentCommandline:
                            print(" [+] \033[0;31;47mLethalHTA Detected !! \033[0m\n ", end='')
                            print("[+] \033[0;31;47mBy Process ID "+ Process_id +" \033[0m\n ", end='')

                    except Exception as e:
                        pass

                # Detect PowershellRemoting via wsmprovhost
                elif EventID[0]=="1":
                    try:
                        if len(User_Name[0][0])>0:
                            UserName_2 = User_Name[0][0].strip()
                            Process_id = Process_Id[0][0].strip()
                            Command_line_2 = Command_line[0][0].strip()
                            Fileversion = FileVersion[0][0].strip()
                            hashes = Hashes[0][0].strip()
                            description = Description[0][0].strip()
                            computer = Computer_Name[0].strip()
                            ParentProcessid = ParentProcessId[0][0].strip()
                            Parentimage = ParentImage[0][0].strip()
                            ParentCommandline = ParentCommandLine[0][0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        if len(User_Name[0][1])>0:
                            UserName_2 = User_Name[0][1]
                            Process_id = Process_Id[0][1].strip()
                            Command_line_2 = Command_line[0][1].strip()
                            Fileversion = FileVersion[0][1].strip()
                            hashes = Hashes[0][1].strip()
                            description = Description[0][1].strip()
                            computer = Computer_Name[1].strip()
                            ParentProcessid = ParentProcessId[0][1].strip()
                            Parentimage = ParentImage[0][1].strip()
                            ParentCommandline = ParentCommandLine[0][1].strip()
                            UtcTime1 = UtcTime[0][1].strip()


                        hashes = re.findall(r'(?i)(?<![a-z0-9])[a-f0-9]{32}(?![a-z0-9])', hashes)
                        MD5 = hashes[0].strip()


                        # Detect PowershellRemoting via wsmprovhost
                        if "wsmprovhost.exe" in Parentimage and "wsmprovhost.exe -Embedding" in ParentCommandline:
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mPowershellRemoting via wsmprovhost Detected !! \033[0m\n ", end='')
                            print(" [+] Command Line : ( %s ) \n " % Command_line_2 , end='')
                            print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                            print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                            print(" [+] description : ( %s ) \n " % description, end='')
                            print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                            print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass


                # Detect PowershellRemoting via wsmprovhost
                if EventID[0]=="10":
                    try:
                        if len(User_Name[0][0])>0:
                            UserName_2 = User_Name[0][0].strip()
                            Process_id = Process_Id[0][0].strip()
                            Command_line_2 = Command_line[0][0].strip()
                            Fileversion = FileVersion[0][0].strip()
                            hashes = Hashes[0][0].strip()
                            description = Description[0][0].strip()
                            computer = Computer_Name[0].strip()
                            ParentProcessid = ParentProcessId[0][0].strip()
                            Parentimage = ParentImage[0][0].strip()
                            ParentCommandline = ParentCommandLine[0][0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        if len(User_Name[0][1])>0:
                            UserName_2 = User_Name[0][1]
                            Process_id = Process_Id[0][1].strip()
                            Command_line_2 = Command_line[0][1].strip()
                            Fileversion = FileVersion[0][1].strip()
                            hashes = Hashes[0][1].strip()
                            description = Description[0][1].strip()
                            computer = Computer_Name[1].strip()
                            ParentProcessid = ParentProcessId[0][1].strip()
                            Parentimage = ParentImage[0][1].strip()
                            ParentCommandline = ParentCommandLine[0][1].strip()
                            UtcTime1 = UtcTime[0][1].strip()


                        hashes = re.findall(r'(?i)(?<![a-z0-9])[a-f0-9]{32}(?![a-z0-9])', hashes)
                        MD5 = hashes[0].strip()


                        # Detect PowershellRemoting via wsmprovhost
                        if "wsmprovhost.exe" in Parentimage and "wsmprovhost.exe -Embedding" in ParentCommandline:
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mPowershellRemoting via wsmprovhost Detected !! \033[0m\n ", end='')
                            print(" [+] Command Line : ( %s ) \n " % Command_line_2 , end='')
                            print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                            print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                            print(" [+] description : ( %s ) \n " % description, end='')
                            print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                            print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass


                # Detect Network Connection via Compiled HTML
                if EventID[0]=="1":
                    try:
                        if len(User_Name[0][0])>0:
                            UserName_2 = User_Name[0][0].strip()
                            Process_id = Process_Id[0][0].strip()
                            Command_line_2 = Command_line[0][0].strip()
                            Fileversion = FileVersion[0][0].strip()
                            hashes = Hashes[0][0].strip()
                            description = Description[0][0].strip()
                            computer = Computer_Name[0].strip()
                            ParentProcessid = ParentProcessId[0][0].strip()
                            Parentimage = ParentImage[0][0].strip()
                            ParentCommandline = ParentCommandLine[0][0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        if len(User_Name[0][1])>0:
                            UserName_2 = User_Name[0][1]
                            Process_id = Process_Id[0][1].strip()
                            Command_line_2 = Command_line[0][1].strip()
                            Fileversion = FileVersion[0][1].strip()
                            hashes = Hashes[0][1].strip()
                            description = Description[0][1].strip()
                            computer = Computer_Name[1].strip()
                            ParentProcessid = ParentProcessId[0][1].strip()
                            Parentimage = ParentImage[0][1].strip()
                            ParentCommandline = ParentCommandLine[0][1].strip()
                            UtcTime1 = UtcTime[0][1].strip()


                        hashes = re.findall(r'(?i)(?<![a-z0-9])[a-f0-9]{32}(?![a-z0-9])', hashes)
                        MD5 = hashes[0].strip()
                        Command = html.unescape(Command_line_2)
                        ParentCommandline = html.unescape(ParentCommandline)


                        # Detect Network Connection via Compiled HTML
                        if "RunHTMLApplication" in Command and "hh.exe" in Parentimage and "chm" in ParentCommandline and "mshtml" in Command:
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mNetwork Connection via Compiled HTML Detected !! \033[0m\n ", end='')
                            print(" [+] Command Line : ( %s ) \n " % Command , end='')
                            print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                            print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                            print(" [+] description : ( %s ) \n " % description, end='')
                            print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                            print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass


                # Detect WinPwnage
                if EventID[0]=="1":
                    try:
                        if len(User_Name[0][0])>0:
                            UserName_2 = User_Name[0][0].strip()
                            Process_id = Process_Id[0][0].strip()
                            Command_line_2 = Command_line[0][0].strip()
                            Fileversion = FileVersion[0][0].strip()
                            hashes = Hashes[0][0].strip()
                            description = Description[0][0].strip()
                            computer = Computer_Name[0].strip()
                            ParentProcessid = ParentProcessId[0][0].strip()
                            Parentimage = ParentImage[0][0].strip()
                            ParentCommandline = ParentCommandLine[0][0].strip()
                            ImageName = ImageName2[0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        if len(User_Name[0][1])>0:
                            UserName_2 = User_Name[0][1]
                            Process_id = Process_Id[0][1].strip()
                            Command_line_2 = Command_line[0][1].strip()
                            Fileversion = FileVersion[0][1].strip()
                            hashes = Hashes[0][1].strip()
                            description = Description[0][1].strip()
                            computer = Computer_Name[1].strip()
                            ParentProcessid = ParentProcessId[0][1].strip()
                            Parentimage = ParentImage[0][1].strip()
                            ParentCommandline = ParentCommandLine[0][1].strip()
                            ImageName = ImageName2[1].strip()
                            UtcTime1 = UtcTime[0][1].strip()


                        hashes = re.findall(r'(?i)(?<![a-z0-9])[a-f0-9]{32}(?![a-z0-9])', hashes)
                        MD5 = hashes[0].strip()
                        Command = html.unescape(Command_line_2)
                        ParentCommandline = html.unescape(ParentCommandline)


                        # Detect WinPwnage python
                        if "cmd.exe" in Parentimage and "winpwnage.py" in Command_line_2 and "-u execute" in Command_line_2 and "python" in ImageName or "-u execute" in Command_line_2 and "python" in ImageName:
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mWinPwnage Detected !! \033[0m\n ", end='')
                            print(" [+] Command Line : ( %s ) \n " % Command , end='')
                            print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                            print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                            print(" [+] description : ( %s ) \n " % description, end='')
                            print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                            print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                            print("____________________________________________________\n")

                        # Detect WinPwnage ieframe.dll,OpenURL
                        if "rundll32.exe" in Command_line_2 and "ieframe.dll,OpenURL" in Command_line_2 and "rundll32.exe" in ImageName:
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mWinPwnage UAC BAYPASS by ieframe.dll,OpenURL Detected !! \033[0m\n ", end='')
                            print(" [+] Command Line : ( %s ) \n " % Command , end='')
                            print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                            print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                            print(" [+] description : ( %s ) \n " % description, end='')
                            print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                            print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                            print("____________________________________________________\n")

                        # Detect WinPwnage url.dll,OpenURL
                        if "rundll32.exe" in Command_line_2 and "url.dll,OpenURL" in Command_line_2 and "rundll32.exe" in ImageName:
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mWinPwnage UAC BAYPASS by url.dll,OpenURL Detected !! \033[0m\n ", end='')
                            print(" [+] Command Line : ( %s ) \n " % Command , end='')
                            print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                            print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                            print(" [+] description : ( %s ) \n " % description, end='')
                            print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                            print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                            print("____________________________________________________\n")


                        # Detect WinPwnage url.dll,FileProtocolHandler
                        if "rundll32.exe" in Command_line_2 and "url.dll,FileProtocolHandler" in Command_line_2 and "rundll32.exe" in ImageName:
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mWinPwnage UAC BAYPASS by url.dll,FileProtocolHandler Detected !! \033[0m\n ", end='')
                            print(" [+] Command Line : ( %s ) \n " % Command , end='')
                            print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                            print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                            print(" [+] description : ( %s ) \n " % description, end='')
                            print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                            print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                            print("____________________________________________________\n")

                        # Detect suspicious mshta.exe
                        if "mshta.exe" in ImageName: # TODO make it more strong, and check the rundll32 of it
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mSuspicios mshta.exe Detected !! \033[0m\n ", end='')
                            print(" [+] Command Line : ( %s ) \n " % Command , end='')
                            print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                            print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                            print(" [+] description : ( %s ) \n " % description, end='')
                            print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                            print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                            print("____________________________________________________\n")

                        # Detect suspicious winlogon.exe SMBV3 CVE-2020-0769
                        # For me: Comment on the detections later to make them more generic
                        if "winlogon.exe" in Parentimage and "cmd.exe" in ImageName.lower(): # TODO make it more strong, and check the rundll32 of it
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mSMBV3 CVE-2020-0769 !! \033[0m\n ", end='')
                            print(" [+] Command Line : ( %s ) \n " % Command , end='')
                            print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                            print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                            print(" [+] description : ( %s ) \n " % description, end='')
                            print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                            print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                            print("____________________________________________________\n")


                    except Exception as e:
                        pass


                # Detect Remote Service
                elif EventID[0]=="7045":
                    try:
                        if len(Channel[0])>0:
                            computer = Computer[0].strip()
                            channel = Channel[0].strip()
                            providerName = Provider_Name[0].strip()
                            eventSource_Name = EventSource_Name[0].strip()
                            serviceName = ServiceName[0][0].strip()
                            service_Image_Path = Service_Image_Path[0][0].strip()
                            serviceType = ServiceType[0][0].strip()
                            serviceStartType = ServiceStartType[0][0].strip()
                            acountName  = Service_Account_Name[0][0].strip()

                        # Detect Remote Service Start
                        if "Service Control Manager" in providerName and "Service Control Manager" in eventSource_Name and "remotesvc" in serviceName or "spoolsv" in serviceName or "spoolfool" and "user mode service" in serviceType:
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='') ### Fix Time
                            print(" [+] \033[0;31;47mRemote Service Start Detect !! \033[0m\n ", end='')
                            print(" [+] Computer : ( %s ) \n " % computer , end='')
                            print(" [+] channel : ( %s ) \n " % channel, end='')
                            print(" [+] Service Name: ( %s ) \n " % serviceName, end='')
                            print(" [+] Started Process : ( %s ) \n " % service_Image_Path, end='')
                            print(" [+] Service Type : ( %s ) \n " % serviceType, end='')
                            print(" [+] Account Name : ( %s ) \n " % acountName, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                # detect winrm code execution
                elif EventID[0]=="800":
                    try:
                        if len(Channel[0])>0:
                            computer = Computer[0].strip()
                            channel = Channel[0].strip()
                            PowershellUserId = PowershellUserId[0].strip()
                            PowershellHostApplication = PowershellHostApplication[0].strip()
                            CommandLine_powershell = CommandLine_powershell[0].strip()
                            PowerShellCommand = PowerShellCommand[0].strip()
                            ScriptName = ScriptName[0].strip()
                            PowerShellCommand = html.unescape(PowerShellCommand)
                            CommandLine_powershell = html.unescape(CommandLine_powershell)
                            PowerShellCommand_All = html.unescape(PowerShellCommand_All)
                            PowershellHostApplication = html.unescape(PowershellHostApplication)
                            PowerShellCommand = re.findall(r' (.*)', PowerShellCommand)
                            words = [r"Invoke-Mimikatz.ps1"]
                            results = [x for x in PowerShellCommand if all(re.search("\\b{}\\b".format(w), x) for w in words)]
                            results = results[0].strip()

                        # detect winrm code execution can you show where i have to work
                        if 1 == 1:
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='') ### Fix Time
                            print(" [+] \033[0;31;47mWinrm Detect !! \033[0m\n ", end='')# we need voice call yes
                            print(" [+] Computer : ( %s ) \n " % computer , end='')
                            print(" [+] channel : ( %s ) \n " % channel, end='')
                            print(" [+] user Name: ( %s ) \n " % PowershellUserId, end='')
                            #print(" [+] Command Name: ( %s ) \n " % Command_Name, end='')
                            print(" [+] PowerShell Script: ( %s ) \n " % ScriptName, end='')
                            print(" [+] PowerShell Mode: ( %s ) \n " % CommandLine_powershell, end='')
                            print(" [+] PowerShell Command: ( %s ) \n " % PowershellHostApplication, end='')
                            for element in PowerShellCommand:
                                if 'name="Arguments"' in element:
                                    print(" [+] PowerShell OutPut: \n ", end='')
                                    print(element.split('value')[1])
                            print("____________________________________________________\n")

                        # detect winrm code execution can you show where i have to work
                        if  results != None:
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='') ### Fix Time
                            print(" [+] \033[0;31;47mWinrm Invoke-Mimikatz Detect !! \033[0m\n ", end='')
                            print(" [+] Computer : ( %s ) \n " % computer , end='')
                            print(" [+] channel : ( %s ) \n " % channel, end='')
                            print(" [+] user Name: ( %s ) \n " % PowershellUserId, end='')
                            print(" [+] PowerShell Command: ( %s ) \n " % PowershellHostApplication, end='')
                            print(" [+] PowerShell Script: ( %s ) \n " % ScriptName, end='')
                            print(" [+] Mimikatz Command: ( %s ) \n " % results, end='')
                            print(bcolor.RED + " [+] PowerShell OutPut:\n ", end='')
                            for element in PowerShellCommand:
                                print(bcolor.CBLUE + element, end='\n')
                            print("____________________________________________________\n")

                    except Exception as e:
                        #print(e)
                        pass

                # Detect Remote Task Creation
                elif EventID[0]=="5145":
                    try:
                        if len(Account_Name[0])>0:
                            computer = Computer[0].strip()
                            channel = Channel[0].strip()
                            accountName = Account_Name[0][0].strip()
                            accountDomain = Account_Domain[0][0].strip()
                            SourceIP = Source_IP[0][0].strip()
                            SourcePort = Source_Port[0][0].strip()
                            ShareName  = ShareName[0][0].strip()
                            ShareLocalPath = ShareLocalPath[0][0].strip()
                            RelativeTargetName = RelativeTargetName[0][0].strip()


                        if len(Account_Name[0][1])>0:
                            computer = Computer[1].strip()
                            channel = Channel[1].strip()
                            accountName = Account_Name[0][1].strip()
                            accountDomain = Account_Domain[0][1].strip()
                            SourceIP = Source_IP[0][1].strip()
                            SourcePort = Source_Port[0][1].strip()
                            ShareName  = ShareName[0][1].strip()
                            ShareLocalPath = ShareLocalPath[0][1].strip()
                            RelativeTargetName = RelativeTargetName[0][1].strip()

                        # Detect Remote Task Creation via ATSVC named pipe
                        if "atsvc" in RelativeTargetName:
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='') ### Fix Time
                            print(" [+] \033[0;31;47mSuspicios ATSVC Detect !! \033[0m\n ", end='')
                            print(" [+] Computer : ( %s ) \n " % computer , end='')
                            print(" [+] channel : ( %s ) \n " % channel, end='')
                            print(" [+] User Name : ( %s ) \n " % accountName, end='')
                            print(" [+] Account Domain Name : ( %s ) \n " % accountDomain, end='')
                            print(" [+] Source IP : ( %s ) \n " % SourceIP, end='')
                            print(" [+] Source Port : ( %s ) \n " % SourcePort, end='')
                            print(" [+] Share Name : ( %s ) \n " % ShareName, end='')
                            print(" [+] Local Share Path : ( %s ) \n " % ShareLocalPath, end='')
                            print(" [+] File Path : ( %s ) \n " % RelativeTargetName, end='')
                            print("____________________________________________________\n")

                            PASS1 = True


                    except Exception as e:
                        pass

                    # Detect Remote Task Creation via ATSVC named pipe
                elif EventID[0] == "4698" or EventID[0] == "4699" and PASS1 == True:
                    Task_Content = str(Task_Content)
                    Task_arguments = re.findall(r'Arguments(.*)/Arguments', Task_Content)
                    Task_Command = re.findall(r'Command(.*)/Command', Task_Content)
                    try:
                        if len(Account_Name[0])>0:
                            computer = Computer[0].strip()
                            channel = Channel[0].strip()
                            accountName = Account_Name[0][0].strip()
                            Task_Name = Task_Name[0][0].strip()
                            Task_arguments = Task_arguments[0].strip()
                            Task_Command = Task_Command[0].strip()


                        if len(Account_Name[0][1])>0:
                            computer = Computer[1].strip()
                            channel = Channel[1].strip()
                            accountName = Account_Name[0][1].strip()
                            Task_Name = Task_Name[0][1].strip()
                            Task_arguments = Task_arguments[1].strip()
                            Task_Command = Task_Command[1].strip()


                        print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='') ### Fix Time
                        print(" [+] \033[0;31;47mRemote Task Creation via ATSVC named pipe Detect !! \033[0m\n ", end='')
                        print(" [+] Computer : ( %s ) \n " % computer , end='')
                        print(" [+] channel : ( %s ) \n " % channel, end='')
                        print(" [+] User Name : ( %s ) \n " % accountName, end='')
                        print(" [+] Task Name : ( %s ) \n " % Task_Name, end='')
                        print(" [+] Task Command : ( %s ) \n " % Task_Command, end='')
                        print(" [+] Task Command Arguments : ( %s ) \n " % Task_arguments, end='')
                        print("____________________________________________________\n")
                    except Exception as e:
                        pass

                # Kerberos AS-REP Attack Detect
                if EventID[0] == "4768":
                    try:
                        if len(TargetAccount_Name[0])>0:
                            computer = Computer[0].strip()
                            channel = Channel[0].strip()
                            TargetAccount_Name=TargetAccount_Name[0][0].strip()
                            source_ip=Source_IP[0][0].strip()
                            serviceName = ServiceName[0][0].strip()
                            target_account_domain=Target_Account_Domain[0][0].strip()
                            Source_Port = Source_Port[0][0].strip()

                        if serviceName == "krbtgt":
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='') ### Fix Time
                            print("[+] \033[0;31;47mKerberos AS-REP Attack Detected ! \033[0m\n ", end='')
                            print("[+] User Name : ( %s ) \n" % TargetAccount_Name, end='')
                            print(" [+] Computer : ( %s ) \n" % computer, end='')
                            print(" [+] Channel : ( %s ) \n" % channel, end='')
                            print(" [+] Service Name : ( %s ) \n" % serviceName, end='')
                            print(" [+] Domain Name : ( %s ) \n" % target_account_domain, end='')
                            print(" [+] Source IP : ( %s ) \n" % source_ip, end='')
                            print(" [+] Source Port : ( %s ) \n" % Source_Port, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                # PowerShell Download Detect
                if EventID[0] == "4104": # TODO Base64 command Detect
                    try:
                        if len(Computer[0])>0:
                            computer = Computer[0].strip()
                            channel = Channel[0].strip()
                            PowerShell_Command = PowerShell_Command[0].strip()
                            Command = html.unescape(PowerShell_Command)

                        #check if command is encoded
                        if isBase64(Command) == False:
                            IsEncoded = False
                        else:
                            CommandEncoded = isBase64(Command)
                            print(CommandEncoded)
                            #check if  download start
                        if IsEncoded == False and "IEX(New-Object Net.WebClient).downloadString" in PowerShell_Command or "(New-Object Net.WebClient)" in PowerShell_Command or "[System.NET.WebRequest]" in PowerShell_Command:
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='') ### Fix Time
                            print("[+] \033[0;31;47mPowerShell Download Detect ! \033[0m\n ", end='')
                            print("[+] PowerShell Command : ( %s ) \n" % Command, end='')
                            print(" [+] Computer : ( %s ) \n" % computer, end='')
                            print(" [+] Channel : ( %s ) \n" % channel, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                #Detect suspicious process Runing PowerShell Command
                if EventID[0]=="4688":
                    try:
                        if len(Account_Name[0])>0:
                            computer = Account_Domain[0][0].strip()
                            accountName = Account_Name[0][0].strip()
                            ProcessId = Process_Id[0][0].strip()
                            commandLine = Command_line[0][0].strip()
                            Process_Name = New_Process_Name[0].strip()
                            TokenElevationType = TokenElevationType[0].strip()
                            Command_unescape = html.unescape(commandLine)

                        Base64Finder = re.findall(r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)', Command_unescape)

                        if "powershell.exe" in Command_unescape.lower() or "powershell" in Command_unescape.lower() and "%%1936" in TokenElevationType: #and "cmd.exe" in Process_Name.lower():
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mFound Suspicios Process Runing PowerShell Command On Full Privilege \033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] User Name : ( %s ) \n " % accountName, end='')
                            print(" [+] Process ID : ( %s ) \n " % ProcessId, end='')
                            print(" [+] Process Name : ( %s ) \n " % Process_Name, end='')
                            print(" [+] Process Command Line : ( %s ) \n " % Command_unescape, end='')
                            if len(Base64Finder[0])>5:
                               print(" [+] Base64 Command : ( %s ) \n " % Base64Finder[0], end='')
                            print("____________________________________________________\n")
                        # PipeName
                        pipe = r'\.\pipe'
                        # SMBEXEC
                        SMBEXEC = r'cmd.exe /q /c echo cd'
                        SMBEXEC2 = r'\\127.0.0.1\c$'
                        wmiexec = r'cmd.exe /q /c'
                        wmiexec2 = r'1> \\127.0.0.1\admin$\__'
                        wmiexec3 = r'2>&1'
                        msiexec = r'msiexec.exe /i Site24x7WindowsAgent.msi EDITA1=asdasd /qn'
                        msiexec2 = r'comsvcs.dll MiniDump  C:\windows\temp\logctl.zip full'
                        msiexec3 = r'windows\temp\ekern.exe'
                        #Detect Privilege esclation "GetSystem"
                        if "cmd.exe /c echo" in Command_unescape.lower() and "%%1936" in TokenElevationType and "cmd.exe" in Process_Name.lower() and pipe in Command_unescape.lower():
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mGetSystem Detect By metasploit & Cobalt Strike & Empire & PoshC2\033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] User Name : ( %s ) \n " % accountName, end='')
                            print(" [+] Process ID : ( %s ) \n " % ProcessId, end='')
                            print(" [+] Process Name : ( %s ) \n " % Process_Name, end='')
                            print(" [+] Process Command Line : ( %s ) \n " % Command_unescape, end='')
                            print("____________________________________________________\n")
                        #Detect Cmd.exe command
                        if "cmd.exe" in Command_unescape.lower() and "%%1936" in TokenElevationType and "cmd.exe" in Process_Name.lower():
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mFound Suspicios Process Runing cmd Command On Full Privilege\033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] User Name : ( %s ) \n " % accountName, end='')
                            print(" [+] Process ID : ( %s ) \n " % ProcessId, end='')
                            print(" [+] Process Name : ( %s ) \n " % Process_Name, end='')
                            print(" [+] Process Command Line : ( %s ) \n " % Command_unescape, end='')
                            print("____________________________________________________\n")

                        #Detect SMBEXEC
                        if SMBEXEC in Command_unescape.lower() and SMBEXEC2 in Command_unescape.lower() and wmiexec3 in Command_unescape.lower() and "%%1936" in TokenElevationType:
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mSMBEXEC Detected !!\033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] User Name : ( %s ) \n " % accountName, end='')
                            print(" [+] Process ID : ( %s ) \n " % ProcessId, end='')
                            print(" [+] Process Name : ( %s ) \n " % Process_Name, end='')
                            print(" [+] Process Command Line : ( %s ) \n " % Command_unescape, end='')
                            print("____________________________________________________\n")

                        #Detect wmiexec variation
                        if wmiexec in Command_unescape.lower() and wmiexec2 in Command_unescape.lower() and "%%1936" in TokenElevationType:
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mWMIEXEC Detected !!\033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] User Name : ( %s ) \n " % accountName, end='')
                            print(" [+] Process ID : ( %s ) \n " % ProcessId, end='')
                            print(" [+] Process Name : ( %s ) \n " % Process_Name, end='')
                            print(" [+] Process Command Line : ( %s ) \n " % Command_unescape, end='')
                            print("____________________________________________________\n")

                        #Detect CVE-2021-44077
                        if msiexec in Command_unescape:
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mCVE-2021-44077 first stage Detected !!\033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] User Name : ( %s ) \n " % accountName, end='')
                            print(" [+] Process ID : ( %s ) \n " % ProcessId, end='')
                            print(" [+] Process Name : ( %s ) \n " % Process_Name, end='')
                            print(" [+] Process Command Line : ( %s ) \n " % Command_unescape, end='')
                            print("____________________________________________________\n")

                        #Detect CVE-2021-44077 second
                        if msiexec2 in Command_unescape:
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mCVE-2021-44077 2th stage Detected !!\033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] User Name : ( %s ) \n " % accountName, end='')
                            print(" [+] Process ID : ( %s ) \n " % ProcessId, end='')
                            print(" [+] Process Name : ( %s ) \n " % Process_Name, end='')
                            print(" [+] Process Command Line : ( %s ) \n " % Command_unescape, end='')
                            print("____________________________________________________\n")

                        #Detect CVE-2021-44077 3th
                        if msiexec3 in Command_unescape:
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mCVE-2021-44077 3th stage Detected !!\033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] User Name : ( %s ) \n " % accountName, end='')
                            print(" [+] Process ID : ( %s ) \n " % ProcessId, end='')
                            print(" [+] Process Name : ( %s ) \n " % Process_Name, end='')
                            print(" [+] Process Command Line : ( %s ) \n " % Command_unescape, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                #Detect Privilege esclation "GetSystem"
                if EventID[0]=="7045":
                    try:
                        if len(Account_Name[0])>0:
                            computer = Account_Domain[0][0].strip()
                            accountName = Account_Name[0][0].strip()
                            ProcessId = Process_Id[0][0].strip()
                            commandLine = Command_line[0][0].strip()
                            Process_Name = New_Process_Name[0].strip()
                            TokenElevationType = TokenElevationType[0].strip()
                            Command_unescape = html.unescape(commandLine)

                        # PipeName
                        pipe = r'\.\pipe'
                        #Detect Privilege esclation "GetSystem"
                        if "cmd.exe /c echo" in Command_unescape.lower() and "%%1936" in TokenElevationType and "cmd.exe" in Process_Name.lower() and pipe in Command_unescape.lower():
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mGetSystem Detect By metasploit & Cobalt Strike & Empire & PoshC2\033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] User Name : ( %s ) \n " % accountName, end='')
                            print(" [+] Process ID : ( %s ) \n " % ProcessId, end='')
                            print(" [+] Process Name : ( %s ) \n " % Process_Name, end='')
                            print(" [+] Process Command Line : ( %s ) \n " % Command_unescape, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                #Detect PsExec execution
                if EventID[0]=="1":
                    try:
                        if len(User_Name[0][0])>0:
                            UserName_2 = User_Name[0][0].strip()
                            Process_id = Process_Id[0][0].strip()
                            Command_line_2 = Command_line[0][0].strip()
                            Fileversion = FileVersion[0][0].strip()
                            hashes = Hashes[0][0].strip()
                            description = Description[0][0].strip()
                            computer = Computer_Name[0].strip()
                            ParentProcessid = ParentProcessId[0][0].strip()
                            Parentimage = ParentImage[0][0].strip()
                            ParentCommandline = ParentCommandLine[0][0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        if len(User_Name[0][1])>0:
                            UserName_2 = User_Name[0][1]
                            Process_id = Process_Id[0][1].strip()
                            Command_line_2 = Command_line[0][1].strip()
                            Fileversion = FileVersion[0][1].strip()
                            hashes = Hashes[0][1].strip()
                            description = Description[0][1].strip()
                            computer = Computer_Name[1].strip()
                            ParentProcessid = ParentProcessId[0][1].strip()
                            Parentimage = ParentImage[0][1].strip()
                            ParentCommandline = ParentCommandLine[0][1].strip()
                            UtcTime1 = UtcTime[0][1].strip()


                        hashes = re.findall(r'(?i)(?<![a-z0-9])[a-f0-9]{32}(?![a-z0-9])', hashes)
                        MD5 = hashes[0].strip()
                        Command_unescape = html.unescape(Command_line_2)

                        # Detect PsExec
                        if "psexesvc.exe" in Parentimage.lower() or "psexesvc.exe" in ParentCommandline.lower():
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mPsexesvc execution Detected !! \033[0m\n ", end='')
                            print(" [+] Command Line : ( %s ) \n " % Command_unescape , end='')
                            print(" [+] Parent Process Command Line : ( %s ) \n " % ParentCommandline, end='')
                            print(" [+] User Name : ( %s ) \n " % UserName_2, end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] File Info : ( %s ) \n " % Fileversion, end='')
                            print(" [+] description : ( %s ) \n " % description, end='')
                            print(" [+] Process MD5 : ( %s ) \n " % MD5, end='')
                            print(" [+] ParentImage Path : ( %s ) \n " % Parentimage, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] Parent Process ID : ( %s ) \n " % ParentProcessid, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                #Detect PsExec Pipe Connection
                if EventID[0]=="18":
                    try:
                        if len(Computer_Name[0])>0:
                            computer = Computer_Name[0].strip()
                            Process_id = Process_Id[0][0].strip()
                            PipeName2 = PipeName2[0].strip()
                            ImageName2 = ImageName2[0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        # Detect PsExec Pipe Connection
                        if "\psexesvc" in PipeName2.lower() and "stderr" in PipeName2.lower() or "\psexesvc" in PipeName2.lower() and "stdin" in PipeName2.lower() or "\psexesvc" in PipeName2.lower() and "stdout" in PipeName2.lower():
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mPsExec Pipe Connection Detected !! \033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] Image Name : ( %s ) \n " % ImageName2, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] PipeName : ( %s ) \n " % PipeName2, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                #Detect PsExec Pipe Creation
                if EventID[0]=="17":
                    try:
                        if len(Computer_Name[0])>0:
                            computer = Computer_Name[0].strip()
                            Process_id = Process_Id[0][0].strip()
                            PipeName2 = PipeName2[0].strip()
                            ImageName2 = ImageName2[0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        # Detect PsExec Pipe Creation
                        if "\psexesvc" in PipeName2.lower() and "stderr" in PipeName2.lower() or "\psexesvc" in PipeName2.lower() and "stdin" in PipeName2.lower() or "\psexesvc" in PipeName2.lower() and "stdout" in PipeName2.lower():
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mPsExec Pipe Creation Detected !! \033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] Image Name : ( %s ) \n " % ImageName2, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] PipeName : ( %s ) \n " % PipeName2, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                #Detect PsExec Pipe Creation
                if EventID[0]=="17":
                    try:
                        if len(Computer_Name[0])>0:
                            computer = Computer_Name[0].strip()
                            Process_id = Process_Id[0][0].strip()
                            PipeName2 = PipeName2[0].strip()
                            ImageName2 = ImageName2[0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        # Detect PsExec Pipe Creation
                        if "\psexesvc" in PipeName2.lower() and "stderr" in PipeName2.lower() or "\psexesvc" in PipeName2.lower() and "stdin" in PipeName2.lower() or "\psexesvc" in PipeName2.lower() and "stdout" in PipeName2.lower():
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mPsExec Pipe Creation Detected !! \033[0m\n ", end='')
                            print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                            print(" [+] Image Name : ( %s ) \n " % ImageName2, end='')
                            print(" [+] Process ID : ( %s ) \n " % Process_id, end='')
                            print(" [+] PipeName : ( %s ) \n " % PipeName2, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                #Detect SMBV3 CVE-2020-0769
                if EventID[0]=="10":
                    try:
                        if len(SourceImage[0])>0:
                            SourceProcessId = SourceProcessId[0].strip()
                            SourceImage = SourceImage[0].strip()
                            TargetProcessId = TargetProcessId[0].strip()
                            TargetImage = TargetImage[0].strip()
                            GrantedAccess = GrantedAccess[0].strip()
                            CallTrace = CallTrace[0].strip()
                            UtcTime1 = UtcTime[0][0].strip()

                        # Detect SMBV3 CVE-2020-0769
                        if "0x1fffff" in GrantedAccess and "winlogon.exe" in TargetImage and "ntdll.dll" in CallTrace and "KERNELBASE.dll" in CallTrace:
                            print("\n__________ " + UtcTime1 + " __________ \n\n ", end='')
                            print(" [+] \033[0;31;47mSTART OF CVE-2020-0769 Detected !! \033[0m\n ", end='')
                            print(" [+] Source Process Id : ( %s ) \n " % SourceProcessId, end='')
                            print(" [+] Source Image : ( %s ) \n " % SourceImage, end='')
                            print(" [+] Target Process Id : ( %s ) \n " % TargetProcessId, end='')
                            print(" [+] Target Image : ( %s ) \n " % TargetImage, end='')
                            print(" [+] Granted Access : ( %s ) \n " % GrantedAccess, end='')
                            print(" [+] CallTrace : ( %s ) \n " % CallTrace, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                #detect pass the hash
                if EventID[0] == "4625" or EventID[0] == "4624":
                    try:
                        #print(Logon_Events)
                        if len(Account_Name[0][0])>0:
                            logon_type=Logon_Type[0][0].strip()
                            user=Account_Name[0][0].strip()
                            target_account_name=TargetAccount_Name[0][0].strip()
                            logon_process=Logon_Process[0][0].strip()
                            key_length=Key_Length[0][0].strip()
                            target_account_domain=Target_Account_Domain[0][0].strip()
                            source_ip=Source_IP[0][0].strip()
                            workstation_name=Workstation_Name[0][0].strip()
                        if len(Account_Name[0][1])>0:
                            logon_type=Logon_Type[0][1].strip()
                            target_account_name=TargetAccount_Name[0][1].strip()
                            logon_process=Logon_Process[0][1].strip()
                            key_length=Key_Length[0][1].strip()
                            target_account_domain=Target_Account_Domain[0][1].strip()
                            source_ip=Source_IP[0][1].strip()
                            workstation_name=Workstation_Name[0][1].strip()

                        if logon_type == "3" or logon_type == "9" and target_account_name != "ANONYMOUS LOGON" and key_length == "0":
                            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='') ### Fix Time
                            print("[+] \033[0;31;47mPass The Hash Detected \033[0m\n ", end='')
                            print("[+] User Name : ( %s ) \n" % target_account_name, end='')
                            print(" [+] Computer : ( %s ) \n" % Computer[0].strip(), end='')
                            print(" [+] Channel : ( %s ) \n" % Channel[0].strip(), end='')
                            print(" [+] Account Domain : ( %s ) \n" % target_account_domain, end='')
                            print(" [+] Logon Type : ( %s ) \n" % logon_type, end='')
                            print(" [+] Logon Process : ( %s ) \n" % logon_process, end='')
                            print(" [+] Source IP : ( %s ) \n" % source_ip, end='')
                            print(" [+] Workstation Name : ( %s ) \n" % workstation_name, end='')
                            print("____________________________________________________\n")

                    except Exception as e:
                        pass

                #Start Of Detecting cve-2021-42287
                if EventID[0]=="4741": #+ EventID[0]=="4673" + EventID[0]=="4742" + EventID[0]=="4781" + EventID[0]=="4768" + EventID[0]=="4781" and EventID[0]=="4769":
                    try:
                        if len(Account_Name[0])>0:
                            ServicePrincipalNames = ServicePrincipalNames[0].strip()

                        if "-" in ServicePrincipalNames:
                            checker("ATTACK_REPLAY_CHECK")

                    except Exception as e:
                        pass


                # Detecting Sam Account name changed to domain controller name
                if EventID[0]=="4742":
                    try:
                        if len(Account_Name[0])>0:
                            SamAccountName = SamAccountName[0].strip()
                            UserName = TargetAccount_Name[0][0].strip()

                        if "-" not in SamAccountName:
                            checker("SAM_ACCOUNT_NAME_CHECK")

                    except Exception as e:
                        pass

                # Verify Sam Account name changed to domain controller name
                if EventID[0]=="4781":
                    try:
                        if len(Account_Name[0])>0:
                            NewTargetUserName = NewTargetUserName[0].strip()
                            computer = Computer_Name[0].strip()


                        if NewTargetUserName in computer:
                             checker("New_Target_User_Name_Check")

                    except Exception as e:
                        pass

                # Kerberos AS-REP Attack Detect
                if EventID[0] == "4768":
                    try:
                        if len(TargetAccount_Name[0])>0:
                            computer = Computer[0].strip()

                        if serviceName == "krbtgt":
                            checker("REQUEST_TGT_CHECK")

                    except Exception as e:
                        pass

################ end of CVE-2021-42278 DETECTION


                #detect PasswordSpray Attack
                if EventID[0] == "4648":
                    try:
                        if len(Account_Name[0][0])>0:
                            user=Account_Name[0][0].strip()
                            target_account_name=TargetAccount_Name[0][0].strip()
                            target_account_domain=Target_Account_Domain[0][0].strip()
                            source_ip=Source_IP[0][0].strip()
                        if len(Account_Name[0][1])>0:
                            target_account_name=TargetAccount_Name[0][1].strip()
                            target_account_domain=Target_Account_Domain[0][1].strip()
                            source_ip=Source_IP[0][1].strip()

                        #For Defrinceation
                        user_list.append(user)
                        user_list_2.append(user)
                        sourceIp_list.append(source_ip)
                        sourceIp_list_2.append(source_ip)

                    except Exception as e:
                        pass


        # FULL CVE-2021-42278 DETECTION
        if "True" in REQUEST_TGT_CHECK_list and "True" in New_Target_User_Name_Check_list and "True" in SAM_ACCOUNT_NAME_CHECK_list and "True" in ATTACK_REPLAY_CHECK_list:
            parser = PyEvtxParser(file)
            for record in parser.records():
                EventID2 = EventID_rex.findall(record['data'])
                NewTargetUserName = NewTargetUserName_rex.findall(record['data'])
                OldTargetUserName = OldTargetUserName_rex.findall(record['data'])
                Computer_Name = Computer_Name_rex.findall(record['data'])
                Target_Account_Domain=Account_Domain_Target_rex.findall(record['data'])
                Account_Name = AccountName_rex.findall(record['data'])
                if len(EventID2) > 0:
                    if EventID2[0] == "4781":
                        try:
                            if len(Account_Name[0])>0:
                                NewTargetUserName = NewTargetUserName[0].strip()
                                computer = Computer_Name[0].strip()
                                OldTargetUserName = OldTargetUserName[0].strip()
                                target_account_domain = Target_Account_Domain[0][0].strip()
                                accountName = Account_Name[0][0].strip()

                            if OldTargetUserName in computer: #and "True" in REQUEST_TGT_CHECK_list and "True" in New_Target_User_Name_Check_list:# and "True" in SAM_ACCOUNT_NAME_CHECK_list and "True" in ATTACK_REPLAY_CHECK_list:
                                print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='')
                                print(" [+] \033[0;31;47mCVE-2021-42287 and CVE-2021-42278 DETCTED !!\033[0m\n ", end='')
                                print(" [+] Computer Name : ( %s ) \n " % computer, end='')
                                print(" [+] User Name : ( %s ) \n " % accountName, end='')
                                print(" [+] New User Name : ( %s ) \n " % NewTargetUserName, end='')
                                print(" [+] Old User Name : ( %s ) \n " % OldTargetUserName, end='')
                                print(" [+] Domain Name : ( %s ) \n " % target_account_domain, end='')
                                print("____________________________________________________\n")


                        except Exception as e:
                            pass
    #### END

    # For Defrinceation and Detect the attack
    if range(len(user_list)) == range(len(user_list_2)) and range(len(sourceIp_list)) == range(len(sourceIp_list_2)):
        SprayUserDetector = 0
        for x in range(len(user_list)):
            if user_list[x] == user_list_2[x]:
                SprayUserDetector += 1
        if SprayUserDetector >= 10:
            print("\n__________ " + record["timestamp"] + " __________ \n\n ", end='') ### Fix Time
            print("[+] \033[0;31;47mPassword Spray Detected!! \033[0m\n ", end='')
            print("[+] Attacker User Name : ( %s ) \n" % user, end='')
            print(" [+] Account Domain : ( %s ) \n" % target_account_domain, end='')
            print(" [+] Source IP : ( %s ) \n" % source_ip, end='')
            print(" [+] Number Of Spray : ( %s ) \n" % SprayUserDetector, end='')
            print("____________________________________________________\n")

    #### print the final report of the SIGMA scanning
    try:
        for RuleName in MatchedRulesAgainstLogs.keys():
            print(f"[!] Rule Name: {RuleName}", end="\t\t\t\t\t\t\n")
            print(f"  [-] Potential False-Positives: {MatchedRulesAgainstLogs[RuleName]['falsepositives']}")
            for Event in MatchedRulesAgainstLogs[RuleName]["Events"]:
                print("\n__________ " + str(Event["Timestamp"]) + " __________ \n\n ")
                if len(Event["EventID"]) != 0:
                    print("     [*] EventID: " + str(Event["EventID"]))
                if len(Event["Computer"]) != 0:
                    print("     [*] Computer: " + str(Event["Computer"]))
                if len(Event["Image"]) != 0:
                    print("     [*] Process Image: " + str(Event["Image"]))
                if len(Event["CommandLine"]) != 0:
                    print("     [*] CommandLine: " + str(Event["CommandLine"]))
                if len(Event["ParentImage"]) != 0:
                    print("     [*] Parent Process Image: " + str(Event["ParentImage"]))
                if len(Event["ParentCommandLine"]) != 0:
                    print("     [*] Parent Process CommandLine: " + str(Event["ParentCommandLine"]))
                if len(Event["User"]) != 0:
                    print("     [*] User: " + str(Event["User"]))
                if len(Event["UserName"]) != 0:
                    print("     [*] UserName: " + str(Event["UserName"]))
                if len(Event["SourceIp"]) != 0:
                    print("     [*] Source IP Address: " + str(Event["SourceIp"]) + ":" + str(Event["SourcePort"]))
                if len(Event["DestinationIp"]) != 0:
                    print("     [*] Destionation IP Address: " + str(Event["DestinationIp"]) + ":" + str(Event["DestinationPort"]))
                if len(Event["OriginalFileName"]) != 0:
                    print("     [*] Original File Name: " + str(Event["OriginalFileName"]))
                if len(Event["SubjectUserName"]) != 0:
                    print("     [*] Subject User Name: " + str(Event["SubjectUserName"]))
                if len(Event["TargetUserName"]) != 0:
                    print("     [*] Target User Name: " + str(Event["TargetUserName"]))
                if len(Event["SubjectDomainName"]) != 0:
                    print("     [*] Subject Domain Name: " + str(Event["SubjectDomainName"]))
                print("____________________________________________________\n")
                print("____________________________________________________\n")
    except Exception as ERROR:
        print(ERROR)
        print("Error printing the Matched Rules")

    # Print the list of all rules that match. Each rule key contains all corresponding events that matched
    # print(MatchedRulesAgainstLogs.keys())
    # You can use this variable MatchedRulesAgainstLogs any way you want

#========================================== END OF SPRAY Detect


# Parsing Evtx File
def parse_evtx(evtx_list):
    try:
        # count = 0
        # record_sum = 0
        # evtx = None
        # for evtx_file in evtx_list:
        #     if evtx is None:
        #         with open(evtx_file, "rb") as fb:
        #             fb_data = fb.read(8)
        #             if fb_data != EVTX_HEADER:
        #                 sys.exit("[!] This file is not EVTX format {0}.".format(evtx_file))

        #         with open(evtx_file, "rb") as evtx:
        #             parser = PyEvtxParser(evtx)
        #             records = list(parser.records())
        #             record_sum += len(records)

        # print("[+] Last record number is {0}.".format(record_sum))

        # # Parse Event log
        # print("[+] Start parsing the EVTX file.")

        # for evtx_file in evtx_list:
        #     print("[+] Parse the EVTX file {0}.".format(evtx_file))

        #     for record, err in xml_records(evtx_file):
        #         if err is not None:
        #             continue
        #         count += 1

        #         if evtx_file == evtx_file:
        #             sys.stdout.write("\r[+] Now loading {0} records.".format(count))
        #             sys.stdout.flush()

        detect_events_security_log(evtx_list)
    except Exception as e:
        print("Exception Occurred")
        print(e)
        print("Opps !")
        print("Enter a Correct Path")


#def sigmahq():
    ## we need to convert the .yml to varible
    ## store all .yml files values to them varible
    ## compare the .yml varible values with .xml varible values
    ## prin tthe result with .yml tag value.

banner = '''

████████╗██╗░░██╗██████╗░███████╗░█████╗░████████╗  
╚══██╔══╝██║░░██║██╔══██╗██╔════╝██╔══██╗╚══██╔══╝  
░░░██║░░░███████║██████╔╝█████╗░░███████║░░░██║░░░  
░░░██║░░░██╔══██║██╔══██╗██╔══╝░░██╔══██║░░░██║░░░  
░░░██║░░░██║░░██║██║░░██║███████╗██║░░██║░░░██║░░░  
░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░╚═╝░░░  

░░░░░░░░░██╗░░██╗░█████╗░██╗░░░██╗███╗░░██╗██████╗░
░░░░░░░░░██║░░██║██╔══██╗██║░░░██║████╗░██║██╔══██╗
░░░░░░░░░███████║██║░░██║██║░░░██║██╔██╗██║██║░░██║
░░░░░░░░░██╔══██║██║░░██║██║░░░██║██║╚████║██║░░██║
██╗██╗██╗██║░░██║╚█████╔╝╚██████╔╝██║░╚███║██████╔╝
╚═╝╚═╝╚═╝╚═╝░░╚═╝░╚════╝░░╚═════╝░╚═╝░░╚══╝╚═════╝░
'''
#parse_evtx(evtx_list2)
def title():
    print(banner)
    print('+------------------------------------------')
    print('+  \033[34mThis Tool Made BY: Mohamed Alzhrani // http://github.com/MazX0p      \033[0m')
    print('+  \033[34m-\033[0m')
    print('+  \033[36m-\033[0m')
    print('+------------------------------------------')

class bcolor:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CBLACK = '\33[30m'
    CRED = '\33[31m'
    RED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    BLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'


def LOGO():
    bcolor_random = [bcolor.CBLUE, bcolor.CVIOLET, bcolor.CWHITE, bcolor.OKBLUE, bcolor.CGREEN, bcolor.WARNING,
                    bcolor.CRED, bcolor.CBEIGE]
    random.shuffle(bcolor_random)
    x = bcolor_random[0] + """

████████╗██╗░░██╗██████╗░███████╗░█████╗░████████╗  ██╗░░██╗░█████╗░██╗░░░██╗███╗░░██╗██████╗░
╚══██╔══╝██║░░██║██╔══██╗██╔════╝██╔══██╗╚══██╔══╝  ██║░░██║██╔══██╗██║░░░██║████╗░██║██╔══██╗
░░░██║░░░███████║██████╔╝█████╗░░███████║░░░██║░░░  ███████║██║░░██║██║░░░██║██╔██╗██║██║░░██║
░░░██║░░░██╔══██║██╔══██╗██╔══╝░░██╔══██║░░░██║░░░  ██╔══██║██║░░██║██║░░░██║██║╚████║██║░░██║
░░░██║░░░██║░░██║██║░░██║███████╗██║░░██║░░░██║░░░  ██║░░██║╚█████╔╝╚██████╔╝██║░╚███║██████╔╝
░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░╚═╝░░░  ╚═╝░░╚═╝░╚════╝░░╚═════╝░╚═╝░░╚══╝╚═════╝░

\n"""

    for c in x:
        print(c, end='')
        sys.stdout.flush()
        sleep(0.0004)
    y = "\t||||||||||||||||||||||||||||||||||||||||||||||||||||||\n"
    for c in y:
        print(bcolor.CRED + c, end='')
        sys.stdout.flush()
        sleep(0.0005)
    y = "\t||                   THREAT HOUND                   ||\n"
    for c in y:
        print(bcolor.CWHITE + c, end='')
        sys.stdout.flush()
        sleep(0.0005)
    x = "\t||                                                  ||\n"
    for c in x:
        print(bcolor.CWHITE + c, end='')
        sys.stdout.flush()
        sleep(0.0005)
    z = "\t||        This Tool Made BY: Mohamed Alzhrani       ||\n"
    for c in z:
        print(bcolor.CWHITE + c, end='')
        sys.stdout.flush()
        sleep(0.0005)
    y = "\t||||||||||||||||||||||||||||||||||||||||||||||||||||||\n"
    for c in y:
        print(bcolor.CRED + c, end='')
        sys.stdout.flush()
        sleep(0.0005)
    y = "\t||              http://github.com/MazX0p            ||\n"
    for c in y:
        print(bcolor.CWHITE + c, end='')
        sys.stdout.flush()
        sleep(0.0005)

    y = "\t||||||||||||||||||||||||||||||||||||||||||||||||||||||\n"
    for c in y:
        print(bcolor.CRED + c, end='')
        sys.stdout.flush()
        sleep(0.0065)


if __name__ == '__main__':
    LOGO()
    sigma_manager.CheckUpdate()
    file = str(input("\033[35mEnter EVTX File With Full Path \nFile:    >>> \033[0m"))
    evtx_list.append(file)
    parse_evtx(evtx_list)
