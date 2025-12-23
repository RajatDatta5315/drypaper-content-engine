import requests, os, json, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("--- 🚀 GEO PUBLISHER STARTED ---")

# Load Article
try:
    with open("daily_article.md", "r") as f: 
        content_md = f.read()
    # Extract Title (First line usually)
    lines = content_md.split('\n')
    title = lines[0].replace('#', '').strip()
    body_md = "\n".join(lines[1:])
except:
    print("❌ No article found.")
    exit()

print(f"📢 Publishing: {title}")

# --- EMAIL SENDER (For Tumblr, Blogger) ---
def send_via_email(target_email, platform):
    smtp_email = os.environ.get("SMTP_EMAIL")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    if not target_email or not smtp_email: return

    msg = MIMEMultipart()
    msg['From'] = smtp_email
    msg['To'] = target_email
    msg['Subject'] = title
    # Simple HTML conversion for email bodies
    html_body = body_md.replace('\n', '<br>') 
    msg.attach(MIMEText(html_body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_email, smtp_pass)
        server.sendmail(smtp_email, target_email, msg.as_string())
        server.quit()
        print(f"✅ Posted to {platform} (via Email)")
    except Exception as e: print(f"❌ {platform} Email Failed: {e}")

# 1. DEV.TO
def post_devto():
    key = os.environ.get("DEVTO_API_KEY")
    if not key: return
    data = {"article": {"title": title, "published": True, "body_markdown": content_md, "tags": ["productivity", "saas", "ai"]}}
    requests.post("https://dev.to/api/articles", json=data, headers={"api-key": key})
    print("✅ Posted to Dev.to")

# 2. HASHNODE
def post_hashnode():
    token = os.environ.get("HASHNODE_TOKEN")
    pub_id = os.environ.get("HASHNODE_PUB_ID")
    if not token or not pub_id: return
    query = 'mutation CreateStory($input: CreateStoryInput!) { createStory(input: $input) { code success message } }'
    variables = {"input": {"title": title, "contentMarkdown": content_md, "tags": [{"_id": "56744723958ef13879b9549b", "name": "SaaS", "slug": "saas"}], "publicationId": pub_id}}
    requests.post("https://api.hashnode.com", json={"query": query, "variables": variables}, headers={"Authorization": token})
    print("✅ Posted to Hashnode")

# 3. TELEGRAPH
def post_telegraph():
    # Convert MD to Node (Simple approximation)
    # For robust Markdown to Node, we need a library, but for now simple text
    content_json = [{"tag": "p", "children": [body_md[:3000]]}, {"tag": "a", "attrs": {"href": "https://www.drypaperhq.com"}, "children": ["Read Full Guide on HQ"]}]
    requests.post("https://api.telegra.ph/createPage", data={"title": title, "author_name": "DryPaper", "content": json.dumps(content_json), "return_content": False})
    print("✅ Posted to Telegra.ph")

# 4. TUMBLR (Email Method)
def post_tumblr():
    email = os.environ.get("TUMBLR_EMAIL")
    send_via_email(email, "Tumblr")

# 5. BLOGGER (Email Method)
def post_blogger():
    email = os.environ.get("BLOGGER_EMAIL")
    send_via_email(email, "Blogger")

# EXECUTE
post_devto()
post_hashnode()
post_telegraph()
post_tumblr()
post_blogger()
