# app/utils/wordcloud_generator.py
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_wordcloud(comments):
    text = " ".join(comment.content for comment in comments)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    # Convertir en image base64
    img = BytesIO()
    wordcloud.to_image().save(img, 'PNG')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')