# project: p4
# submitter: zluo43
# partner: jkang96@wisc.edu 
# hours: 15

#The data I chose with my partner is the world hapinness report. It is interesting to see how the perception of hapiness can be measured with data. 





import pandas as pd
from flask import Flask, request, jsonify
import re
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

counts = 1
countA = 0
countB = 0
email_n=0

@app.route('/')
def home():
    global counts
    ratioA =countA/counts
    ratioB =countB/counts
    
    with open("index.html") as f:
        html = f.read()        
    if counts < 11:
        if (counts % 2) == 0:
            counts=counts+1
            return html.replace(
                '<a href="donate.html">donate</a><br><br>',
                '<a style="background-color:red;border-color:black" href="donate.html?from=A">donate</a><br><br>')
        else:
            counts=counts+1
            return html.replace(
                '<a href="donate.html">donate</a><br><br>',
                '<a style="background-color:green;border-color:blue" href="donate.html?from=B">donate</a><br><br>')

    else:

        if ratioA >= ratioB:
            with open("index.html") as f:
                html = f.read()
                htmlA=html.replace('<a href="donate.html">donate</a><br><br>',
                '<a style="background-color:red;border-color:black" href="donate.html">donate</a><br><br>')
                return htmlA

        else:
            with open("index.html") as f:
                html = f.read()
                htmlB=html.replace(
                '<a href="donate.html">donate</a><br><br>',
                '<a style="background-color:green;border-color:blue" href="donate.html">donate</a><br><br>')
                
                return htmlB


@app.route('/browse.html')
def browse():
    main_csv = pd.read_csv("main.csv")
    table=main_csv.to_html()
    header = """
    <h1>Browse</h1>
    """

    return  header+table   #html table 
   

@app.route('/email', methods=["POST"])
def email():
    global email_n
    
    email = str(request.data, "utf-8")
    suffix = r"\.(edu|com|org|net|io)"
    at = r"(@|[aA][tT][AT])"
    opt_brackets = r"[\(\)\{\}\[\]]?"
  
    if re.match(r"(\w+)\s*" + opt_brackets + at + opt_brackets + r"\s*(\w+)" + suffix, email): # 1
        with open("emails.txt", "a") as f: # open file in append mode
                  f.write(email + "\n")
            
                  email_n=email_n+1
            
            
        return jsonify("thanks, you're subscriber number {}!".format(email_n))
    return jsonify("Invalid Email address! Use ur brain!!") #3



@app.route('/donate.html')
def donate():
    
    with open("donate.html") as f:
        html = f.read()    
    if request.args.get("from")=="A":
        global countA
        countA=countA+1
        #print ('a is',countA)
        

    else:
        global countB
        countB=countB+1
        #print ('b is ',countB)
       
    return html




if __name__ == '__main__':
    app.run(host="0.0.0.0")    