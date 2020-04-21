
from flask import render_template, flash, send_from_directory, send_file
from app.giturl_class.url_form import UrlForm
from app.giturl_class.download_form import DownloadButton
from app.giturl_class import bp
import json
import os

USE_TEST_FILE = False

if(os.getenv('SM2KG_TEST_MODE') == 'TRUE'):
    USE_TEST_FILE = True
    print('SM2KG in Test Mode')
else:  
    from somef import cli 

#from somef import cli

dirname = os.path.dirname(__file__)

#class names in json to be added in the header section. Can either add classes, or rearrange the order of these to change the display
headerClassNames = [ 
        "topics",
        "languages",
        "license",
        "forks_url",
        "readme_url"
]
#class names in json to be added to body of metadata section, similar to headerClassNames
bodyClassNames = [
        "citation",
        "installation",
        "invocation",
        "description"
]

#this is a defaultHeaderClassBreak value, could change it for different formatting
headerClassBreak = int(len(headerClassNames)/2)

#helper function to display array of data in string format
def arrayToStr(arrayToCon):
    returnStr = arrayToCon[0] 
    for i in range(1, len(arrayToCon)):
        returnStr = returnStr + " " + arrayToCon[i] 

    return returnStr

#checks if string starts with https:
def isURL(urlString): 
    if(not(type(urlString is str))): 
            return False
    elif(len(urlString) < 6):  
            return False
    print(urlString[0:6])
    return urlString[0:6] == "https:"

def getAvgOfArr(numArray):
    avg = 0
    numOfNums = 0
    for i in numArray:
        avg += i
        numOfNums += 1

    return avg/numOfNums



@bp.route('/index', methods = ['GET', 'POST'])
def urlPage():
    urlForm = UrlForm()
    downloadForm = DownloadButton()

    citation_list = []
    installation_list = []
    invocation_list = []
    description_list = []
    description_conf_list = None
    showDownload = None
    git_name = None
    git_owner = None
    headerClassesToPass = []
    bodyClassesToPass = []


    

    if downloadForm.submit_download.data:
        output_file = os.path.join(dirname, '../data/output.txt')
        return send_file("../data/output.json", as_attachment=True)
        #flash("Download")
        
    if urlForm.validate_on_submit() and urlForm.submit.data:
       
        #page only shows json data if showDownload is True. Sets to true if json file generated or test file env var set(would be nice to be able to set test file)
        showDownload = True
        try: 
            cli.run_cli(urlForm.giturl.data, .8, 'data/output.json')
        except: 
            print("Error generating json") 
            flash("There must be a problem with your link")
            showDownload = False 
        inputFile = 'data/output.json'
        if(USE_TEST_FILE):
            inputFile = 'data/test.json'
            showDownload = True

        with open(inputFile) as json_file:
            data = json.load(json_file)
            storedData = data

            for i in bodyClassNames:
                classData = []
                for j in data[i]:

                    j["confidencAvg"] = getAvgOfArr(j["confidence"])
                    classData.append(j)

                tempDict = {"className" : i,
                    "metadata" : classData }
                bodyClassesToPass.append(tempDict)
            
            print(bodyClassesToPass) 
            for i in headerClassNames:
                #if excerpt is a list, converts it to string for display 
                if(type(data[i]["excerpt"]) is list):
                    data[i]["excerpt"] = arrayToStr(data[i]["excerpt"])

                #if excerpt is url, makes into link 
                tempDict = {"className" : i,
                    "excerpt" : data[i]["excerpt"],
                    "confidence" : data[i]["confidence"],
                    "isURL" : isURL(data[i]["excerpt"]) }

                headerClassesToPass.append(tempDict)

               
            #two headerClasses that take special formating, could be passed in as special params but eh, ima lazy boy
            git_name = data["name"]["excerpt"]
            git_owner = data["owner"]["excerpt"]
                    

    return render_template('giturl_class/giturl.html',
                           form = urlForm,
                           downloadForm = downloadForm,
                           showDownload = showDownload,
                           citation = citation_list,
                           installation = installation_list,
                           invocation = invocation_list,
                           description = description_list,
                           headerClasses = headerClassesToPass,
                           headerClassBreak = headerClassBreak,
                           bodyClasses = bodyClassesToPass,
                           git_name = git_name,
                           git_owner = git_owner)


@bp.route('/about', methods = ['GET'])
def aboutPage():
    return render_template('aboutpage/aboutpage.html')


@bp.route('/help', methods = ['GET'])
def helpPage():
    return render_template('helppage/helppage.html')
