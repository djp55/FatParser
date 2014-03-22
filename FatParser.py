#DJ Palombo
#FAT Parser

def hexFormat(data, location): #This function is used to properly format the hex values being read off the disk
    formattedCorrectly = hex(data[location]) #This created formattedCorrectly as the hex value found at the location given
    strippedData = formattedCorrectly[2:] #This removes the "0x" from in front of the value to allow for easier processing
    if len(strippedData) == 2: #This if statement just ensures that two values are returned, as hex values of double zero and with a leading zero were being problematic
        return (strippedData)
    elif len(strippedData) == 1:
        return ("0"+strippedData)
    else:
        return ("00")

def letterHex(data, location): #This is used when parsing GPT.  This is to get the partition name.
    letterHexValue = hexFormat(data, location) #The offset for the name is 56
    if letterHexValue == "00": #Once a name ends, it pads the rest of the 72 bytes as 00, which wouldn't work with the name.  So I replace 00 with nothing so it has no effect
        letterHexValue = ""
        return (letterHexValue)
    else:
        letterValue = chr(int(letterHexValue, 16))
        return (letterValue)

def fatSfnName(data, location):
    x = 1
    firstChar = letterHex(data, location)
    while x < 12:
        firstChar += letterHex(data, (location + x))
        x = x + 1
        return(firstChar)

def fatTimeF(data, location):
    createTime = hexFormat(data, location)
    createTime += hexFormat(data, (location - 1))
    binTime = bin(int(createTime, 10))
    binTimeS = binTime[-5:]
    binTimeM = binTime[-6:6]
    binTimeH = binTime[:5]

    if int(binTimeH, 10) < 13:
        creationTime = ("AM")
        creationTime += (int(binTimeS, 10) * 2)
        creationTime += int(binTimeM, 10)
        creationTime += int(binTimeH, 10)
    else:
        creationTime = ("PM")
        creationTime += (int(binTimeS, 10) * 2)
        creationTime += int(binTimeM, 10)
        creationTime += int(binTimeH, 10)

def fatDateF(data, location):
    fatDate = hexFormat(data, location)
    fatDate += hexFormat(data, (location - 1))
    binDate = bin(int(fatDate, 10))
    binDateD = binDate[-5:]
    binDateM = binDate[-6:8]
    binDateY = binDate[:7]
    return(int(binDateD, 10) + "/" + int(binDateM, 10) + "/" + (int(binDateY, 10) + 1980))

def sfn(data, location):
    firstChar = hexFormat(data, (location + 0))

    if firstChar == "00":
        print("Unallocated")
        #exit this function
    elif firstChar.upper() == "E5":
        print(fatSfnName(1))
        print("Deleted")

    else:
        print(fatSfnName(0))

    fileAttributes = hexFormat(data, location + 12)
    if fileAttributes == "01":
        print("Read Only")
    elif fileAttributes == "02":
        print("Hidden File")
    elif fileAttributes == "04":
        print("System File")
    elif fileAttributes == "08":
        print("Volume Label")
    elif fileAttributes == "0f":
        print("Long File Name")
    elif fileAttributes == "10":
        print("Directory")
    elif fileAttributes == "20":
        print("Archive")
    else:
        print(fileAttributes, "Is not a valid file attribute")

    creationTime = fatTimeF(data, 16)
    print("The file creation time is: ", creationTime, '\n')
    creationDate = fatDateF(data, 18)
    print("The file creation date is: ", creationDate, '\n')
    accessDate = fatDateF(data, 20)
    print("The file access date is: ", accessDate, '\n')

    modifiedTime = fatTimeF(data, 24)
    print("The file modified date is: ", modifiedTime, '\n')
    modifiedDate = fatDateF(data, 26)
    print("The file modified date is: ", modifiedDate, '\n')

    fileSize = hexFormat(data, 32)
    fileSize += hexFormat(data, 31)
    fileSize += hexFormat(data, 30)
    fileSize += hexFormat(data, 29)
    if int(fileSize, 10) != 0:
        print("The file size is: ", int(fileSize, 10))
    else:
        print("Directories do not have their size stored in Root Directory.")


def fat32(infile, location):
    y = 0
    data = infile.read()
    while hexFormat(data, location) != "00":
        sfn(data, (location + y))
        y = y + 32


def main():
    given = input("Enter the path to a FAT formatted RAW image: ")
    with open(given, "rb") as infile:
        data = infile.read(1024)

        bytesPerSector = hexFormat(data, 11)
        bytesPerSector += hexFormat(data, 10)
        theCluster = int(bytesPerSector, 10)

        sectorsPerCluster = int(hexFormat(data, 12), 10)

        fatCopies = int(hexFormat(data, 15), 10)

        rootDirectoryEntries = hexFormat(data, 17)
        rootDirectoryEntries += hexFormat(data, 16)
        numberRootDirEntries = int(rootDirectoryEntries, 10)

        rootDirectoryLocation = hexFormat(data, 48)
        rootDirectoryLocation += hexFormat(data, 47)
        rootDirectoryLocation += hexFormat(data, 46)
        rootDirectoryLocation += hexFormat(data, 45)
        rootDirectory = int(rootDirectoryLocation, 10)

        if numberRootDirEntries == 224:
            print("in progress")
        elif numberRootDirEntries == 0:
            fat32(infile, rootDirectory)
        else:
            print("in progress")
