from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import traceback
import time
import random
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
HF_TOKEN = os.getenv("HF_TOKEN")

DEBUG_MODE = True

# Enhanced model list with better creative writing models
MODELS = [
    "microsoft/DialoGPT-medium",
    "gpt2",
    "EleutherAI/gpt-neo-1.3B",
    "facebook/opt-1.3b",
    "bigscience/bloom-560m"
]

def log_debug(message):
    """Enhanced logging function"""
    if DEBUG_MODE:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

def call_huggingface_api(prompt, model_name, category, max_retries=3):
    """Enhanced API call with better error handling and category-specific parameters"""
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Category-specific parameters
    if category.lower() == "poem":
        params = {
            "max_new_tokens": 150,
            "temperature": 0.8,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False,
            "repetition_penalty": 1.2
        }
    elif category.lower() == "dialogue":
        params = {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False,
            "repetition_penalty": 1.1
        }
    else:  # story
        params = {
            "max_new_tokens": 250,
            "temperature": 0.75,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False,
            "repetition_penalty": 1.1
        }
    
    payload = {
        "inputs": prompt,
        "parameters": params
    }
    
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    log_debug(f"Trying model: {model_name}")
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=35)
            log_debug(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                log_debug(f"API Response: {result}")
                
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    generated_text = result.get("generated_text", "")
                else:
                    generated_text = str(result)
                
                if generated_text and len(generated_text.strip()) > 10:
                    return clean_generated_text(generated_text, category)
                    
            elif response.status_code == 503:
                log_debug(f"Model {model_name} is loading, attempt {attempt + 1}")
                wait_time = 15 + (attempt * 5)  # Progressive backoff
                time.sleep(wait_time)
                continue
                
            elif response.status_code == 429:
                log_debug("Rate limit hit, waiting...")
                time.sleep(20)
                continue
                
            else:
                log_debug(f"API Error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            log_debug(f"Timeout on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                time.sleep(10)
            continue
        except Exception as e:
            log_debug(f"Request error: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(5)
            continue
    
    return None

def clean_generated_text(text, category):
    """Clean and format generated text based on category"""
    if not text:
        return ""
    
    text = text.strip()
    
    # Remove common prefixes that models might add
    prefixes_to_remove = [
        "Once upon a time,", "Story:", "Poem:", "Dialogue:",
        "Here's a story:", "Here's a poem:", "Here's a dialogue:"
    ]
    
    for prefix in prefixes_to_remove:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    
    # Category-specific cleaning
    if category.lower() == "poem":
        # Ensure proper line breaks for poems
        text = text.replace(". ", ".\n")
        text = text.replace("! ", "!\n")
        text = text.replace("? ", "?\n")
    
    # Limit length
    if len(text) > 800:
        text = text[:800] + "..."
    
    return text

def create_enhanced_fallback_content(prompt, category):
    """Enhanced fallback content with more variety"""
    
    story_templates = [
        f"The morning air was crisp when Elena first encountered {prompt}. She had been walking through the old district, lost in thought, when something extraordinary caught her attention. The way the light danced around it seemed almost magical, as if the universe itself was trying to tell her something important. This was the beginning of an adventure that would change her understanding of the world forever.",
        
        f"Marcus had always been skeptical about {prompt}, but today was different. As he stood in the dusty library, surrounded by ancient books, he discovered something that challenged everything he believed. The leather-bound journal in his hands seemed to pulse with energy, its pages filled with secrets that had been waiting decades to be revealed.",
        
        f"In the small town of Millbrook, {prompt} was considered nothing more than a legend. But when the storms came and the power went out, Sarah found herself face-to-face with a truth that would shake the foundation of her reality. The old lighthouse keeper had been right all along – some mysteries are meant to be solved.",
        
        f"The antique shop at the corner of Fifth and Main had always been peculiar, but today it held something extraordinary. When David stepped inside, drawn by an inexplicable force, he discovered {prompt} waiting for him. The shopkeeper's knowing smile suggested this encounter was no mere coincidence."
    ]
    
    poem_templates = [
        f"In whispered winds of {prompt} bright,\nA tale unfolds in morning light,\nWhere dreams and reality dance as one,\nAnd magic flows till day is done.\n\nThe world transforms with each heartbeat,\nAs wonder makes our souls complete,\nAnd in this dance of hope and fear,\nWe find the truth we hold most dear.\n\nOh {prompt}, mysterious and grand,\nYou guide us with your gentle hand,\nThrough shadows deep and sunlight warm,\nYou are our shelter in the storm.",
        
        f"Beneath the stars of {prompt} gleaming,\nA poet sits in quiet dreaming,\nOf worlds beyond our earthly sight,\nWhere darkness transforms into light.\n\nThe gentle breeze carries whispers,\nOf secrets that the moonlight glistens,\nAnd in this sacred, silent hour,\nWe feel {prompt}'s ancient power.\n\nSo let us pause and listen well,\nTo stories that the heavens tell,\nFor in their song, we find our way,\nTo greet the dawn of each new day.",
        
        f"Like morning dew on petals bright,\n{prompt} brings forth new sight,\nA vision of what we might become,\nWhen all our scattered dreams are one.\n\nThe river flows with endless grace,\nReflecting every human face,\nAnd in its depths, we come to see,\nThe beauty of our destiny.\n\nOh {prompt}, you are the key,\nTo unlock our humanity,\nIn your embrace, we find our voice,\nAnd know that love is always choice."
    ]
    
    dialogue_templates = [
        f'"I\'ve been thinking about {prompt} lately," Maya said, stirring her coffee thoughtfully.\n\n"Really? What about it?" her friend Alex asked, leaning forward with interest.\n\n"Well, I used to think it was just a concept, something abstract. But now I\'m starting to believe it might be more real than we ever imagined."\n\n"That\'s fascinating. What changed your mind?"\n\n"Yesterday, I experienced something that made me question everything I thought I knew. It was like {prompt} was trying to communicate with me directly."\n\n"That sounds incredible. Tell me more."',
        
        f'"Professor Chen, what do you think about {prompt}?" the student asked after class.\n\n"That\'s a profound question, Jamie. In my thirty years of research, I\'ve come to believe that {prompt} represents something fundamental about human nature."\n\n"But how can we be sure it\'s real and not just wishful thinking?"\n\n"The evidence is all around us, if we know how to look. {prompt} manifests in ways that science is only beginning to understand."\n\n"Could you give me an example?"\n\n"Consider how {prompt} appears in different cultures throughout history. The consistency is remarkable."',
        
        f'"You know," David said, watching the sunset, "I never really understood {prompt} until today."\n\n"What happened today that was so special?" his sister Emma asked.\n\n"I met someone who embodies everything {prompt} represents. It was like seeing a living example of something I\'d only read about in books."\n\n"That must have been quite an experience."\n\n"It was transformative. I finally understand why ancient philosophers spent so much time contemplating {prompt}. It\'s not just an idea – it\'s a way of being in the world."'
    ]
    
    templates = {
        "story": story_templates,
        "poem": poem_templates,
        "dialogue": dialogue_templates
    }
    
    category_templates = templates.get(category.lower(), story_templates)
    return random.choice(category_templates)

def create_enhanced_prompt(prompt, category):
    """Create better prompts based on category"""
    if category.lower() == "story":
        return f"Write a compelling short story about {prompt}. Make it vivid and engaging:\n\n"
    elif category.lower() == "poem":
        return f"Write a beautiful, lyrical poem about {prompt}:\n\n"
    elif category.lower() == "dialogue":
        return f"Write an engaging dialogue between two characters discussing {prompt}:\n\n"
    else:
        return f"Write creatively about {prompt}:\n\n"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        log_debug(f"Received request: {data}")
        
        prompt = data.get("prompt", "").strip()
        category = data.get("category", "story").strip()

        if not prompt:
            return jsonify({"result": "⚠️ Please enter a prompt to generate content."})

        if len(prompt) > 500:
            return jsonify({"result": "⚠️ Please keep your prompt under 500 characters."})

        # Create enhanced prompt
        full_prompt = create_enhanced_prompt(prompt, category)
        log_debug(f"Generated prompt: {full_prompt}")

        # Try multiple models
        generated_text = None
        successful_model = None
        
        for model_name in MODELS:
            log_debug(f"Attempting with model: {model_name}")
            generated_text = call_huggingface_api(full_prompt, model_name, category)
            
            if generated_text and len(generated_text.strip()) > 20:
                successful_model = model_name
                log_debug(f"Success with model: {model_name}")
                break
            else:
                log_debug(f"Failed with model: {model_name}")
                continue
        
        # Use enhanced fallback if all models fail
        if not generated_text or len(generated_text.strip()) < 20:
            log_debug("All models failed, using enhanced fallback")
            generated_text = create_enhanced_fallback_content(prompt, category)
            
        log_debug(f"Final response length: {len(generated_text)}")
        
        return jsonify({
            "result": generated_text,
            "model_used": successful_model,
            "category": category
        })

    except Exception as e:
        log_debug(f"Error in generate: {str(e)}")
        traceback.print_exc()
        
        # Enhanced fallback error handling
        try:
            fallback_prompt = data.get("prompt", "imagination") if 'data' in locals() else "imagination"
            fallback_category = data.get("category", "story") if 'data' in locals() else "story"
            fallback_content = create_enhanced_fallback_content(fallback_prompt, fallback_category)
            
            return jsonify({
                "result": fallback_content,
                "model_used": "fallback",
                "category": fallback_category
            })
        except:
            return jsonify({
                "result": "Welcome to InspireWrite! Let your creativity flow and try again with an inspiring prompt.",
                "model_used": "fallback",
                "category": "story"
            })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "available_models": len(MODELS)
    })

if __name__ == "__main__":
    log_debug("Starting InspireWrite Creative Generator...")
    log_debug(f"Available models: {MODELS}")
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=5000)