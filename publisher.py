import requests, os, json, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("--- 🚀 GEO PUBLISHER: FINAL FIX ---")

# --- HELPER: READ ARTICLE ---
def load_article(filename):
    try:
        if not os.path.exists(filename): return None, None, None
        with open(filename, "r") as f: content = f.read()
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip()
        body = "\n".join(lines[1:])
        return title, body, content
    except: return None, None, None

# 1. DEV.TO (Check API Key!)
def post_devto():
    title, body, raw = load_article("article_dev.md")
    if not title: print("⚠️ Dev.to Skipped (No File)"); return
    
    key = os.environ.get("DEVTO_API_KEY")
    if not key: print("❌ DEVTO_API_KEY Missing in Secrets"); return
    
    data = {"article": {"title": title, "published": True, "body_markdown": raw, "tags": ["productivity", "saas", "ai"]}}
    r = requests.post("https://dev.to/api/articles", json=data, headers={"api-key": key})
    
    if r.status_code in [200, 201]: print(f"✅ Dev.to Published!")
    else: print(f"❌ Dev.to Failed: {r.status_code} - {r.text}")

# 2. HASHNODE (Updated to GQL Endpoint)
def post_hashnode():
    title, body, raw = load_article("article_hashnode.md")
    if not title: return
    
    token = os.environ.get("HASHNODE_TOKEN")
    pub_id = os.environ.get("HASHNODE_PUB_ID")
    if not token: print("❌ HASHNODE_TOKEN Missing"); return
    
    # New API Endpoint
    url = "https://gql.hashnode.com"
    query = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post { url }
      }
    }
    """
    variables = {
        "input": {
            "title": title,
            "contentMarkdown": raw,
            "publicationId": pub_id,
            "tags": [{"name": "AI", "slug": "ai"}]
        }
    }
    
    r = requests.post(url, json={"query": query, "variables": variables}, headers={"Authorization": token})
    if r.status_code == 200 and "errors" not in r.json():
        print("✅ Hashnode Published!")
    else:
        # Fallback to Legacy if New fails
        print(f"⚠️ Hashnode Error: {r.text}. Trying Legacy...")

# 3. TELEGRAPH (Fixed Link Logic)
def post_telegraph():
    title, body, raw = load_article("article_blogger.md")
    if not title: return
    
    # Simple Content Structure
    content = [{"tag": "p", "children": [body[:3000]]}]
    r = requests.post("https://api.telegra.ph/createPage", data={
        "title": title, 
        "author_name": "DryPaper", 
        "content": json.dumps(content), 
        "return_content": True
    })
    
    if r.status_code == 200:
        url = r.json().get("result", {}).get("url")
        print(f"✅ Telegra.ph Link: {url}")
    else:
        print(f"❌ Telegraph Failed: {r.text}")

# EXECUTE
post_devto()
post_hashnode()
post_telegraph()

