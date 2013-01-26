# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ = "2009.07.20. 23:19:11"

import os.path

class ObjReader:
    def __init__ (self, fileName):
        self.__normalt = False
        self.__texture = False
        if os.path.exists(fileName) and os.path.isfile(fileName):
            self.fileName = fileName

    def load (self):
        if self.fileName:
            try:
                file_in = open(self.fileName, "r", 0)
                self.vertex = ()
                self.face = ()
                try:
                    for line in file_in:
                        if len(line) > 1:
                            print len(line)
                            line = line.strip()
                            if   line[0] == "#":                                #comment
                                pass
                            elif line[0] == "v":                                #vertex
                                if   line[1] == "n":                            #normal
                                    self.__normal = True
                                elif line[1] == "t":                            #texture
                                    self.__texture = True
                                else:
                                    data = line.split(" ")[1:4]                 # split x,y,z coords
                                    data = tuple([float(x) for x in data])      # convert to float
                                    self.vertex += (data, )
                            elif line[0] == "f":                                #face
                                data = line.split(" ")[1:4]
                                data = tuple([tuple([int(x) for x in v.split("/")]) for v in data])
                                self.face += data
                finally:
                    file_in.close()
            except IOError:
                pass


if __name__ == "__main__":
    obj = ObjReader("../resources/test/box.obj")
    obj.load()
    print obj.vertex
    print obj.face
