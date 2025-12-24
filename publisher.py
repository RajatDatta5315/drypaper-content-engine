import requests, os, json, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("--- 🚀 GEO PUBLISHER: FINAL FIX ---")

def load_article(filename):
    try:
        if not os.path.exists(filename): return None, None, None
        with open(filename, "r") as f: content = f.read()
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip()
        body = "\n".join(lines[1:])
        return title, body, content
    except: return None, None, None

# 1. DEV.TO (Using NEW Secret Name)
def post_devto():
    title, body, raw = load_article("article_dev.md")
    if not title: print("⚠️ Dev.to Skipped (No File)"); return
    
    # 🔥 UPDATED SECRET NAME
    key = os.environ.get("DEVTO_KEY_NEW") 
    if not key: print("❌ DEVTO_KEY_NEW Missing in Secrets"); return
    
    data = {"article": {"title": title, "published": True, "body_markdown": raw, "tags": ["productivity", "saas", "ai"]}}
    r = requests.post("https://dev.to/api/articles", json=data, headers={"api-key": key})
    
    if r.status_code in [200, 201]: print(f"✅ Dev.to Published!")
    else: print(f"❌ Dev.to Failed: {r.status_code} - {r.text}")

# 2. HASHNODE
def post_hashnode():
    title, body, raw = load_article("article_hashnode.md")
    if not title: return
    token = os.environ.get("HASHNODE_TOKEN")
    pub_id = os.environ.get("HASHNODE_PUB_ID")
    if not token: print("❌ HASHNODE_TOKEN Missing"); return
    
    url = "https://gql.hashnode.com"
    query = """mutation PublishPost($input: PublishPostInput!) { publishPost(input: $input) { post { url } } }"""
    variables = {"input": {"title": title, "contentMarkdown": raw, "publicationId": pub_id, "tags": [{"name": "AI", "slug": "ai"}]}}
    r = requests.post(url, json={"query": query, "variables": variables}, headers={"Authorization": token})
    if r.status_code == 200 and "errors" not in r.json(): print("✅ Hashnode Published!")
    else: print(f"⚠️ Hashnode Error: {r.text}")

# 3. TELEGRAPH
def post_telegraph():
    title, body, raw = load_article("article_blogger.md")
    if not title: return
    content = [{"tag": "p", "children": [body[:3000]]}]
    r = requests.post("https://api.telegra.ph/createPage", data={"title": title, "author_name": "DryPaper", "content": json.dumps(content), "return_content": True})
    if r.status_code == 200: print(f"✅ Telegra.ph Link: {r.json().get('result', {}).get('url')}")
    else: print(f"❌ Telegraph Failed: {r.text}")

# 4. TELEGRAM CHANNEL (Auto-Post)
def post_telegram():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    # 🔥 Using your Channel ID from logs
    chat_id = "-1003646770200" 
    
    if not token: return
    msg = "🚀 New AI Tool Dropped on DryPaper HQ!\n\nCheck it out: https://www.drypaperhq.com"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, data={"chat_id": chat_id, "text": msg})
    if r.status_code == 200: print("✅ Telegram Channel Posted")
    else: print(f"❌ Telegram Failed: {r.text}")

# EXECUTE
post_devto()
post_hashnode()
post_telegraph()
post_telegram()

