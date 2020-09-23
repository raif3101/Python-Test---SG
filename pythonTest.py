""""""""""""""""""
Author: Fatima-ezzahra Rais / Fzrs.rais@gmail.com

""""""""""""""""""


import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
from string import Template
try:
	import urllib.request as urllib2
except ImportError:
	import urllib2
import platform



def check_java_exist():
	java = subprocess.Popen(["Java -version"],
	stdout = subprocess.PIPE,
	stderr = subprocess.STDOUT)
	out, error = java.communicate()
	if error:
		print('Java is not installed')
	return error
    
    
def check_java_version():
	java_version = subprocess.check_output(["Java -version"],
			   stderr=subprocess.STDOUT)
	vers_tmp = java_version.decode('utf8').strip()
	version = vers_tmp.splitlines()[0].split()[-1].strip('"')
	version = version[2:3]
	return version


def download_and_install_java(packages, version, update, b):
	site = "http://download.oracle.com/otn-pub/java/jdk"
	osEx = sys.platform
	if osEx.startswith("linux"):
		osEx = "linux"
		ext = "tar.gz"
	urlTemplate = Template("${site}/${version}u${update}-b${b}/${package}-${version}-${osEx}-x${arch}.${ext}")
	fileTemplate = Template("${package}-${version}u${update}-${osEx}-x${arch}.${ext}")
	arch = platform.architecture()[0]
	arch = arch[0:2]
	for package in packages:
		d = dict(
			site = site,
			package = package,
			version = version,
			update = update,
			b = b,
			osEx = osEx, 
			arch = arch,
			ext= ext
		)
		url = urlTemplate.safe_substitute(d)
		file = fileTemplate.safe_substitute(d)
		fileName = file.split(".")[0]
		print("Downloading %s" % (url))
		opener = urllib2.build_opener()
		cookie = 'Cookie'
		license = 'oraclelicense=accept-securebackup-cookie'
		opener.addheaders.append((cookie, license))
		f = opener.open(url)
		with open(file, 'wb+') as save:
			save.write(f.read())
		pathJava =  "/usr/bin/java"
		fileName = file.split(".")[0]
		pathLocal = os.getcwd()+"/"+fileName+"/bin/java"
		subprocess.Popen(["tar", "-xvf", file], stdin=PIPE,stdout=PIPE,stderr=PIPE)
		variables = ["java", "javac", "javaws"]
		for var in variables:
			print("Installing Java" % (var))
			process = subprocess.Popen(["sudo", "update-alternatives", "--install",  pathJava, var, pathLocal], 
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)
			out, error = process.communicate()
			if not error:
				print("Done installing Java" % (var))


def update_java_version(packages, version, update, wpkgRoot):
    for package in packages:
            sourceXML = "%s-%d.xml" % (package, version)
            with open(sourceXML) as templateXML:
                lines=templateXML.readlines()
            template = Template( ''.join(lines) )
            d=dict(update=update)
            targetXML = os.path.join(wpkgRoot,'packages',sourceXML)
            with open(targetXML,'w') as packageXML:
                packageXML.writelines(template.safe_substitute(d))


def status_email(From, Pwd, To, emailContent):
	msg = MIMEMultipart()
	msg['Subject'] = 'Java installation updates'
	msg['From'] = From
	msg['To'] = To
	body = MIMEText(emailContent)
	msg.attach(body)
	server = smtplib.SMTP(host='your_host_address', port='your_port')
	server.starttls()
	server.login(From, Pwd)
	server.sendmail(msg['From'], msg['To'], msg.as_string())


def main():
	java = check_java_exist()
	From = "Your address here "
	Pwd = "Your Pwd here"
	To = "Your recipients here" #List in case of multiple recipients
	if not java:
		version = check_java_version()
		print ("Java version installed :" + version)
		emailContent += "\n This email is automatically sent, please do not reply to this email"
		send_email(From, Pwd,  To, emailContent)
	else:
		packages = ["jdk","jre"]
		update = "131"
		b = "11"
		version = 8
		wpkgRoot = '/usr/bin/wpkg-tmp'[:-1]
		download_install_java(packages, version, update, b)
		if not java:
			version = check_java_version()
			update_java_version(packages = packages , version = version, update = update, wpkgRoots = wpkgRoots)
			emailContent = "Java wasn't installed, the version that is installed now:" + version
			emailContent += "\n This email is automatically sent, please do not reply to this email"
			send_email(From,Pwd, To, emailContent)


if __name__=='__main__':
	main()



