# coding: utf-8

import subprocess as sp
import os


def exec_command(cmd):

	res = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
	stdout,stderr = res.communicate()
	stdout = stdout.decode('utf-8').replace("\n","")

	return stdout



def fetch_package_list():

	f = open("./sources.list", "r")

	c = 0
	for l in f:
		l = l.replace("\n","").split(" ")
		if l[0] != "deb":
			continue

		branches = l[3:]
		for branch in branches:
			url = l[1]+"/dists/"+l[2]+"/"+branch+"/binary-amd64/Packages.gz"
			filen = l[1].replace(":","]").replace("/","[")+"@"+str(c)
			exec_command("wget "+url+" -O ./Packages/"+filen+".gz")
			c += 1
			print(url)

	f.close()

	for file in [s for s in os.listdir("./Packages") if s[0] != '.']:
		exec_command("gunzip ./Packages/"+file)




def package_info(target):

	source_list = os.listdir("./Packages")
	source_list = [s for s in source_list if s[0] != "."]

	needs = ["Filename","Depends"]
	find = False

	for source in source_list:

		with open("./Packages/"+source, "r") as f:
			for line in f:

				if ":" in line.split(" ")[0]:
					attr = line.split(" ")[0].replace(":","").replace("\n","")

				if attr == "Package":
					if find:
						return info

					info = {attr:line.split(": ")[1].replace("\n","")}

				if attr in needs:
					info[attr] = line.split(": ")[1].replace("\n","")

				if attr == 'Package' and target in line:
					find = True
					fname = source.split("_")[0]
					info["Host"] = source.replace("[","/").replace("]",":").split("@")[0]
					if info["Host"][-1] != "/":
						info["Host"] += "/"






def fetch_package(package, info):

	url = info["Host"]+info["Filename"]
	exec_command("wget "+url+" -O ./src/")
	"""
			exec_command("wget "+dire+"/"+path2+" -O ./src/"+package+"/"+path2)

			if path1.split(".")[-1] == "gz" or path1.split(".")[-1] == "bz2":
				exec_command("tar xf ./src/"+package+"/"+path1+" -C ./src/"+package)

			if path1.split(".")[-1] == "xz":
				exec_command("xz -dv ./src/"+package+"/"+path1)
				exec_command("tar xfv ./src/"+package+"/"+path1.replace(".xz","")+" -C ./src/"+package)
	"""











info = package_info("libgcc1")
fetch_package(info)
print(info)
exit()













