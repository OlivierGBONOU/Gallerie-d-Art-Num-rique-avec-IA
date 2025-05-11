# Module d’analyse NLP (émotions + mots-clés)
# app/utils/emotion_analysis.py
from transformers import pipeline

# Charger le modèle pré-entraîné pour la classification des émotions
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def analyze_emotion(text):
    """
    Analyse le texte et retourne l’émotion dominante (ex. 'joy', 'sadness').
    """
    result = emotion_classifier(text)
    return result[0]['label']