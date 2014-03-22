def hexFormat(data, location): #This function is used to properly format the hex values being read off the disk
    formattedCorrectly = hex(data[location]) #This created formattedCorrectly as the hex value found at the location given
    strippedData = formattedCorrectly[2:] #This removes the "0x" from in front of the value to allow for easier processing
    if len(strippedData) == 2: #This if statement just ensures that two values are returned, as hex values of double zero and with a leading zero were being problematic
        return (strippedData)
    elif len(strippedData) == 1:
        return ("0"+strippedData)
    else:
        return ("00")

