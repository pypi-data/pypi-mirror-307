import re

def regexpFindDataInString(allString , strTemplate , data  )->list:
    # ss = strTemplate
    firstIndex = strTemplate.find(data) 
    if firstIndex == -1:
        return []
    lastIndex = firstIndex + len(data)
    if lastIndex > len(strTemplate) :
        return []
    regString = strTemplate[:firstIndex] + "(.*?)" + strTemplate[lastIndex:]
    result = re.findall(regString,allString)
    return result