import os
import time
import json
import uuid
import random
import socket
import requests
import hashlib
import urllib.parse
from urllib.parse import urlparse
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from textblob import TextBlob
from newspaper import Article, Config
from duckduckgo_search import DDGS
from blockchain.blockchain import Blockchain # Ensure your blockchain.py is in a folder named 'blockchain'

app = Flask(__name__)

# --- CONFIGURATION ---
GENAI_API_KEY = "YOUR_API_KEY"
try:
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    print("Success: Connected to Gemini 2.5 Flash!")
except Exception as e:
    print(f"Warning: Gemini Setup Issue. {e}")

blockchain = Blockchain()
node_identifier = str(uuid.uuid4()).replace('-', '')

# --- REAL-TIME STATS COUNTER ---
SYSTEM_STATS = {
    'scans': 0,
    'threats': 0,
    'nodes': 1,
    'defcon': "LEVEL 5 (LOW)"
}

# --- HELPER FUNCTIONS ---

def get_real_server_location(url):
    """Dynamically resolves domain to IP and fetches real geolocation."""
    if not url or url == 'text':
        return "N/A (Text Input)"
    try:
        domain = urlparse(url).netloc.lower()
        if not domain:
            domain = url
            
        ip = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if response.get("status") == "success":
            city = response.get('city', 'Unknown')
            country = response.get('country', 'Unknown')
            isp = response.get('isp', 'Unknown')
            return f"{city}, {country} (ISP: {isp}) [IP: {ip}]"
    except Exception as e:
        print(f"Location Error: {e}")
    return "Location Unverified / Hidden Behind Proxy"

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = (blob.sentiment.polarity + 1) * 50 
    bias = blob.sentiment.subjectivity * 100
    return round(sentiment, 1), round(bias, 1)

def scrape_url(url):
    try:
        config = Config()
        config.browser_user_agent = 'Mozilla/5.0'
        config.request_timeout = 5
        article = Article(url, config=config)
        article.download()
        article.parse()
        return f"{article.title}. {article.text}"[:4000]
    except: 
        return None

def search_web_agent(query):
    """Uses DuckDuckGo to find sources. Falls back to Google Search link if blocked."""
    sources = []
    context = ""
    try:
        results = DDGS().text(query, max_results=3)
        if results:
            for r in results:
                sources.append({"title": r['title'], "url": r['href']})
                context += f"Source ({r['href']}): {r['body']}\n"
    except Exception as e:
        print(f"Search API Blocked/Failed: {e}")

    # FAIL-SAFE: If no sources found, generate manual Google link
    if not sources:
        encoded_query = urllib.parse.quote(query)
        sources.append({
            "title": "⚠️ Live Search Blocked: Click to Verify on Google", 
            "url": f"https://www.google.com/search?q={encoded_query}"
        })
        context += "Context unavailable (Search rate-limited)."
        
    return sources, context

def analyze_with_gemini(text, url, search_context):
    """Uses LLM to determine veracity and calculate factual entailment."""
    prompt = f"""
    You are an expert fact-checking and cyber-threat analysis AI.
    Analyze the following content for misinformation, satire, or malicious intent.
    
    Content: "{text[:2000]}"
    URL/Domain (if any): "{url}"
    Live Web Context: "{search_context[:2000]}"
    
    TASK:
    1. Determine if the content is Real, Fake, or Malicious.
    2. Calculate a 'Factual Entailment Confidence Score' (0-100).
    
    Respond STRICTLY in valid JSON format:
    {{
        "verdict": "Real",
        "confidence": 95,
        "explanation": "Provide a detailed 2-sentence reason pointing to specific facts.",
        "abstract": "Provide a 1-sentence summary for the blockchain ledger."
    }}
    """
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"Gemini Parsing Error: {e}")
        return {"verdict": "Unsure", "confidence": 50, "explanation": "AI Analysis failed.", "abstract": "Log: Unverified."}

def update_system_defcon():
    ratio = SYSTEM_STATS['threats'] / max(1, SYSTEM_STATS['scans'])
    if ratio > 0.5: SYSTEM_STATS['defcon'] = "LEVEL 1 (CRITICAL)"
    elif ratio > 0.2: SYSTEM_STATS['defcon'] = "LEVEL 2 (HIGH)"
    elif ratio > 0.05: SYSTEM_STATS['defcon'] = "LEVEL 3 (ELEVATED)"
    else: SYSTEM_STATS['defcon'] = "LEVEL 5 (LOW)"

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify_news():
    SYSTEM_STATS['scans'] += 1
    data = request.get_json()
    user_input = data.get('text', '').strip()
    input_type = data.get('type', 'text')
    
    if not user_input: return jsonify({'error': 'No input provided'}), 400

    news_text = user_input
    url = user_input if input_type == 'url' else 'text'
    
    # 1. Scrape & Gather Live Context
    if input_type == 'url':
        scraped = scrape_url(user_input)
        if scraped: news_text = scraped
    
    sources, search_context = search_web_agent(news_text[:150])

    # 2. Real Geolocation
    server_loc = get_real_server_location(url)

    # 3. AI Analysis
    ai_result = analyze_with_gemini(news_text, url, search_context)
    prediction = ai_result.get("verdict", "Unsure")
    confidence = ai_result.get("confidence", 50)
    
    # 4. Threat Metrics
    if prediction in ["Fake", "Malicious"]:
        SYSTEM_STATS['threats'] += 1
        cyber_report_id = f"CYBER-INCIDENT-{random.randint(10000,99999)}" if prediction == "Malicious" else None
    else:
        cyber_report_id = None
        
    update_system_defcon()
    sentiment_score, bias_score = analyze_sentiment(news_text)
    
    # 5. Blockchain Anchoring
    try:
        last_block = blockchain.last_block
        block = blockchain.new_block(proof=123, previous_hash=last_block['previous_hash'])
        block_hash = blockchain.hash(block)
    except Exception:
        block_hash = hashlib.sha256(str(time.time()).encode()).hexdigest()

    return jsonify({
        'prediction': prediction, 
        'confidence': f"{confidence}%", 
        'explanation': ai_result.get("explanation", "Analyzed."),
        'sources': sources, 
        'block_hash': block_hash, 
        'stored_abstract': ai_result.get("abstract", "Logged."),
        'cyber_report_id': cyber_report_id, 
        'server_location': server_loc, 
        'sentiment': sentiment_score, 
        'bias': bias_score
    }), 200

@app.route('/lookup', methods=['POST'])
def lookup_hash():
    data = request.get_json()
    target_hash = data.get('hash', '')
    
    try:
        for block in blockchain.chain:
            recalculated_hash = blockchain.hash(block)
            if recalculated_hash == target_hash or block.get('previous_hash') == target_hash:
                is_tampered = (recalculated_hash != target_hash) and (block.get('hash') == target_hash)
                return jsonify({
                    'found': True, 'tampered': is_tampered,
                    'block_index': block.get('index', 'N/A'), 
                    'timestamp': block.get('timestamp', time.time()), 
                    'transactions': block.get('transactions', [])
                })
    except Exception as e: print(f"Blockchain Error: {e}")
    return jsonify({'found': False, 'message': 'Hash not found.'}), 404

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'scans_today': SYSTEM_STATS['scans'],
        'threats_blocked': SYSTEM_STATS['threats'],
        'nodes_active': SYSTEM_STATS['nodes'],
        'defcon': SYSTEM_STATS['defcon']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
