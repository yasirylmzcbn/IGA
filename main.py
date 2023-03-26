from flask import Flask, render_template, request
import openai
from PyPDF2 import PdfReader
 

def read(bookName, pages):
    reader = PdfReader(bookName + ".pdf")
    for i in range(len(reader.pages)):
        pages.append(reader.pages[i].extract_text())


    

openai.api_key = "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"
# "He pocketed it to use on Fluf fy — he didn’ t feel much like singing. He ran back down to the common room. “We’d better put the cloak on here, and make sure it covers all three of us –         if Filch spots one of our feet wandering along on its own —” What are you doing?” said a voice from the corner of the room. Neville appeared from behind an armchair , clutching T revor the toad, who looked as though he’d been making another bid for freedom.         “Nothing, Neville, nothing,” said Harry , hurriedly putting the cloak behind         his back.         Neville stared at their guilty faces.         “You’re going out again,” he said.         “No, no, no,” said Hermione. “No, we’re not. Why don’ t you go to bed, Neville?” Harry looked at the grandfather clock by the door . They couldn’ t afford to         waste any more time, Snape might even now be playing Fluf fy to sleep. “You can’ t go out,” said Neville, “you’ll be caught again. Gryf findor will be in even more trouble.” “You don’ t understand,” said Harry , “this is important.”         But Neville was clearly steeling himself to do something desperate.         I won’ t let you do it,” he said, hurrying to stand in front of the portrait hole. “I’ll — I’ll fight you!” “Neville, “Ron exploded, “get away from that hole and don’ t be an idiot— "

app = Flask(__name__)
pageNumber = 0

def generateImage(pages, pageNumber):
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
    print(image_url)
    return image_url

@app.route("/", methods=['GET', 'POST'])
def index():
    global pageNumber
    imgUrl = generateImage(pages, pageNumber)
    return render_template("landing.html", pageText=pages[2], pageNumber=pageNumber, dalleImage=imgUrl)

@app.route("/next")
def next():
    global pageNumber
    if pageNumber != len(pages):
        pageNumber += 1
    imgUrl = generateImage(pages, pageNumber)
    return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, dalleImage=imgUrl)

@app.route("/previous")
def previous():
    global pageNumber
    if pageNumber != 0:
        pageNumber -= 1
    imgUrl = generateImage(pages, pageNumber)
    return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, dalleImage=imgUrl)


@app.route("/<bookName:string>/<pageNum:int>")
def bookPage(bookName, pageNum):
    pages = []
    reader = PdfReader("books\\" + str(bookName) + ".pdf")
    read(bookName, pages)
    imgUrl = generateImage(pages, pageNumber)
    return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, dalleImage=imgUrl)


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
