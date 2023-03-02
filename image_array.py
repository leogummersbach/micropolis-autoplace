from tkinter import *
from PIL import Image, ImageTk
import random as rd
import copy

class PlacedImage():
    def __init__(self, path, x, y, deg, height=128, width=128):
        self.path = path
        self.x = x
        self.y = y
        self.deg = deg
        self.height = height
        self.width = width

    def getImageTk(self):
        img = Image.open(self.path).resize((self.height, self.width))
        img_r = img.rotate(self.deg)
        return ImageTk.PhotoImage(img_r)

    def getCoord(self):
        return (self.x, self.y)

class Imagelist():
    def __init__(self, size=128):
        self.list = []
        self.size = size
        
    def setImageSize(self, newSize):
        self.size = newSize
        
    def addDefault(self, name, x, y, rot=0):
        self.list.append(PlacedImage("default_modules/"+name+".png", self.size*x, self.size*y, 90*rot))

    def add(self, path, x, y, rot=0):
        self.list.append(PlacedImage(path, self.size*x, self.size*y, 90*rot, height=self.size, width=self.size))

    def getImageTkList(self):
        mapped = []
        for pi in self.list:
            mapped.append(pi.getImageTk())
        return mapped

    def getCoordList(self):
        mapped = []
        for pi in self.list:
            mapped.append(pi.getCoord())
        return mapped

class StreetLocations():
    def __init__(self, string, cornerstring, custom=None):
        if custom is None:
            custom = ["-" * 16, "-" * 16, "-" * 16, "-" * 16]
        self.loc = string #steets
        self.corners = cornerstring #corners
        self.custom = custom #custom connections
        self.custom_important = [False, False, False, False]
        self.key = ["", "", "", ""]

    def getCustomImportant(self, direction):
        direction = direction % 4
        return self.custom_important[direction]

    def setCustomImportant(self, direction, toSet):
        direction = direction % 4
        self.custom_important[direction] = toSet

    def getKey(self, direction):
        direction = direction % 4
        return self.key[direction]

    def setKey(self, direction, key):
        direction = direction % 4
        self.key[direction] = key

    def rotate(self, rotation):
        real_rot = rotation % 4
        for i in range(real_rot):
            self.loc = self.loc[3] + self.loc[:3]
            self.corners = self.corners[3] + self.corners[:3]
            newcustom = [self.custom[3], self.custom[0], self.custom[1], self.custom[2]]
            self.custom = newcustom
            newkey = [self.key[3], self.key[0], self.key[1], self.key[2]]
            self.key = newkey
            newcustom_important = [self.custom_important[3], self.custom_important[0], self.custom_important[1], self.custom_important[2]]
            self.custom_important = newcustom_important

    def setCustomConnection(self, side, index, connectionKey):
        # side must be 0-3, index 0-15
        if(len(connectionKey) == 1):
            l = list(self.custom[side])
            l[index] = connectionKey
            self.custom[side] = "".join(l)

    def getCustomConnection(self, side, index):
        return self.custom[side][index]

    def customConnectionMatch(self, other, side, compareToNextAlso=False):
        side = side % 4
        other_side = (side + 2) % 4
        assumption = True
        for i in range(16):
            toCompare = self.getCustomConnection(side, i)
            if(toCompare == other.getCustomConnection(other_side, 15-i)):
                continue
            if(i < 15 and compareToNextAlso):
                #compare other one lower
                if(toCompare == other.getCustomConnection(other_side, 14-i)):
                    continue
            if(i > 0 and compareToNextAlso):
                #compare other one more
                if(toCompare == other.getCustomConnection(other_side, 16-i)):
                    continue
            assumption = False
            break
        return assumption

    def __repr__(self):
        sides = []
        if (self.loc[0] == '1'):
            sides.append("right")
        if (self.loc[1] == '1'):
            sides.append("top")
        if (self.loc[2] == '1'):
            sides.append("left")
        if (self.loc[3] == '1'):
            sides.append("bottom")
        sides_nice = ", ".join(sides)
        cornersides = []
        if (self.corners[0] == '1'):
            cornersides.append("upper-right")
        if (self.corners[1] == '1'):
            cornersides.append("upper-left")
        if (self.corners[2] == '1'):
            cornersides.append("lower-left")
        if (self.corners[3] == '1'):
            cornersides.append("lower-right")
        corners_nice = ", ".join(cornersides)
        return "The Module has a Street on the " + sides_nice + " side and a corner on the " + corners_nice + " side. Cornerstring: " + self.corners + ", Customs:\n" +\
            str(self.custom)

