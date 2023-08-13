from flask import Flask,render_template,request
import pickle
import numpy as np
popular_df = pickle.load(open('popular2.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['title'].values),
                           author=list(popular_df['authors'].values),
                           image=list(popular_df['thumbnail'].values),
                           categories=list(popular_df['categories'].values),
                           rating=list(popular_df['average_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    # index fetch
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:9]
    
    data2 = []
    for i in similar_items:
        item = []
        temp_df = popular_df[popular_df['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['authors'].values))
        item.extend(list(temp_df.drop_duplicates('title')['thumbnail'].values))
        item.extend(list(temp_df.drop_duplicates('title')['categories'].values))
        
        data2.append(item)
    print(data2)

    return render_template('recommend.html',data=data2)

if __name__ == '__main__':
    app.run(debug=True)