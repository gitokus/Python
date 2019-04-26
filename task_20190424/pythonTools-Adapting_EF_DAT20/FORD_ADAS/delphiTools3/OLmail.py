import win32com.client


def sendMail(toList, subject, body, CCList=None, BCCList=None,
             atachments=None, preview=False):

    obj = win32com.client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(0)
    newMail.GetInspector
    newMail.To = '; '.join(toList)
    newMail.Subject = subject

    index = newMail.HTMLbody.find('>', newMail.HTMLbody.find('<body'))
    newMail.HTMLbody = newMail.HTMLbody[:index + 1] + body + newMail.HTMLbody[index + 1:]


    if CCList is not None and type(CCList) == list:
        newMail.CC = '; '.join(CCList)
    if BCCList is not None and type(BCCList) == list:
        newMail.BCC = '; '.join(BCCList)

    if atachments is not None and type(atachments) == list:
        for atachment in atachments:
            newMail.Attachments.Add(atachment)

    if preview:
        newMail.display()
    else:
        newMail.Send()