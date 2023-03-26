from flask import Flask, render_template, request, redirect, url_for
import openai
from PyPDF2 import PdfReader
import os

books_name = ""
pages = []
pageNumber = 0
def read(bookName):
    global pages, pageNumber
    pageNumber = 0
    pages = []
    reader = PdfReader("books/" + bookName + ".pdf")
    for i in range(len(reader.pages)):
        pages.append(reader.pages[i].extract_text())


openai.api_key = "YOUR_API_TOKEN_HERE"

app = Flask(__name__)
pageNumber = 0


@app.route("/<string:bookName>/generateImage")
def genBookImage(bookName):
    print("in function")
    return redirect(url_for('generateImage'))

@app.route('/generateImage')
def generateImage():
    print("generating")
    global pageNumber
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
    
    return render_template("testindex2.html", pageText=pages[pageNumber], pageNumber=pageNumber, bookName=books_name, dalleImage=image_url)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("landing.html")

@app.route("/next")
def next():
    global pageNumber
    if pageNumber != len(pages):
        pageNumber += 1
    print(len(pages))
    return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, bookName=books_name, dalleImage="https://raw.githubusercontent.com/yasirylmzcbn/IGA/chromeExtension/loading.gif")

@app.route("/previous")
def previous():
    global pageNumber, books_name
    if pageNumber != 0:
        pageNumber -= 1

    return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, bookName=books_name, dalleImage="https://raw.githubusercontent.com/yasirylmzcbn/IGA/chromeExtension/loading.gif")


@app.route("/<string:bookName>/page", methods=['POST'])
def page(bookName):
    global pageNumber, books_name
    print("old pagenum", pageNumber)
    print(request.form.get("pageInput"))
    
    pageNumber = int(request.form['pageInput'])
    if(pageNumber > len(pages)):
        pageNumber = len(pages)
    print("new pagenum", pageNumber)
    return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, bookName=bookName, dalleImage="https://raw.githubusercontent.com/yasirylmzcbn/IGA/chromeExtension/loading.gif")

# @app.route('/favicon.ico')
# def favicon():
#     return '', 204

# @app.route("/HP")
# def HP():
#     global pageNumber, pages
#     pageNumber = 0
#     read('HP')
#     print("length = ",len(pages))
#     return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, dalleImage="https://github.com/yasirylmzcbn/IGA/blob/chromeExtension/loading.gif")

@app.route("/<string:name>")
def chooseBook(name):
    global pageNumber, pages, books_name
    pageNumber = 0
    books_name = name
    read(name)
    return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, bookName=name, dalleImage="https://raw.githubusercontent.com/yasirylmzcbn/IGA/chromeExtension/loading.gif")


# @app.route("/<string:name>/<int:pageNum>")
# def bookPage(name, pageNum):
#     global pages
#     pageNumber = pageNum
#     reader = PdfReader("books/" + str(name) + ".pdf")
#     read(name)
#     return render_template("testindex.html", pageText=pages[pageNumber], pageNumber=pageNumber, dalleImage="https://github.com/yasirylmzcbn/IGA/blob/chromeExtension/loading.gif")
