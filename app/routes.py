from app import app
from flask import redirect, render_template, request
from app.fire_detection import detect_fire_in_img
from app.chat import get_chat_response

import os

#home route
@app.route('/')
def home():
    print("home")
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])  
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        response="res"
        response = get_chat_response(user_input, '/home/keerthana/Desktop/Fire Detection and Alarming System/documentation/doc.pdf')
        return render_template('chat.html', response=response)
    return render_template('chat.html')  

    
# route to detect fire and renders result to index page
@app.route('/detect',methods=['POST'])
def detect():
    print("model")
    if 'file' not in request.files:
        return redirect(request.url)
    file=request.files['file']
    if file.filename=='':
        return redirect(request.url)
    if file:
        file_path=os.path.join('static/uploads',file.filename)
        file.save(file_path)
        prediction=detect_fire_in_img(file_path)
        if prediction==0:
            result='fire detected'
        else:
            result="no fire"
        return render_template('index.html',result=result,img_path=file_path)
    return redirect(request.url)
    
