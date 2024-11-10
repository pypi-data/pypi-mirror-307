import math
import numpy

# Man kan ikke vælge cDegree fordi den altid er 90

class RightTriangle:

    def __init__(self, aSide=False, bSide=False, cSide=False, aDegree=False, bDegree=False):
        self.aSide = aSide
        self.bSide = bSide
        self.cSide = cSide
        self.aDegree = aDegree
        self.bDegree = bDegree
        self.sideDict = {"aSide": aSide, "bSide": bSide, "cSide": cSide}
        self.degreeDict = {"aDegree": aDegree, "bDegree": bDegree, "cDegree": 90}
        self.area = False

        # Type test
        for name, value in self.sideDict.items():
            self.ValueCheck(value, name)

        for name, value in self.degreeDict.items():
            self.ValueCheck(value, name)

        self.RunCalculations()

    def ValueCheck(self, value, name):
        if value is False:
            return
        if isinstance(value, int):
            return
        else:
            raise TypeError(f"{name} must be an integer")


    def get_triangle(self):
        return_dict = dict(self.sideDict, **self.degreeDict)
        return_dict.update({"area": self.area})
        return return_dict
    
    def set_triangle(self):
        return "cannot set value!"
    
    def get_sides(self):
        return self.sideDict
    
    def set_sides(self):
        return "cannot set value!"

    def get_degrees(self):
        return self.degreeDict
    
    def set_degrees(self):
        return "cannot set value!"     

    def RunCalculations(self):
        self.RemoveUnessesaryAngles()
        self.RemoveUnessesarySides()

        if len(self.degreeDict) == 2:
            self.CalculateAngles()

        if len(self.sideDict) == 2:
            self.CalculateSides()
            self.CalculateArea()

        if len(self.sideDict) == 1 and len(self.degreeDict) >= 2:
            self.CalculateSideByAngleAndSide()
            self.CalculateSides()

        if len(self.sideDict) >= 2 and len(self.degreeDict) == 1:
            self.CalculateAngleBySide()
            self.CalculateAngles()


    def RemoveUnessesarySides(self):
        newSideDict = {}

        for key in self.sideDict:
            value = self.sideDict.get(key)
            if value != False:
                newSideDict[key] = value

        self.sideDict = newSideDict

        

    def RemoveUnessesaryAngles(self):
        newDegreeDict = {}

        for key in self.degreeDict:
            value = self.degreeDict.get(key)
            if value != False:
                newDegreeDict[key] = value

        self.degreeDict = newDegreeDict
    

    def CalculateAngles(self):

        firstEntry = self.degreeDict.get(list(self.degreeDict)[0])
        secondEntry = self.degreeDict.get(list(self.degreeDict)[1])
        thirdDegree = 180 - (firstEntry + secondEntry)

        for i in "aDegree", "bDegree", "cDegree":
            if (i not in self.degreeDict):
                self.degreeDict[i] = thirdDegree


    def CalculateArea(self):
        areaFake = self.sideDict["aSide"] * self.sideDict["bSide"]
        arealReal = areaFake/2
        self.area = arealReal

    def CalculateSides(self):
        powersCombined = None

        firstKey = list(self.sideDict)[0]
        secondKey = list(self.sideDict)[1]

        firstEntry = self.sideDict.get(firstKey)
        secondEntry = self.sideDict.get(secondKey)

        firstEntrySecondPower = math.pow(firstEntry, 2)
        secondEntrySecondPower = math.pow(secondEntry, 2)

        if firstKey == "cSide":
            powersCombined = firstEntrySecondPower - secondEntrySecondPower
        elif secondKey == "cSide":
            powersCombined = secondEntrySecondPower - firstEntrySecondPower
        else:
            powersCombined = firstEntrySecondPower + secondEntrySecondPower

        thirdSide = float(math.sqrt(powersCombined))

        for i in "aSide", "bSide", "cSide":
            if (i not in self.sideDict):
                self.sideDict[i] = thirdSide

    def CalculateAngleBySide(self):
        # Jeg kunne lige så godt bruge cos eller tan fordi jeg har de tre sider i dette tilfælde.
        sideA = self.sideDict.get("aSide")
        sideC = self.sideDict.get("cSide")
        ADividedByC = sideA/sideC
        aDegree = float(numpy.degrees(numpy.arcsin(ADividedByC)))
        self.degreeDict["aDegree"] = aDegree


    def CalculateSideByAngleAndSide(self):
        # Jeg tager bare en random side
        # Jeg ved jeg har alle grader

        if "aSide" in self.sideDict:
            ADegree = self.degreeDict.get("aDegree")
            ASide = self.sideDict.get("aSide")

            sinOfADegree = float(numpy.sin(numpy.deg2rad(ADegree)))
            cSide = ASide/sinOfADegree

            self.sideDict["cSide"] = cSide

        elif "bSide" in self.sideDict:
            ADegree = self.degreeDict.get("aDegree")
            BSide = self.sideDict.get("bSide")

            cosOfADegree = float(numpy.cos(numpy.deg2rad(ADegree)))
            cSide = BSide/cosOfADegree

            self.sideDict["cSide"] = cSide
            
        elif "cSide" in self.sideDict:
            ADegree = self.degreeDict.get("aDegree")
            CSide = self.sideDict.get("cSide")

            cosOfADegree = float(numpy.cos(numpy.deg2rad(ADegree)))
            bSide = CSide * cosOfADegree

            self.sideDict["bSide"] = bSide

