# IGA

### IGA, or Image Generating Apparatus, is a project that utilizes OpenAI's APIs for ChatGPT-3.5 and DALL-E 2 to detect the important content in the page that they are reading and create an image using the key content on every page to aid the reader in visualizing what is going on in the book. We also created a chrome extension that allows users to input text that gets summarized and turned into a DALL-E 2 prompt, which is then turned into a picture.

## To run the website yourself locally:

* Go to https://platform.openai.com/account/api-keys
* Create a new API key for yourself and copy it
* Download the repository
* Open app.py and paste your API key where it says `openai.api_key  =  "YOUR_API_TOKEN_HERE"`
* Open a terminal in the directory of the repository
* Run the command `flask run` (you will have to pip install flask, openai, and PyPDF2 if you don't have them already)
* Click on the IP address that pops up in the terminal to visit the the web page.

## To run the extension yourself:
TODO

### Technologies Used:
* Python
* Flask
* OpenAI API
* HTML
* CSS
* JavaScript


