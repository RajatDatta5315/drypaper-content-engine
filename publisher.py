import requests, os, json, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("--- 🚀 GEO PUBLISHER: UNIQUE CONTENT MODE ---")

# --- HELPER: READ ARTICLE ---
def load_article(filename):
    try:
        with open(filename, "r") as f: 
            content = f.read()
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip()
        body = "\n".join(lines[1:])
        return title, body, content
    except:
        return None, None, None

# --- PLATFORM 1: DEV.TO (Tech Version) ---
def post_devto():
    title, body, raw = load_article("article_dev.md")
    if not title: return
    key = os.environ.get("DEVTO_API_KEY")
    if not key: return
    
    data = {"article": {"title": title, "published": True, "body_markdown": raw, "tags": ["productivity", "saas", "ai"]}}
    r = requests.post("https://dev.to/api/articles", json=data, headers={"api-key": key})
    if r.status_code in [200, 201]: print(f"✅ Dev.to Published: {title}")
    else: print(f"❌ Dev.to Failed: {r.text}")

# --- PLATFORM 2: HASHNODE (Business Version) ---
def post_hashnode():
    title, body, raw = load_article("article_hashnode.md")
    if not title: return
    token = os.environ.get("HASHNODE_TOKEN")
    pub_id = os.environ.get("HASHNODE_PUB_ID")
    
    query = 'mutation CreateStory($input: CreateStoryInput!) { createStory(input: $input) { code success message } }'
    variables = {"input": {"title": title, "contentMarkdown": raw, "tags": [{"_id": "56744723958ef13879b9549b", "name": "SaaS", "slug": "saas"}], "publicationId": pub_id}}
    
    r = requests.post("https://api.hashnode.com", json={"query": query, "variables": variables}, headers={"Authorization": token})
    print(f"✅ Hashnode Status: {r.json()}") # Debug print

# --- PLATFORM 3: TELEGRAM (Bot API) ---
def post_telegram():
    # Telegram simple short text leta hai
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id: return
    
    # Send Link to Store
    msg = "🚀 New AI Tool Dropped!\n\nCheck out the latest automation tool on DryPaper HQ.\n\n👉 https://www.drypaperhq.com"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, data={"chat_id": chat_id, "text": msg})
    if r.status_code == 200: print("✅ Telegram Message Sent")
    else: print(f"❌ Telegram Failed: {r.text}")

# --- PLATFORM 4: TELEGRAPH (Link Return) ---
def post_telegraph():
    title, body, raw = load_article("article_blogger.md") # Use casual version
    if not title: return
    
    content_json = [{"tag": "p", "children": [body[:2000]]}, {"tag": "a", "attrs": {"href": "https://www.drypaperhq.com"}, "children": ["Download Tool"]}]
    r = requests.post("https://api.telegra.ph/createPage", data={"title": title, "author_name": "DryPaper", "content": json.dumps(content_json), "return_content": False})
    if r.status_code == 200:
        path = r.json().get('result', {}).get('path')
        print(f"✅ Telegra.ph Link: https://telegra.ph/{path}")

# --- PLATFORM 5: BLOGGER (Email) ---
def post_blogger():
    title, body, raw = load_article("article_blogger.md")
    if not title: return
    
    email = os.environ.get("BLOGGER_EMAIL")
    smtp_email = os.environ.get("SMTP_EMAIL")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    
    if not email or not smtp_email: return

    msg = MIMEMultipart()
    msg['From'] = smtp_email
    msg['To'] = email
    msg['Subject'] = title
    msg.attach(MIMEText(body.replace('\n', '<br>'), 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_email, smtp_pass)
        server.sendmail(smtp_email, email, msg.as_string())
        server.quit()
        print(f"✅ Blogger Email Sent")
    except Exception as e: print(f"❌ Blogger Failed: {e}")

# EXECUTE ALL
post_devto()
post_hashnode()
post_telegram()
post_telegraph()
post_blogger()