class SimpleImage():
    def __init__(self, path, rot, isDefaultImage=False):
        self.streetlocations = None
        if(isDefaultImage):
            self.path = "default_modules/"+path+".png"
            if(path == "O"):
                self.streetlocations = StreetLocations("1111", "1111")
                
            if(path == "I00"):
                self.streetlocations = StreetLocations("0010", "0110")
            if(path == "I01"):
                self.streetlocations = StreetLocations("0010", "1110")
            if(path == "I10"):
                self.streetlocations = StreetLocations("0010", "0111")
            if(path == "I11"):
                self.streetlocations = StreetLocations("0010", "1111")
                
            if(path == "II"):
                self.streetlocations = StreetLocations("0101", "1111")
                
            if(path == "L0"):
                self.streetlocations = StreetLocations("1001", "1011")
            if(path == "L1"):
                self.streetlocations = StreetLocations("1001", "1111")
                
            if(path == "None0000"):
                self.streetlocations = StreetLocations("0000", "0000")
            if(path == "None0001"):
                self.streetlocations = StreetLocations("0000", "0001")
            if(path == "None0011"):
                self.streetlocations = StreetLocations("0000", "0011")
            if(path == "None0101"):
                self.streetlocations = StreetLocations("0000", "0101")
            if(path == "None0111"):
                self.streetlocations = StreetLocations("0000", "0111")
            if(path == "None1111"):
                self.streetlocations = StreetLocations("0000", "1111")
                
            if(path == "U"):
                self.streetlocations = StreetLocations("1101", "1111")
            self.streetlocations.rotate(rot)
        else:
            self.path = path
        self.rot = rot
        self.defaultImage = isDefaultImage

    def getKey(self, direction):
        direction = direction % 4
        return self.streetlocations.key[direction]

    def isDefault(self):
        return self.defaultImage

    def setStreetLocations(self, streetlocationselement):
        self.streetlocations = streetlocationselement
        self.streetlocations.rotate(self.rot)

    def isCompatible(self, other, location, mindCustoms=False):
        """
        Determines if image is compatible to another image, when other image is placed on location (0 = right, 1 = top, 2 = left, 3 = bottom) relative to this image.
        """
        if(self.streetlocations == None or other.streetlocations == None):
            return False
        real_location = location % 4
        other_real_location = (real_location + 2) % 4
        #print(f"self ({self.path}) custom: {self.streetlocations.custom[real_location]}, other ({other.path}) custom: {other.streetlocations.custom[other_real_location]}, mindCustoms: {mindCustoms}")
        this_street_on_location = self.streetlocations.loc[real_location]
        other_street_on_location = other.streetlocations.loc[other_real_location]
        if(this_street_on_location == '1' and other_street_on_location == '1'):
            if(mindCustoms and not self.isDefault()):
                return self.streetlocations.customConnectionMatch(other.streetlocations, location)
            else:
                return True
        if(this_street_on_location == '0' and other_street_on_location == '0'):
            this_before_location = (real_location + 3) % 4
            other_before_location = (other_real_location + 3) % 4
            this_corner_on_location1 = self.streetlocations.corners[real_location]
            this_corner_on_location0 = self.streetlocations.corners[this_before_location]
            other_corner_on_location1 = other.streetlocations.corners[other_real_location]
            other_corner_on_location0 = other.streetlocations.corners[other_before_location]
            if(this_corner_on_location1 == other_corner_on_location0 and this_corner_on_location0 == other_corner_on_location1):
                if (mindCustoms and not self.isDefault()):
                    return self.streetlocations.customConnectionMatch(other.streetlocations, location)
                else:
                    return True
        return False

    def __repr__(self):
        return "SimpleImage: Path: " + self.path + ", Rot: " + str(self.rot) + ", StreetLocations: " + str(self.streetlocations) + "\n"

