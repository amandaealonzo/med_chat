from flask import Flask, render_template, request, url_for
import sys 
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import nltk
import string
from nltk.corpus import stopwords
import spacy
import chatterbot_corpus
import yaml

app = Flask(__name__)

# python -m spacy download en_core_web_sm
  
# Create object of ChatBot class with Storage Adapter
bot = ChatBot('Doctor',   read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
        ],
)

trainer = ChatterBotCorpusTrainer(bot)
# put the yaml file under: \.venv\Lib\site-packages\chatterbot_corpus\data\custom
# todo: change from short for prod
#  only do this once for web app because takes some times
trainer.train("chatterbot.corpus.custom.medical_short")

@app.route('/')
def homepage():
    return render_template("chat.html")

@app.route('/chat/', methods=["POST","GET"])
def chat():
    user_question = request.form['t1']    
    this_bot_answer = find_answer(user_question) 
    #return "<h2>Bot Response: %s</h2>"%(this_bot_answer)
    return render_template("chat.html", bot_answer = this_bot_answer, user_question=user_question)


def find_answer(t1):    
    answer = bot.get_response(t1)
    return answer

if __name__ == "__main__":
    app.run()