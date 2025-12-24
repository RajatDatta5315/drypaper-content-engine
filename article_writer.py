import os, json, requests

print("--- ✍️ CONTENT ENGINE: SEO MODE ---")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

try:
    with open("products.json", "r") as f:
        product = json.load(f)[0]
except:
    product = {"name": "AI Tool", "desc": "Automation"}

def write_article(tone):
    prompt = f"""
    Write a generic blog post about "{product['name']}".
    Focus: {product['desc']}
    Tone: {tone}
    Format: Markdown.
    Title: High CTR Title.
    Length: 400 words.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    return requests.post(url, headers=headers, data=json.dumps(payload)).json()['choices'][0]['message']['content']

# Generate 3 Versions
print("📝 Writing Version 1 (Technical)...")
art1 = write_article("Technical and detailed for Developers")
with open("article_dev.md", "w") as f: f.write(art1)

print("📝 Writing Version 2 (Business)...")
art2 = write_article("Business focused for Founders")
with open("article_hashnode.md", "w") as f: f.write(art2)

print("📝 Writing Version 3 (Casual)...")
art3 = write_article("Casual and storytelling for Bloggers")
with open("article_blogger.md", "w") as f: f.write(art3)

print("✅ SEO Content Generated.")