class AllDefaultAllRotationsImageList():
    def __init__(self):
        list = []
        for i in range(4):
            list.append(SimpleImage("I00", i, isDefaultImage=True))
            
        for i in range(4):
            list.append(SimpleImage("I01", i, isDefaultImage=True))
        for i in range(4):
            list.append(SimpleImage("I10", i, isDefaultImage=True))
        for i in range(4):
            list.append(SimpleImage("I11", i, isDefaultImage=True))
            
            
        for i in range(2):
            list.append(SimpleImage("II", i, isDefaultImage=True))

        for i in range(4):
            list.append(SimpleImage("L0", i, isDefaultImage=True))
            
        for i in range(4):
            list.append(SimpleImage("L1", i, isDefaultImage=True))
            
        for i in range(1):
            list.append(SimpleImage("None0000", i, isDefaultImage=True))
        for i in range(1):
            list.append(SimpleImage("None0001", i, isDefaultImage=True))            
        for i in range(1):
            list.append(SimpleImage("None0011", i, isDefaultImage=True))            
        for i in range(1):
            list.append(SimpleImage("None0101", i, isDefaultImage=True))            
        for i in range(1):
            list.append(SimpleImage("None0111", i, isDefaultImage=True))            
        for i in range(1):
            list.append(SimpleImage("None1111", i, isDefaultImage=True))
            
        for i in range(1):
            list.append(SimpleImage("O", i, isDefaultImage=True))
        for i in range(4):
            list.append(SimpleImage("U", i, isDefaultImage=True))
        self.list = list
        
