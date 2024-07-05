from flask import Flask, render_template, jsonify
import pandas as pd
import json
import random

app = Flask(__name__)

# Load your data
df = pd.read_csv('updated_df.csv')
likes_df = pd.read_csv('filtered_likes.csv')
comments_df=pd.read_csv('filtered_comments.csv')
repost_df=pd.read_csv('filtered_reposts.csv')

@app.route('/api/analyze-likes')
def api_analyze_likes():
    original_likes_data = df['Likes'].dropna().tolist()
    filtered_likes_data = likes_df['Likes'].dropna().tolist()

    response_data = {
        'filtered_likes_data': filtered_likes_data,
        'original_likes_data': original_likes_data
    }
    
    return jsonify(response_data)

@app.route('/api/scatter-likes')
def api_scatter_likes():
    lower_bound = likes_df['Likes'].quantile(0.05)
    upper_bound = likes_df['Likes'].quantile(0.95)

    scatter_data = df[['Username', 'Likes']].copy()
    scatter_data['Unreliable'] = (df['Likes'] < lower_bound) | (df['Likes'] > upper_bound)

    scatter_data['Likes'] = scatter_data['Likes'].replace({float('nan'): None})

    response_data = {
        'scatter_data': scatter_data.to_dict(orient='records'),
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }
    
    return jsonify(response_data)



@app.route('/analyze-likes')
def analyze_likes():
    return render_template('likes_page.html')


@app.route('/api/analyze-comments')
def api_analyze_comments():
    original_comments_data = df['Comments'].dropna().tolist()
    filtered_comments_data = comments_df['Comments'].dropna().tolist()

    response_data = {
        'filtered_comments_data': filtered_comments_data,
        'original_comments_data': original_comments_data
    }
    
    return jsonify(response_data)

@app.route('/api/scatter-comments')
def api_scatter_comments():
    lower_bound = comments_df['Comments'].quantile(0.05)
    upper_bound = comments_df['Comments'].quantile(0.95)

    scatter_data = df[['Username', 'Comments']].copy()
    scatter_data['Unreliable'] = (df['Comments'] < lower_bound) | (df['Comments'] > upper_bound)

    scatter_data['Comments'] = scatter_data['Comments'].replace({float('nan'): None})
    
    response_data = {
        'scatter_data': scatter_data.to_dict(orient='records'),
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }
    
    return jsonify(response_data)

@app.route('/analyze-comments')
def analyze_comments():
    return render_template('comments_page.html')


@app.route('/api/analyze-repost')
def api_analyze_repost():
    original_repost_data = df['Repost'].dropna().tolist()
    filtered_repost_data = repost_df['Repost'].dropna().tolist()

    response_data = {
        'original_repost_data': original_repost_data,
        'filtered_repost_data': filtered_repost_data
    }
    
    return jsonify(response_data)

@app.route('/api/scatter-repost')
def api_scatter_repost():
    lower_bound = repost_df['Repost'].quantile(0.05)
    upper_bound = repost_df['Repost'].quantile(0.95)

    scatter_data = df[['Username', 'Repost']].copy()
    scatter_data['Unreliable'] = (df['Repost'] < lower_bound) | (df['Repost'] > upper_bound)

    scatter_data['Repost'] = scatter_data['Repost'].replace({float('nan'): None})

    response_data = {
        'scatter_data': scatter_data.to_dict(orient='records'),
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }
    
    return jsonify(response_data)


@app.route('/analyze-repost')
def analyze_repost():
    return render_template('repost_page.html')

@app.route('/api/pie-chart-data')
def pie_chart_data():
    
    data = {
        "Likes": df['Likes'].sum(),
        "Comments": df['Comments'].sum(),
        "Reposts": df['Repost'].sum()
    }
    return jsonify(data)

@app.route('/api/bar-chart-data')
def bar_chart():
    colors = ['#FF6347', '#1E90FF', '#32CD32']  
    random.shuffle(colors)

    avg_likes = likes_df['Likes'].mean()
    avg_comments = comments_df['Comments'].mean()
    avg_reposts = repost_df['Repost'].mean()

    bar_chart_data = {
        'categories': ['Average No. of Likes', 'Average No. of Comments', 'Average No. of Reposts'],
        'values': [avg_likes, avg_comments, avg_reposts],
        'colors': colors  
    }
    return jsonify(bar_chart_data)

@app.route('/')
def home():
    return render_template('index.html')


