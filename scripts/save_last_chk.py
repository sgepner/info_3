# -*- coding: utf-8 -*-

import os
import shutil
import sys
import fileinput

def zeroTime(sol_file):
    for line in fileinput.input(sol_file, inplace=1):
        if line.startswith("        <Time>"):
            print "        <Time>0.0</Time>"
            stop=True
        else:
            print line,

def save(zero_time=0):
    if zero_time == 1:
        print "Time will be ReSet"
    for root, dirs, files in os.walk("./"):
        num = []
        save=False
        fnum = 0
        for file in files:
            if file.endswith(".chk"):
                case_str = file.split(".")
                num.append(int(case_str[0][5:]))
        for i in range(0,len(num)):
            file = "geom_"+str(max(num)-i)+".chk"
            file0 = os.path.join(root, file)
            try:
	    	fsize = os.path.getsize(file0)
            	if fsize != 0:
                    save = True
                    fnum = max(num)-i
                    break
	    except:
		pass
        if save:
            file = "geom_"+str(fnum)+".chk"
            file1 = os.path.join(root, file)
            file2 = os.path.join(root, "geom.fld")
            print("copy "+file1+" to "+file2)
            shutil.copyfile(file1, file2)
            command = "rm " + root +"/*.chk"
            print(command)
            os.system(command)
            if zero_time: zeroTime(file2)
        
        num = []
        save=False
        fnum = 0
        for dir in dirs:
            if dir.endswith(".chk"):
#                print(dir)
                case_str = dir.split(".")
                num.append(int(case_str[0][5:]))
        num.sort()
        for i in range(0,len(num)):
            dir = "geom_"+str(max(num)-i)+".chk"
            dir = os.path.join(root, dir)
            isAnyZero=False
            isInfoMissing=True
            for root1, dirs1, files1 in os.walk(dir):
                for file in files1:
#                    print(file)
                    if file=='Info.xml': isInfoMissing=False
                    file0 = os.path.join(root1, file)
                    fsize = os.path.getsize(file0)
                    print dir," ", file0, " ", fsize
                    if fsize == 0:
                        print 'File ', file0, " is empty! ", fsize
                        isAnyZero = True
                        break
                if isAnyZero or isInfoMissing:
                    break
            
                print root1, " is any zero:", isAnyZero, " is Info.xml missing? ", isInfoMissing
                if (not isAnyZero) or (not isInfoMissing):
                    save = True
                    fnum = max(num)-i
                    break
            if save:
                break
        if save:
            dir = "geom_"+str(fnum)+".chk"
            dir = os.path.join(root, dir)
            dir2 = os.path.join(root, "geom.fld")
            command = "rm -rf " + dir2
            print(command)
            os.system(command)
            print("move "+dir+" to " + dir2)
            shutil.move(dir, dir2)
            command = "rm -rf " + root +"/*.chk"
            print(command)
            os.system(command)
            if zero_time:
                infoFile= os.path.join(dir2, "Info.xml")
                zeroTime(infoFile)
            print("Saving ", fnum)
            
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
zero_time=0
if len(sys.argv)>1:
    if str(sys.argv[1])=='zero': zero_time=1
save(zero_time)
