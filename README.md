# SOMEF-WebApp

The Sofware Metadata Extraction Framework Web Application lets users enter a Github URL, and retrieve metadata about the repository, which can be downloaded in a JSON format.

Installation Instructions:

1st) 
  Make sure you have Python version 3!
  Follow the instructions here if you don't: https://wiki.python.org/moin/BeginnersGuide/Download
  
2nd) 
  Download the somef library as describered here: https://github.com/KnowledgeCaptureAndDiscovery/somef/tree/cli
  ```
  pip3 install -r requirements.txt
  ```
3rd)
  Download the requirements from the requirements.txt
  ```
  pip3 install -r requirements.txt
  ```
4th)
  To run the Flask application run:
  ```
  flask run
  ```
Additional Instructions:
  If you're having trouble connection to github or downloading the somef package, you can run the site on an example repo by running: 
  ```
  export SM2KG_TEST_MODE=TRUE
  flask run
  ```
  