class ImageArray():
    def __init__(self):
        self.dict = {}
        self.highPriority = [] #list for high priority customs (must be placed, are always considered first)

    def addHighPriority(self, path, streetlocations):
        self.highPriority.append((path, streetlocations))

    def enrichPriority(self):
        out = []
        list = self.highPriority
        for t in list:
            path = t[0]
            streetlocations = t[1]
            for r in range(4):
                si = SimpleImage(path, r)
                streetlocations_copy = copy.copy(streetlocations)
                si.setStreetLocations(streetlocations_copy)
                out.append(si)
        return out

    def removeFromPriority(self, path):
        list = self.highPriority
        for e in list:
            if(e[0] == path):
                list.remove(e)
                break
        self.highPriority = list


    def getImage(self, x, y):
        return self.dict[(x, y)]

    def addImage(self, path, x, y, rot, default=False, streetlocations=None):
        si = SimpleImage(path, rot, isDefaultImage=default)
        if(streetlocations != None):
            si.streetlocations = streetlocations
        self.dict[(x, y)] = si

    def addDefaultImage(self, name, x, y, rot=0):
        self.dict[(x, y)] = SimpleImage(name, rot, isDefaultImage=True)
        
    def toImageList(self, size=128):
        out = Imagelist(size)
        for im in self.dict:
            x = im[0]
            y = im[1]
            image = self.dict[im]
            out.add(image.path, x, y, image.rot)
        return out
    
    def __repr__(self):
        out = "ImageArray: \n"
        for key in self.dict:
            out += "Item " + str(self.dict[key]) + " at position " + str(key) + ".\n"
        return out

    def getNeighbors(self, x, y):
        """
        returns all neighbors next to x and y, as well as their relative direction
        """
        out = []
        if((x+1, y) in self.dict):
            out.append((self.getImage(x+1, y), 0))
        if((x, y-1) in self.dict):
            out.append((self.getImage(x, y-1), 1))
        if((x-1, y) in self.dict):
            out.append((self.getImage(x-1, y), 2))
        if((x, y+1) in self.dict):
            out.append((self.getImage(x, y+1), 3))
        return out

    def getNeighbor(self, x, y, direction):
        """
        returns the neighbor next to x and y in the specified direction
        """
        if(direction == 0):
            if((x+1, y) in self.dict):
                return self.getImage(x+1, y)
            else:
                return None
        if(direction == 1):
            if((x, y-1) in self.dict):
                return self.getImage(x, y-1)
            else:
                return None
        if(direction == 2):
            if((x-1, y) in self.dict):
                return self.getImage(x-1, y)
            else:
                return None
        if(direction == 3):
            if((x, y+1) in self.dict):
                return self.getImage(x, y+1)
            else:
                return None

    def getNeighborCoords(self, x, y, direction):
        if (direction == 0):
            return (x + 1, y)
        if (direction == 1):
            return (x, y - 1)
        if (direction == 2):
            return (x - 1, y)
        if (direction == 3):
            return (x, y + 1)

    def isOutside(self, x, y, max_x, max_y):
        return x < 0 or x >= max_x or y < 0 or y >= max_y

    def init_array(self, size_x, size_y, mindCustoms=False, consumeCustoms=True, verbose=False):
        """
        Initializes an image array with width size_x and height size_y.
        The high priority images are tried to be placed first
        The default images are selected random with equal probability.
        Output is always correct if success is True.
        """
        self.dict = {}
        success = True #assumption
        x = -1
        while (x+1 < size_x):
            x += 1
            y = -1
            while (y+1 < size_y):
                y += 1
                if verbose: print(f"({x},{y})")
                highPrio = self.enrichPriority()
                allDefaults = AllDefaultAllRotationsImageList().list

                #check if a high priority module matches
                for direction in range(4):
                    neighbor = self.getNeighbor(x, y, direction)
                    neighbor_coords = self.getNeighborCoords(x, y, direction)
                    neighbor_outside = self.isOutside(neighbor_coords[0], neighbor_coords[1], size_x, size_y)
                    if verbose: print(f"outside: {neighbor_outside}")
                    stillPossible = []
                    for possible in highPrio:
                        #compute neighborKey
                        if(neighbor != None):
                            neighborKey = neighbor.getKey((direction + 2) % 4)
                        elif(neighbor_outside):
                            neighborKey = ""
                        else:
                            neighborKey = None
                        possibleKey = possible.getKey(direction)
                        if verbose: print(f"ok: {possibleKey} (d: ({direction})")
                        if verbose: print(f"nk: {neighborKey} (d: {(direction + 2) % 4})")

                        # check for fitting
                        if(neighborKey == None or possibleKey == neighborKey):
                            if verbose: print("possibleKey == neighborKey")
                            if(neighbor == None or possible.isCompatible(neighbor, direction, mindCustoms=mindCustoms)):
                                stillPossible.append(possible)

                    highPrio = stillPossible

                if verbose: print(f"Possibles: {highPrio}")

                if(len(highPrio) == 0 and mindCustoms):
                    #high possible is empty, mindCustoms is true, so this restriction might be to big
                    #now same algorithm, but if custom connection is not important, mindcustoms is false
                    #print("No Possbiles found. Check for non-important custom connections.")
                    highPrio = self.enrichPriority()
                    for direction in range(4):
                        neighbor = self.getNeighbor(x, y, direction)
                        neighbor_coords = self.getNeighborCoords(x, y, direction)
                        neighbor_outside = self.isOutside(neighbor_coords[0], neighbor_coords[1], size_x, size_y)
                        if verbose: print(f"outside: {neighbor_outside}")
                        stillPossible = []
                        for possible in highPrio:
                            if (neighbor != None):
                                neighborKey = neighbor.getKey((direction + 2) % 4)
                                neighbor_important = neighbor.streetlocations.getCustomImportant((direction + 2) % 4)
                            elif(neighbor_outside):
                                neighborKey = ""
                            else:
                                neighborKey = None
                            possibleKey = possible.getKey(direction)
                            # check for fitting
                            if (neighborKey == None or possibleKey == neighborKey):
                                if verbose: print("possibleKey == neighborKey")
                                if (neighbor == None or possible.isCompatible(neighbor, direction, mindCustoms = (possible.streetlocations.getCustomImportant(direction) or neighbor_important))):
                                    stillPossible.append(possible)
                        highPrio = stillPossible

                if(len(highPrio) != 0):
                    #possible found
                    choose = rd.choice(highPrio)
                    self.addImage(choose.path, x, y, choose.rot, streetlocations=choose.streetlocations)
                    if(consumeCustoms):
                        self.removeFromPriority(choose.path)
                    continue #continue with next field




                #check if a default module matches
                for direction in range(4):
                    neighbor = self.getNeighbor(x, y, direction)
                    stillPossible = []
                    for possible in allDefaults:
                        if(neighbor == None or possible.isCompatible(neighbor, direction, mindCustoms=mindCustoms)):
                            stillPossible.append(possible)
                    allDefaults = stillPossible

                if(len(allDefaults) == 0):
                    print("no default found..")
                    success = False
                    break
                else:
                    choose = rd.choice(allDefaults)
                    self.addDefaultImage(choose.path[16:-4:], x, y, choose.rot)
                    if((not choose.isDefault) and consumeCustoms):
                        self.removeFromPriority(choose.path, high=False)
            if(not success):
                break
        return success
        
