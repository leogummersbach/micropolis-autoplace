from image_array import *
import json
import os


class Module_connections():
    def __init__(self, streets="0000", corners="0000", custom=None):
        if custom is None:
            custom = ["-" * 16, "-" * 16, "-" * 16, "-" * 16]
        self.streetLocations = StreetLocations(streets, corners, custom)

    def __repr__(self):
        return str(self.streetLocations)

    def safe(self, path):
        json_dict = {
                    "streets": self.streetLocations.loc,
                    "corners": self.streetLocations.corners,
                    "custom_connections": self.streetLocations.custom,
                    "custom_important": self.streetLocations.custom_important,
                    "key": self.streetLocations.key
                    }
        toWrite = json.dumps(json_dict)
        f = open(path, "w")
        f.write(toWrite)
        f.close()


    def load(self, path):
        if(os.path.exists(path)):
            f = open(path, "r")
            read = f.read()
            d = json.loads(read)
            try:
                self.streetLocations.loc = d["streets"]
            except:
                pass
            try:
                self.streetLocations.corners = d["corners"]
            except:
                pass
            try:
                self.streetLocations.custom = d["custom_connections"]
            except:
                pass
            try:
                self.streetLocations.key = d["key"]
            except:
                pass
            try:
                self.streetLocations.custom_important = d["custom_important"]
            except:
                pass
        else:
            print(f"Could not load file <{path}>, defaults will be safed instead.")
            self.safe(path)

    def getStreetLocation(self, pos, getCorner=False):
        if(not getCorner):
            return bool(int(self.streetLocations.loc[pos]))
        else:
            return bool(int(self.streetLocations.corners[pos]))

    def setStreetLocation(self, pos, connectionBool, setCorner=False):
        if(not setCorner):
            l = list(self.streetLocations.loc)
            l[pos] = str(int(connectionBool))[0]
            self.streetLocations.loc = "".join(l)
        else:
            l = list(self.streetLocations.corners)
            l[pos] = str(int(connectionBool))[0]
            self.streetLocations.corners = "".join(l)