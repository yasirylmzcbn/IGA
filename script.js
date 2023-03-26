var apiKey =  "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"

const req = new XMLHttpRequest();
var reply1;
var reply2;


function update(){
  document.getElementById("img").innerHTML = '<img width="400px" height="400px" src="loading.gif"></img>'
  var element = document.getElementById("text");

  req.open('POST', 'https://api.openai.com/v1/chat/completions');
  req.setRequestHeader('Content-Type', 'application/json');
  req.setRequestHeader('Authorization', 'Bearer ' + apiKey);
  req.send(JSON.stringify({
    'model': 'gpt-3.5-turbo',
    'messages': [
      {"role": "system", "content": "You are a helpful assistant that finds a few keywords from a page from a book that is inputted to be used as a prompt for DALL-E to generate images to aid the user in visualizing what's going on in the text. You create a prompt from the keywords in a way that would help the DALL-E AI generate a picture that is like a scene from a movie. Keep the prompt to about a sentence and only include the most important idea from the input."},
      {"role": "user", "content": element.value}
    ],
  }));
  setTimeout(function() {next();}, 2000);
 
}

function next(){
  let json = JSON.parse(req.responseText);
  console.log(json);
  let reply = json['choices'][0]['message']['content'];
  console.log(reply);
  // console.log(reply)

  req.open('POST', 'https://api.openai.com/v1/images/generations');
  req.setRequestHeader('Content-Type', 'application/json');
  req.setRequestHeader('Authorization', 'Bearer ' + apiKey);
  req.send(JSON.stringify({
    "prompt": reply,
    "n":1,
    "size":"1024x1024"
  }));

  setTimeout(function() {next2();}, 7500);

}

function next2() {
  var reply1 = JSON.parse(req.responseText); 
  console.log(reply1);
  let img_url = reply1['data'][0]['url'];
  console.log(img_url)

  document.getElementById("img").innerHTML = '<img width="400px" height="400px" src=' + img_url + '></img>' 
}

window.onload = function () {
  document.getElementById("gen").addEventListener("click", function () {
    update();
  })
};

