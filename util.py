# coding: utf-8

import subprocess as sp
import os


def exec_command(cmd):

	res = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
	stdout,stderr = res.communicate()
	stdout = stdout.decode('utf-8').replace("\n","")

	return stdout


def fetch_package_source_list():

	f = open("./sources.list", "r")

	c = 0
	for l in f:
		l = l.replace("\n","").split(" ")
		if l[0] != "deb-src":
			continue

		branches = l[3:]
		for branch in branches:
			url = l[1]+"/dists/"+l[2]+"/"+branch+"/source/Sources.gz"
			filen = l[1].replace(":","]").replace("/","[")+"@"+str(c)
			exec_command("wget "+url+" -O ./Sources/"+filen+".gz")
			c += 1
			print(url)

	f.close()

	for file in [s for s in os.listdir("./Sources") if s[0] != '.']:
		exec_command("gunzip ./Sources/"+file)


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
	print(source_list)

	needs = ["Filename"]
	find = False

	for source in source_list:

		with open("./Packages/"+source, "r") as f:
			for line in f:

				if ":" in line.split(" ")[0]:
					attr = line.split(" ")[0].replace(":","").replace("\n","")

				if attr == "Package":
					if find:
						print(info)
						print(info["Host"]+"/"+info["Filename"])
						exit()
					info = {attr:line.split(": ")[1].replace("\n","")}

				if attr in needs:
					info[attr] = line.split(": ")[1].replace("\n","")

				if attr == 'Package' and target in line:
					find = True
					fname = source.split("_")[0]
					print(fname)
					info["Host"] = source.replace("[","/").replace("]",":").split("@")[0]








def package_info2(target):

	source_list = os.listdir("./Sources")
	source_list = [s for s in source_list if s[0] != "."]
	print(source_list)

	needs = ["Directory"]
	find = False

	for source in source_list:

		with open("./Sources/"+source, "r") as f:
			for line in f:

				if ":" in line.split(" ")[0]:
					attr = line.split(" ")[0].replace(":","").replace("\n","")

				if attr == "Package":
					if find:
						print(info)
						exit()
					info = {attr:line.split(": ")[1].replace("\n","")}

				if attr in needs:
					info[attr] = line.split(": ")[1].replace("\n","")

				if attr == 'Binary' and target in line:
					find = True
					fname = source.split("_")[0]
					print(fname)
					info["Host"] = source.replace("[","/").replace("]",":").split("@")[0]


package_info("libboost-all-dev")
exit()




def fetch_package_source(package):

	source_list = os.listdir("./Sources")
	source_list = [s for s in source_list if s[0] != "."]
	print(source_list)


	os.mkdir("./src/"+package)

	for source in source_list:
		cmd = "cat ./Sources/"+source+" | sed -n \'/Package: "+package+"$/,$p\' | grep \'Directory:\' | head -n 1 | awk \'{print $2}\'"
		res = exec_command(cmd)

		print(res)

		if res != "":
			dire = "http://"+"/".join(source.split("@")[1:])+"/"+res
			print(dire)
		
			cmd2 = "cat ./Sources/"+source+" | sed -n \'/Package: "+package+"$/,$p\' | sed -n \'/Files:/,$p\' | head -n 3 | tail -n 1 | awk \'{print $3}\'"
			cmd3 = "cat ./Sources/"+source+" | sed -n \'/Package: "+package+"$/,$p\' | sed -n \'/Files:/,$p\' | head -n 2 | tail -n 1 | awk \'{print $3}\'"


			path1 = exec_command(cmd2)
			path2 = exec_command(cmd3)

			print(path1, path2)

			exec_command("wget "+dire+"/"+path1+" -O ./src/"+package+"/"+path1)
			exec_command("wget "+dire+"/"+path2+" -O ./src/"+package+"/"+path2)

			if path1.split(".")[-1] == "gz" or path1.split(".")[-1] == "bz2":
				exec_command("tar xf ./src/"+package+"/"+path1+" -C ./src/"+package)

			if path1.split(".")[-1] == "xz":
				exec_command("xz -dv ./src/"+package+"/"+path1)
				exec_command("tar xfv ./src/"+package+"/"+path1.replace(".xz","")+" -C ./src/"+package)

			return None












def build_package(package):

	os.chdir("./src/"+package)

	for path in os.listdir("./"):
		if os.path.isdir(path):
			os.chdir(path)
			break


	os.system("./configure --prefix=$HOME/bin")
	exec_command("make")
	exec_command("make install")

	os.chdir("../../../")






package_list2 = ["zlib", "libsdl2", "nasm", "tar"]
package_list3 = ["bzip2", "gtk+2.0", "glib2.0", "fluidsynth", "game-music-emu"]

#, "openal-soft", "unzip", "boost-defaults", "libjpeg8-empty"]
package_list5 = ["mpg123", "libsndfile", "wildmidi", "gtk+3.0", "timidity", "chrpath"]



def main():

	#fetch_package_source_list()

	for package in package_list3:
		fetch_package_source(package)
		build_package(package)



main()



# 愚直にapt installでいろいろ入れたかった
# aptはsudoできないと使えない
# 任意のパッケージについて，aptが参照しているソースをダウンロードして，~/以下でビルドすることにする


# 前提 make dpkg-source


# /etc/apt/sources.list の deb-srcの行にあるSourceファイルのurlを取得
# このプログラムでは以下のurlを用いる

















