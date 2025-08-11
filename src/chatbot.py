import os
import json
from datetime import datetime
from typing import Dict, List
import requests
from dotenv import load_dotenv
load_dotenv()
try:
    from langdetect import detect
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Please run: pip install -r requirements.txt")
    exit(1)

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

class SimpleAITeacher:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("No Groq API key found. Please set GROQ_API_KEY.")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"

        # Languages
        self.languages = {'en': 'English', 'hi': 'Hindi', 'te': 'Telugu'}

        # Subject keywords
        self.subjects = {
            'math': ['math', 'algebra', 'geometry', 'गणित', 'గణితం'],
            'science': ['science', 'physics', 'chemistry', 'विज्ञान', 'శాస్త్రం'],
            'general': []
        }

        # Teacher prompts
        self.teacher_prompts = {
            'en': "You are a helpful teacher. Provide clear explanations with examples.",
            'hi': "आप एक सहायक शिक्षक हैं। उदाहरण के साथ स्पष्ट व्याख्या दें।",
            'te': "మీరు సహాయక ఉపాధ్యాయుడు. ఉదాహరణలతో స్పష్ట వివరణలు ఇవ్వండి।"
        }

        self.history = []

    def transliterate_to_roman(self, text: str, language: str) -> str:
        if language == 'hi':
            return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
        elif language == 'te':
            return transliterate(text, sanscript.TELUGU, sanscript.ITRANS)
        else:
            return text

    def detect_romanized_language(self, text: str) -> str | None:
        # Define some romanized keywords for Hindi and Telugu
        hindi_keywords = ['namaste', 'kaise', 'hai', 'kya', 'koi', 'shiksha', 'padhai', 'sikhao']
        telugu_keywords = ['namaskaram', 'ela', 'unnaru', 'emi', 'telusu', 'chaduvu', 'cheppu']

        text_lower = text.lower()
        words = text_lower.split()

        hindi_count = sum(word in hindi_keywords for word in words)
        telugu_count = sum(word in telugu_keywords for word in words)

        if hindi_count > 0 and hindi_count >= telugu_count:
            return 'hi'
        elif telugu_count > 0 and telugu_count > hindi_count:
            return 'te'
        else:
            return None

    def detect_language(self, text: str) -> str:
        try:
            detected = detect(text)
            return detected if detected in self.languages else 'en'
        except Exception:
            return 'en'

    def categorize_question(self, text: str) -> str:
        text_lower = text.lower()
        for subject, keywords in self.subjects.items():
            if subject != 'general' and any(keyword in text_lower for keyword in keywords):
                return subject
        return 'general'

    def detect_length_preference(self, user_input: str) -> str:
        shorter_keywords = {"short", "brief", "summarize", "in short", "shorter"}
        longer_keywords = {"more", "detailed", "expand", "explain more", "longer"}

        lower_input = user_input.lower()
        if any(k in lower_input for k in shorter_keywords):
            return "short"
        if any(k in lower_input for k in longer_keywords):
            return "long"
        return "normal"

    def build_prompt_with_history(self, user_input: str, length_pref: str, language: str) -> str:
        # Take last 3 exchanges (Q&A) for context
        history_snippet = ""
        for convo in self.history[-3:]:
            history_snippet += f"User: {convo['user_input']}\nTeacher: {convo['response']}\n"

        length_instruction = {
            "short": "Please answer briefly and concisely.",
            "long": "Please provide a detailed explanation with examples.",
            "normal": "Please provide a clear and helpful answer."
        }[length_pref]

        # Base teacher prompt for language
        base_prompt = self.teacher_prompts.get(language, self.teacher_prompts['en'])
        if language != 'en':
            lang_names = {'hi': 'Hindi', 'te': 'Telugu'}
            base_prompt += f" Respond in {lang_names.get(language, language)}."

        full_prompt = f"{base_prompt}\n{length_instruction}\nConversation history:\n{history_snippet}User: {user_input}\nTeacher:"
        return full_prompt

    def get_ai_response(self, question: str, language: str) -> str:
        length_pref = self.detect_length_preference(question)
        transliterate_response = False
        detected_roman_lang = self.detect_romanized_language(question)
        if detected_roman_lang:
            language = detected_roman_lang
            transliterate_response = True

        prompt = self.build_prompt_with_history(question, length_pref, language)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": prompt}
            ],
            "max_tokens": 400,
            "temperature": 0.7
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            data = response.json()
            choices = data.get("choices", [])
            if choices and "message" in choices[0]:
                content = choices[0]["message"].get("content", "").strip()
                if transliterate_response:
                    content = self.transliterate_to_roman(content, language)
                return content
            return ""
        except Exception as e:
            print(f"Groq API error: {e}")
            fallback_response = self.get_fallback_response(question, language)
            if transliterate_response:
                fallback_response = self.transliterate_to_roman(fallback_response, language)
            return fallback_response

    def get_fallback_response(self, question: str, language: str) -> str:
        responses = {
            'en': "I'd love to help you learn! Could you tell me more about what you'd like to know?",
            'hi': "मैं आपकी सीखने में मदद करना चाहूंगा! आप और क्या जानना चाहते हैं?",
            'te': "నేను మీకు నేర్చుకోవడంలో సహాయం చేయాలనుకుంటున్నాను! మీరు మరేమి తెలుసుకోవాలనురాలు?"
        }
        return responses.get(language, responses['en'])

    def chat(self, user_input: str) -> Dict:
        language = self.detect_language(user_input)
        language_name = self.languages.get(language, 'English')
        category = self.categorize_question(user_input)
        response = self.get_ai_response(user_input, language)

        conversation = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_input': user_input,
            'language': language,
            'language_name': language_name,
            'category': category,
            'response': response
        }
        self.history.append(conversation)
        return conversation

    def get_stats(self) -> Dict:
        if not self.history:
            return {'total_messages': 0, 'languages_used': [], 'subjects_discussed': []}
        languages = list(set(conv['language'] for conv in self.history))
        subjects = list(set(conv['category'] for conv in self.history))
        return {
            'total_messages': len(self.history),
            'languages_used': languages,
            'subjects_discussed': subjects
        }

    def clear_history(self):
        self.history = []
