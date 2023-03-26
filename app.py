from flask import Flask, render_template, request
import openai
from PyPDF2 import PdfReader
 
pages = []
def read(bookName):
    global pages
    pages = []
    reader = PdfReader("books/" + bookName + ".pdf")
    for i in range(len(reader.pages)):
        pages.append(reader.pages[i].extract_text())


    
openai.api_key = "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"
# "He pocketed it to use on Fluf fy — he didn’ t feel much like singing. He ran back down to the common room. “We’d better put the cloak on here, and make sure it covers all three of us –         if Filch spots one of our feet wandering along on its own —” What are you doing?” said a voice from the corner of the room. Neville appeared from behind an armchair , clutching T revor the toad, who looked as though he’d been making another bid for freedom.         “Nothing, Neville, nothing,” said Harry , hurriedly putting the cloak behind         his back.         Neville stared at their guilty faces.         “You’re going out again,” he said.         “No, no, no,” said Hermione. “No, we’re not. Why don’ t you go to bed, Neville?” Harry looked at the grandfather clock by the door . They couldn’ t afford to         waste any more time, Snape might even now be playing Fluf fy to sleep. “You can’ t go out,” said Neville, “you’ll be caught again. Gryf findor will be in even more trouble.” “You don’ t understand,” said Harry , “this is important.”         But Neville was clearly steeling himself to do something desperate.         I won’ t let you do it,” he said, hurrying to stand in front of the portrait hole. “I’ll — I’ll fight you!” “Neville, “Ron exploded, “get away from that hole and don’ t be an idiot— "

app = Flask(__name__)
pageNumber = 0

@app.route('/generateImage')
def generateImage():
    gptPrompt = pages[pageNumber]
    # prompt generation
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that finds a few keywords from a page from a book that is inputted to be used as a prompt for DALL-E to generate images to aid the user in visualizing what's going on in the text. You create a prompt from the keywords in a way that would help the DALL-E AI generate a picture that is like a scene from a movie. Keep the prompt to about a sentence and only include the most important idea from the input."},
        {"role": "user", "content": gptPrompt}]) 

    reply = response['choices'][0]['message']['content']
    print(reply)

    # image generation
    response = openai.Image.create(
    prompt= reply + "",
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    print("image url:",image_url)
    return render_template("testindex2.html", pageText=pages[pageNumber], pageNumber=pageNumber, dalleImage=image_url)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("landing.html")

@app.route("/next")
def next():
    global pageNumber
    if pageNumber != len(pages):
        pageNumber += 1
    return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, dalleImage="https://github.com/yasirylmzcbn/IGA/blob/chromeExtension/loading.gif")

@app.route("/previous")
def previous():
    global pageNumber
    if pageNumber != 0:
        pageNumber -= 1
    return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, dalleImage="https://github.com/yasirylmzcbn/IGA/blob/chromeExtension/loading.gif")

# @app.route("/HP")
# def HP():
#     global pageNumber, pages
#     pageNumber = 0
#     read('HP')
#     print("length = ",len(pages))
#     return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, dalleImage="https://github.com/yasirylmzcbn/IGA/blob/chromeExtension/loading.gif")

@app.route("/<string:name>")
def chooseBook(name):
    global pageNumber, pages
    pageNumber = 0
    read(name)
    return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, bookName=name, dalleImage="https://github.com/yasirylmzcbn/IGA/blob/chromeExtension/loading.gif")

# @app.route("/submitPage")
# def my_form_post():
#     text = request.form['pageInput']
#     processed_text = text.upper()
#     print('-'*100)
#     print(processed_text)
#     print('-'*100)
#     return processed_text


# @app.route("/<string:name>/<int:pageNum>")
# def bookPage(name, pageNum):
#     global pages
#     pageNumber = pageNum
#     reader = PdfReader("books/" + str(name) + ".pdf")
#     read(name)
#     return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, dalleImage="https://github.com/yasirylmzcbn/IGA/blob/chromeExtension/loading.gif")
