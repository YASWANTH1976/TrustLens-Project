import google.generativeai as genai

# PASTE YOUR KEY HERE
api_key = "YOUR_API_KEY"

genai.configure(api_key=api_key)

print("Checking available models for your key...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ AVAILABLE: {m.name}")
except Exception as e:
    print(f"❌ ERROR: {e}")
