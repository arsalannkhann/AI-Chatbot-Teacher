
# AI Chatbot Teacher

A simple AI-powered chatbot that acts like a teacher, supporting English, Hindi, and Telugu languages with intelligent responses.  
Built with Python, Streamlit, and Groq API for fast, reliable language model inference.

---

## Features

- **Multilingual Support:**  
  Understands English, Hindi, and Telugu inputs. Detects language automatically.

- **Romanized Language Detection:**  
  Detects Hindi and Telugu typed in Latin script (romanized input) and responds in the corresponding language transliterated back into Roman script.

- **Transliteration:**  
  Responses in Hindi and Telugu are transliterated from native scripts (Devanagari, Telugu) into readable Roman script when the input is romanized.

- **Contextual Memory:**  
  Maintains recent conversation history (last 3 Q&A) to provide coherent and context-aware answers.

- **Length Preference:**  
  Detects if the user requests shorter or longer answers using keywords like "short", "brief", "detailed", etc., and adjusts response length accordingly.

- **Subject Categorization:**  
  Classifies questions into subjects such as Math, Science, and General for more structured answers.

- **Chat History in UI:**  
  Streamlit interface stores and displays chat history with timestamps.  
  Features to **Clear Chat History** and **Download Chat History** as a text file.

- **Powered by Groq API:**  
  Uses Groq's hosted language model API (`llama3-8b-8192` by default) for AI-powered response generation.  

---

## Setup Instructions

### Requirements

- Python 3.8 or higher  
- [Streamlit](https://streamlit.io/)  
- Groq API key ([Get one here](https://www.groq.com/))  
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone this repo:  
   ```bash
   git clone https://github.com/yourusername/AI-Chatbot-Teacher.git
   cd AI-Chatbot-Teacher
   ```

2. Create and activate a virtual environment (optional but recommended):  
   ```bash
   python -m venv chatbot_env
   source chatbot_env/bin/activate  # Linux/Mac
   chatbot_env\Scripts\activate     # Windows
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

4. Set your Groq API key as an environment variable:  
   ```bash
   export GROQ_API_KEY="your_api_key_here"  # Linux/Mac
   setx GROQ_API_KEY "your_api_key_here"    # Windows PowerShell
   ```

5. Run the Streamlit app:  
   ```bash
   streamlit run app.py
   ```

---

## Usage

- Type your questions in English, Hindi, or Telugu.  
- You can also type Hindi or Telugu using English letters (Romanized). The chatbot will detect and respond accordingly.  
- Use phrases like "Give me a shorter answer" or "Explain in detail" to get responses tailored in length.  
- View your full chat history on the UI, clear it anytime, or download it for later reference.

---

## Project Structure

```
AI-Chatbot-Teacher/
├── src/
│   └── chatbot.py           # Core chatbot logic with language detection, transliteration, Groq API calls
├── app.py                   # Streamlit UI application
├── cli.py                   # Command-line interface for the chatbot
├── requirements.txt         # Python dependencies
├── README.md                # This documentation
└── .env                     # Environment variables

```

---

## Dependencies

- `streamlit`  
- `requests`  
- `langdetect`  
- `indic-transliteration`  
- `python-dotenv`  
- And others listed in `requirements.txt`

---

## Notes

- The Groq API is used for inference; ensure your API key is valid and has sufficient quota.  
- The chatbot limits context to the last 3 messages for performance and prompt size constraints.  
- Transliteration uses the `indic-transliteration` library.

---

## License

MIT License

---

Feel free to contribute, raise issues, or request features!

---

**Created by Arsalan Khan**
