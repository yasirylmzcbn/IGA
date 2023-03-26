from flask import Flask, render_template, request
import openai
from PyPDF2 import PdfReader
# from pageIndex import pageNum
 
# creating a pdf reader object
reader = PdfReader('HP1.pdf')
# printing number of pages in pdf file
print(len(reader.pages))
pages = [] 

def get_paragraphs(page_text):
    paragraphs = []
    for line in page_text.split("\n"):
        if line.endswith((".", "?", "!")) and len(line) > 2 and len(line) < 70:
            current_paragraph += line.strip() + "\n"
            paragraphs.append(current_paragraph)
            current_paragraph = ""
        else:
            current_paragraph += line.strip() + " "
        if line.isupper():
            current_paragraph += '\n\n'
        
    # Add the last paragraph to the list
    if current_paragraph:
        paragraphs.append(current_paragraph)
    return paragraphs

for i in range(len(reader.pages)):
    pages.append(reader.pages[i].extract_text())
    




# openai.api_key = "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"

# # prompt generation
# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "system", "content": "You are a helpful assistant that finds a few keywords from a page from a book that is inputted to be used as a prompt for DALL-E to generate images to aid the user in visualizing what's going on in the text. You create a prompt from the keywords in a way that would help the DALL-E AI generate a picture that is like a scene from a movie. Keep the prompt to about a sentence and only include the most important idea from the input."},
#         {"role": "user", "content": "He pocketed it to use on Fluf fy — he didn’ t feel much like singing. He ran back down to the common room. “We’d better put the cloak on here, and make sure it covers all three of us –         if Filch spots one of our feet wandering along on its own —” What are you doing?” said a voice from the corner of the room. Neville appeared from behind an armchair , clutching T revor the toad, who looked as though he’d been making another bid for freedom.         “Nothing, Neville, nothing,” said Harry , hurriedly putting the cloak behind         his back.         Neville stared at their guilty faces.         “You’re going out again,” he said.         “No, no, no,” said Hermione. “No, we’re not. Why don’ t you go to bed, Neville?” Harry looked at the grandfather clock by the door . They couldn’ t afford to         waste any more time, Snape might even now be playing Fluf fy to sleep. “You can’ t go out,” said Neville, “you’ll be caught again. Gryf findor will be in even more trouble.” “You don’ t understand,” said Harry , “this is important.”         But Neville was clearly steeling himself to do something desperate.         I won’ t let you do it,” he said, hurrying to stand in front of the portrait hole. “I’ll — I’ll fight you!” “Neville, “Ron exploded, “get away from that hole and don’ t be an idiot— "}]) 


# reply = response['choices'][0]['message']['content']

# print(reply)

# # image generation
# response = openai.Image.create(
#   prompt= reply + "",
#   n=1,
#   size="1024x1024"
# )
# image_url = response['data'][0]['url']
# print(image_url)

app = Flask(__name__)
pageNumber = 0

# @app.route('/')
# def index():
#     return "main pageee"

@app.route("/", methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     if request.form.get('action1') == 'Previous':
    #         pass # do something
    #     elif  request.form.get('action2') == 'Next':
    #         pass # do something else
    #     else:
    #         pass # unknown
    # elif request.method == 'GET':
    #     return render_template('testindex.html')
    
    return render_template("testindex.html", pageText=pages[2])

@app.route("/next")
def next():
    # if pageNumber != 0:
    #     pageNumber += 1
    return render_template("testindex.html", pageText=pages[15])

@app.route("/previous")
def previous():
    # if pageNumber != len(pages):
    #     pageNumber -= 1
    return render_template("testindex.html", pageText=pages[10])

pageNumber = 0
# def contact():
#     if request.method == 'POST':
#         if request.form['submit_button'] == 'Do Something':
#             pass # do something
#         elif request.form['submit_button'] == 'Do Something Else':
#             pass # do something else
#         else:
#             pass # unknown
#     elif request.method == 'GET':
#         return render_template('contact.html', form=form)
