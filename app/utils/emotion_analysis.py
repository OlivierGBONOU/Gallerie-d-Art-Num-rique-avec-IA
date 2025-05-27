# Module d’analyse NLP (émotions + mots-clés)
# app/utils/emotion_analysis.py
from transformers import pipeline
from langdetect import detect
from deep_translator import GoogleTranslator

def analyze_emotion(text):
    """
    Analyse le texte et retourne l’émotion dominante (ex. 'joy', 'sadness').
    Détecte la langue du texte et le traduit en anglais si nécessaire.
    
    Args:
        text (str): Texte à analyser.
    
    Returns:
        str: Émotion dominante détectée.
    """
    # Initialiser le classificateur d'émotion (en anglais)
    emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
    
    try:
        lang = detect(text)
        
        if lang != 'en':
            translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        else:
            translated_text = text
        
        # Analyser l'émotion sur le texte traduit
        result = emotion_classifier(translated_text)
        return result[0]['label']
    
    except Exception as e:
        return f"Erreur lors de l'analyse : {str(e)}"