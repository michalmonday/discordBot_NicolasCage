from selenium import webdriver
from selenium.webdriver.common.keys import Keys #needed to press enter after the bot types the reply
from bs4 import BeautifulSoup #awesome tool for extracting useful data from websites
import time #to add delay
import re # regular expressions, much more direct than BeautifulSoup, allows to find patterns within the text (it's a bit like a language on its own)

def GetSource(): # used to refresh the content
    global br # browser object
    elem = br.find_element_by_xpath("//*") # get some kind of "root" element in order to get the actual source
    src = elem.get_attribute("outerHTML")
    return src

def ParseMessage(msg): #used to remove things like: <!-- react-text: 611 -->
    toBeRemoved = re.findall(r'<.+?>', msg) # find all the text between < and >
    for text in toBeRemoved: 
        msg = msg.replace(text, "") # remove each occurence of the text found between < and > so only the actual message is left
    return msg

def GetComments():
    comments = []
    for comChunk in BeautifulSoup(GetSource(), "lxml").find_all("div", class_="comment"): # for each chunk of the code which covers 1 comment
        name = comChunk.find("strong", class_="user-name").string #find username of the one who posted it
        msg=[] # define new list
       
        for addMsgChunk in comChunk.find_all("div", class_="message"): # each "comment" may consist of several messages if the same person posts few messages in a row, this loop adds them all together into 1 class
            msg.append(ParseMessage(repr(addMsgChunk.find("div", class_="markup")))) # appends messages into 1 comment
        
        comments.append({"name":name, "msg":msg}) # appends comments and names into 1 full list
    return comments

def GetCurrentMsg():
    coms = GetComments()
    return coms[-1]["name"], coms[-1]["msg"][-1]

def SendMsg(msg):
    global br # br is a browser object
    entry = br.find_element_by_xpath('//*[@id="app-mount"]/div/div[2]/div/div[2]/div/section/div[3]/div[2]/div[1]/form/div/div/textarea') # get the text input element
    entry.send_keys(msg) # write characters into text input
    entry.send_keys(Keys.RETURN) # press enter


br = webdriver.Chrome()
#br.get("https://discord.gg/VxGFHY4")
br.get("https://discordapp.com/channels/265199259291222016/265199259291222016")

raw_input("Press enter when discord is ready...")


lastName=""
lastMsg=""
while True:
    time.sleep(0.2)
    try:
        name, msg = GetCurrentMsg()
        if msg.startswith("@Nicolas Cage"):
            if name != lastName:
                if msg.endswith("help"):
                    reply = "```Nicolas Cage V0.1 Documentation\nUSAGE: @Nicolas Cage\nCopyright: Nicolas Cage\nAuthor: Nicolas Cage\nSpecial thanks to Nicolas for testing```"
                else:
                    reply = "http://i2.kym-cdn.com/entries/icons/original/000/006/993/1817.jpg"
                
                SendMsg(reply)
                lastName = name
    except Exception as e:
        print "Error: " + repr(e)

    
''' #shows the latest message
cm = GetCurrentMsg(GetSource())
print cm["name"] + ": " + cm["msg"][len(cm["msg"])-1]
'''

''' saves source of the website to a file
soup = BeautifulSoup(source, "lxml")
soup.find("div", class_="messages-wrapper")
with open("src.html", "wb") as f:
    f.write(BeautifulSoup(source, "lxml").prettify().encode("utf-8")) # prettify() function adds identation to the text so it looks nice and clean in the output
'''


