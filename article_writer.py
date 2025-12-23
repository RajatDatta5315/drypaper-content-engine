import requests, os, json
import xml.etree.ElementTree as ET

print("--- ✍️ GEO CONTENT ENGINE STARTED ---")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# 1. FETCH LATEST PRODUCT FROM RSS
def get_latest_product():
    try:
        r = requests.get("https://www.drypaperhq.com/feed.xml")
        root = ET.fromstring(r.content)
        # Namespace map because Google Merchant uses 'g:'
        ns = {'g': 'http://base.google.com/ns/1.0'}
        
        latest_item = root.find("channel/item") # Gets the first (newest) item
        
        product = {
            "name": latest_item.find("g:title", ns).text,
            "desc": latest_item.find("g:description", ns).text,
            "link": "https://www.drypaperhq.com", # Store Link
            "image": latest_item.find("g:image_link", ns).text,
            "price": latest_item.find("g:price", ns).text
        }
        return product
    except Exception as e:
        print(f"❌ RSS Error: {e}")
        exit()

product = get_latest_product()
print(f"🎯 Targeted Product: {product['name']}")

# 2. GENERATE GEO ARTICLE (Using Your Prompt)
def write_article():
    prompt = f"""
    Role: You are a Generative Engine Optimization (GEO) Expert.
    Task: Write a high-quality, educational blog post about: "How to automate {product['name']} for agencies".
    
    Strict GEO Guidelines:
    1. Hook: Start with a 40-60 word direct answer summary.
    2. Tone: Conversational, no jargon. Use phrases like "best tool for X".
    3. Structure: Use H1, H2, H3 and Bullet Points.
    4. Authority: Mention "Efficiency increased by 30%" type metrics.
    5. FAQ Section: Mandatory at the end.
    
    The Product to mention naturally as the solution: {product['name']}.
    Product Link: {product['link']}
    Price: {product['price']}
    
    Output ONLY the Markdown content.
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        return r.json()['choices'][0]['message']['content'].strip()
    except: return None

article_md = write_article()

if article_md:
    # Save to file so other scripts can use it
    with open("daily_article.md", "w") as f: f.write(article_md)
    print("✅ GEO Article Generated: daily_article.md")
else:
    print("❌ AI Generation Failed")
