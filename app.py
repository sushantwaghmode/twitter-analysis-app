from flask import Flask, render_template,request
from python import AccessTwitter
import matplotlib.pyplot as plt
import time
import pandas as pd
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/processed.html',methods=['GET','POST'])
def processed():
    if request.method == 'POST':
        search = request.form['key']
        (sentiment_bar,sentiment_pie,word_cloud,n,s)=AccessTwitter(search)
        sentiment_bar.value_counts().plot(kind='bar')
        plt.title('Sentiment analysis')
        plt.ylabel('counts')
        plt.xlabel('sentiment')
        for filename in os.listdir('static/'):
            if filename.startswith('bar_'): 
                os.remove('static/' + filename)
        barchart = "bar" + str(time.time()) + ".png"
        plt.savefig('static/' + barchart,bbox_inches='tight')
        plt.close()

        sentiment_pie.value_counts().plot(kind='pie',autopct='%1.0f%%',pctdistance=1.3,labeldistance=1.5)
        for filename in os.listdir('static/'):
            if filename.startswith('pie_'): 
                os.remove('static/' + filename)
        piechart = "pie" + str(time.time()) + ".png"
        plt.savefig('static/' + piechart,bbox_inches='tight')
        plt.close()

        plt.imshow(word_cloud,interpolation='bilinear')
        plt.axis('off')
        for filename in os.listdir('static/'):
            if filename.startswith('word_cloud_'): 
                os.remove('static/' + filename)
        word_cloud_ = "word_cloud" + str(time.time()) + ".png"
        plt.savefig('static/' +word_cloud_,bbox_inches='tight')
        plt.close()

        plt.barh(n,s)
        plt.xlabel('Word')
        plt.ylabel("Frequency")
        for filename in os.listdir('static/'):
            if filename.startswith('word_count_'): 
                os.remove('static/' + filename)
        word_count_ = "word_count" + str(time.time()) + ".png"
        plt.savefig('static/' +word_count_,bbox_inches='tight')
        plt.close()

        return render_template('processed.html',barfig=barchart,piefig =piechart ,word_cloudfig=word_cloud_,word_countfig=word_count_)
     
   

if __name__ == "__main__":
    app.run(debug=True)
