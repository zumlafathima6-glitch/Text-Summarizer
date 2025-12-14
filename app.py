from flask_cors import CORS
from flask import Flask, request, jsonify
import re, numpy as np, networkx as nx
from nltk.corpus import stopwords
from scipy.spatial.distance import cosine as cosine_distance
import nltk
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)
# ----------- Summarizer Functions -----------

def read_user_text(text):
    # Split text by period to get sentences
    lines = text.split(".")
    sentences = []
    for line in lines:
        # Keep letters and spaces only; remove other punctuation
        cleaned = re.sub(r'[^a-zA-Z ]', '', line)
        words = cleaned.split()
        if words:
            sentences.append(words)
    return sentences

def sentence_similarity(sent1, sent2, stop_words=None):
    if stop_words is None:
        stop_words=[]
    # Convert to lowercase and remove stopwords
    sent1=[w.lower() for w in sent1 if w.lower() not in stop_words]
    sent2=[w.lower() for w in sent2 if w.lower() not in stop_words]
    all_words=list(set(sent1+sent2))
    vector1=[0]*len(all_words)
    vector2=[0]*len(all_words)
    for w in sent1:
        vector1[all_words.index(w)]+=1
    for w in sent2:
        vector2[all_words.index(w)]+=1
    if cosine_distance(vector1,vector2)==0:
        return 1
    return 1-cosine_distance(vector1,vector2)

def gen_sim_matrix(sentences, stop_words):
    n=len(sentences)
    sim_matrix=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i!=j:
                sim_matrix[i][j]=sentence_similarity(sentences[i], sentences[j], stop_words)
    return sim_matrix

def generate_summary(text):
    stop_words = stopwords.words('english')
    sentences = read_user_text(text)
    if len(sentences)==0:
        return "❌ No sentences found!"
    sim_matrix=gen_sim_matrix(sentences, stop_words)
    graph=nx.from_numpy_array(sim_matrix)
    scores=nx.pagerank(graph)
    ranked=sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    top_n=max(1,int(len(sentences)*0.4))
    summary=[" ".join(ranked[i][1]) for i in range(top_n)]
    return ". ".join(summary) + "."

# ----------- Flask Routes -----------

@app.route("/", methods=["GET"])
def home():
    return "Flask server is running! Use POST to /summarize with your text."

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text","")
    summary = generate_summary(text)
    return jsonify({"summary": summary})

# ----------- Run Server -----------

if __name__=="__main__":
    app.run(debug=True)
