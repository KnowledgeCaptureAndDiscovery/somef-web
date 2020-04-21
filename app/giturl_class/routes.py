
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
    print("bla bla")
    print(type(urlString))
    if(not(type(urlString is str))):
            print("sdf")
            return False
    elif(len(urlString) < 6): 
            print("hal")
            return False
    print(urlString[0:6])
    return urlString[0:6] == "https:"


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
    git_topics = None
    git_languages = None
    git_license = None
    git_forks_url = None
    git_topics = []
    git_languages = []
    git_readme_url = None

    headerClassesToPass = []


    

    if downloadForm.submit_download.data:
        output_file = os.path.join(dirname, '../data/output.txt')
        return send_file("../data/output.json", as_attachment=True)
        #flash("Download")
        
    if urlForm.validate_on_submit() and urlForm.submit.data:
        #flash("Classifying data")

        showDownload = True
        try: 
            cli.run_cli(urlForm.giturl.data, .8, 'data/output.json')
        except: 
            print("Error") 
            flash("There must be a problem with your link")
            showDownload = False 
        inputFile = 'data/output.json'
        if(USE_TEST_FILE):
            inputFile = 'data/test.json'
            showDownload = True
        with open(inputFile) as json_file:
            data = json.load(json_file)
            for i in data['citation']:
                if type(i) is dict:
                    citation_list.append(i['excerpt'])
            for i in data['installation']:
                if type(i) is dict:
                    installation_list.append(i['excerpt'])
            for i in data['invocation']:
                if type(i) is dict:
                    invocation_list.append(i['excerpt'])
            
            for i in data['description']:  
                if type(i) is dict:
                    description_list.append(i['excerpt'])
                else:
                    description_list.append(i)

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

               
            #two headerClasses that take special formating, could be passed in as special params but eh 
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
                           git_name = git_name,
                           git_owner = git_owner)


@bp.route('/about', methods = ['GET'])
def aboutPage():
    return render_template('aboutpage/aboutpage.html')


@bp.route('/help', methods = ['GET'])
def helpPage():
    return render_template('helppage/helppage.html')
