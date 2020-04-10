import flask
import pandas as pd


app = flask.Flask(__name__, template_folder='templates')

data_df = pd.read_csv('./model/Data_DF.csv')

counts1 = data_df['UserID'].value_counts()
ratings = data_df[data_df['UserID'].isin(counts1[counts1 >= 10].index)]
counts = data_df['Rate'].value_counts()
ratings = data_df[data_df['Rate'].isin(counts[counts >= 1000].index)]
    
average_rating = pd.DataFrame(data_df.groupby('Course')['Rate'].mean())
average_rating['ratingCount'] = pd.DataFrame(data_df.groupby('Course')['Rate'].count())
average_rating.sort_values('ratingCount', ascending=False)
 
ratings_pivot = ratings.pivot_table(index='UserID', columns='Course').Rate
UserID = ratings_pivot.index
Course = ratings_pivot.columns

data_df= data_df['Course'].unique()

all_titles = []
all_titles = data_df


def get_recommendation(course):
         
    input_ratings = ratings_pivot[course]
    similar_to_course = ratings_pivot.corrwith(input_ratings)
    
    corr_course = pd.DataFrame(similar_to_course,columns=['pearsonR'])
    
    corr_course.dropna(inplace = True)
    
    corr_summary = corr_course.join(average_rating['ratingCount'])
       
    final_recomm = corr_summary[corr_summary['ratingCount']>=300].sort_values('pearsonR' , ascending =False).head(6)
    df = final_recomm.index
    return df


@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
            
    if flask.request.method == 'POST':
        m_name = flask.request.form['course']
        
        result_final = get_recommendation(m_name)
        
        names = []
       
        for i in range(len(result_final)):
                names.append(result_final[i])                
        return flask.render_template('feedback.html',movie_names=names[1::],search_name=m_name)

       
if __name__ == '__main__':
    app.run()
    
    

'''
                                    
                                    WORKING CODE
                                    # Set up the main route
                                    @app.route('/', methods=['GET', 'POST'])
                                    
                                    def main():
                                        if flask.request.method == 'GET':
                                            return(flask.render_template('index.html'))
                                                
                                        if flask.request.method == 'POST':
                                            m_name = flask.request.form['course']
                                            
                                            result_final = get_recommendation(m_name)
                                            print("Got Recoo")         
                                    
                                            return flask.render_template('index.html',prediction_text ='Next Recommended Courses are ${}'.format(result_final))
                                    
                                    if __name__ == '__main__':
                                        app.run()
                                        
                                    '''    
                                    
                                    
                                    # Set up the main route
