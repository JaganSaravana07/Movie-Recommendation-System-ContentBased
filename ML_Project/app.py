from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))
overview = model[0]
genre = model[1]

def clean_data(x):
   if isinstance(x, list):
      return [str.lower(i.replace(" ", "")) for i in x]
   else:
      #Check if director exists. If not, return empty string
      if isinstance(x, str):
         return str.lower(x.replace(" ", ""))
      else:
         return ''

def overviewbased(idx):
   sig_scores = list(enumerate(overview[idx]))
   sig_scores = sorted(sig_scores,key=lambda x: x[1], reverse=True)
   # Get the movie indices
   mov_indices = [i[0] for i in sig_scores[1:11]]
   # Return the top 10 most similar movies
   fd =  df[['Title','Poster_Url']].iloc[mov_indices]
   arr = []
   for row in fd.iterrows():
      arr.append(row[1]["Title"])

   if(not(len(arr))):
      arr[0] = 0
   
   return arr

def genrebased(idx):
   sig_scores = list(enumerate(genre[idx]))
   sig_scores = sorted(sig_scores,key=lambda x: x[1], reverse=True)
   # Get the movie indices
   mov_indices = [i[0] for i in sig_scores[2:12]]
   # Return the top 10 most similar movies
   fd =  df[['Title','Poster_Url']].iloc[mov_indices]
   arr = []
   for row in fd.iterrows():
      arr.append(row[1]["Title"])

   if(not(len(arr))):
      arr[0] = 0
   
   return arr

def storybased(idx):
   sig_scores = list(enumerate(overview[idx] * 0.5 + genre[idx] * 0.5))
   sig_scores = sorted(sig_scores,key=lambda x: x[1], reverse=True)
   # Get the movie indices
   mov_indices = [i[0] for i in sig_scores[1:11]]
   # Return the top 10 most similar movies
   fd =  df[['Title','Poster_Url']].iloc[mov_indices]
   arr = []
   for row in fd.iterrows():
      arr.append(row[1]["Title"])
   
   if(not(len(arr))):
      arr[0] = 0
   
   return arr


#<----------------------------------- PAGE REDIRECTING ------------------------------------>


@app.route('/')
@app.route('/home')
def home():
   return render_template('index.html')

@app.route("/result",methods = ['POST',"GET"])
def result():
   choice = int(request.form['choice'])
   title = request.form['name']
   if(title == " "):
      return render_template("index.html")


   else:
      indices = pd.Series(df.index, index=df['Title']).drop_duplicates()  
      idx = indices[title]
      if(choice == 1):
         return render_template("output.html",name = overviewbased(idx), choice = choice)
      elif(choice == 2):
         return render_template("output.html",name = genrebased(idx), choice = choice)
      elif(choice == 3):
         return render_template("output.html",name = storybased(idx), choice = choice)
      else:
         return render_template("index.html")



#<---------------------------------------- MAIN FLOW ------------------------------------------->


if __name__ == '__main__':
   df = pd.read_csv("Movies.csv", lineterminator = "\n")
   df['Overview'] = df['Overview'].fillna('')
   df['Genre'] = df['Genre'].apply(clean_data)
   app.run(debug = True)