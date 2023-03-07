import os
import csv

#global functions

def getRotationString(name, rot):
    custom_rotation_offset = 0

    #get config info
    with open("studioexport/config.csv") as config:
        reader = csv.DictReader(config)
        for row in reader:
            if(row["name"] == name):
                custom_rotation_offset = row["custom_rotation_offset"]

    rot += 1 #default offset
    rot += int(custom_rotation_offset)
    rot = rot % 4
    if(rot == 0):
        return "1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000"
    if(rot == 1):
        return "0.000000 0.000000 -1.000000 0.000000 1.000000 0.000000 1.000000 0.000000 0.000000"
    if(rot == 2):
        return "-1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 -1.000000"
    if(rot == 3):
        return "0.000000 0.000000 1.000000 0.000000 1.000000 0.000000 -1.000000 0.000000 0.000000"

def getPositionOffset(name, rot):
    custom_offset_x = 0
    custom_offset_y = 0
    custom_offset_z = 0
    custom_rotation_offset = 0
    extra_offset1 = 0
    extra_offset2 = 0
    extra_offset3 = 0

    #get config info
    with open("studioexport/config.csv") as config:
        reader = csv.DictReader(config)
        for row in reader:
            if(row["name"] == name):
                custom_offset_x = row["custom_offset_x"]
                custom_offset_y = row["custom_offset_y"]
                custom_offset_z = row["custom_offset_z"]
                custom_rotation_offset = row["custom_rotation_offset"]
                if(row["extra_offset1"] != None):
                    extra_offset1 = row["extra_offset1"]
                if(row["extra_offset2"] != None):
                    extra_offset2 = row["extra_offset2"]
                if(row["extra_offset3"] != None):
                    extra_offset3 = row["extra_offset3"]
                break

    rot += 1 #default offset
    rot += int(custom_rotation_offset)
    rot = rot % 4
    if(rot == 0):
        return 0 - int(custom_offset_x) - int(extra_offset3), int(custom_offset_y), 0 + int(custom_offset_z) + int(extra_offset3)
    if(rot == 1):
        return 160 + int(custom_offset_x), int(custom_offset_y), -180 + int(custom_offset_z)
    if(rot == 2):
        return 340 + int(custom_offset_x) + int(extra_offset1), int(custom_offset_y), -20 - int(custom_offset_z) - int(extra_offset1)
    if(rot == 3):
        return 180 - int(custom_offset_x) - int(extra_offset2), int(custom_offset_y), 160 - int(custom_offset_z) - int(extra_offset2)

def makeName(name):
    l = name.split(".", maxsplit=1)[0] #cut off file ending
    return "".join(l)

def makeModuleNameUnique(line, name):
    if(line.startswith("1")):
        if(not line.endswith(".dat")):
            return line + "_" +  name
    elif(line.startswith("0 FILE")):
        return line + "_" + name
    return line

def getBricks(filestring, name):
    out = []
    l = filestring.splitlines()

    #remove leading lines beginning with zero
    while(True):
        if(not l[0].startswith("1")):
            l.pop(0)
        else:
            break
    for line in l:
        if(line.startswith("1") or line.startswith("0 FILE") or line.startswith("0 NOFILE")):
            out.append(makeModuleNameUnique(line, name))
    return "\n".join(out)


class StudioExport():
    def __init__(self, imagearray, name):
        self.dict = imagearray.dict
        self.name = makeName(name)

    def createFileHead(self):
        out = "0 FILE " + self.name + "\n"
        for key in self.dict:
            im = self.dict[key]
            name = makeName(im.path)
            rot = im.rot
            x = key[1]*320 + getPositionOffset(name, rot)[0]
            y = getPositionOffset(name, rot)[1]
            z = key[0]*320 + getPositionOffset(name, rot)[2]
            rotstring = getRotationString(name, rot)
            line = f"1 16 {str(x)} {str(y)} {str(z)} {rotstring} {name}\n"
            out += line
        out += "0 NOFILE\n"
        return out

    def precheck(self):
        #checks if all used modules have exported ldraw files
        notfound = []
        for key in self.dict:
            im = self.dict[key]
            name = makeName(im.path)
            lookfor = name + ".ldr"
            if(not os.path.isfile("studioexport/" + lookfor)):
                if(not lookfor in notfound):
                    notfound.append(lookfor)
        return notfound

    def createFileEnd(self):
        out = ""
        for key in self.dict:
            im = self.dict[key]
            name = makeName(im.path)
            path = "studioexport/" + name + ".ldr"
            file = open(path, "r")
            head = "0 FILE " + name + "\n"
            end = "0 NOFILE\n"
            out += (head + getBricks(file.read(), name) + "\n" + end)
        return out

    def createFile(self):
        name = self.name + ".ldr"
        path = "studioexport/out/" + name
        content = self.createFileHead() + self.createFileEnd()
        file = open(path, "w")
        file.write(content)

