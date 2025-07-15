import re
from groq import Groq
from dotenv import load_dotenv
import os
import praw

load_dotenv()
clientid = os.getenv("client_id")
clientsecret = os.getenv("secret_key")
useragent = os.getenv("user_agent")


#Initializing Groq LLaMA 3 client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

#Initializing Reddit client
reddit = praw.Reddit(
    client_id=clientid,
    client_secret=clientsecret,
    user_agent=useragent
)


#Scraping user posts and comments
def scrape_user(username, limit=50):
    user = reddit.redditor(username)
    combined_data = []

    try:
        for post in user.submissions.new(limit=limit):
            combined_data.append({
                "type": "Post",
                "title": post.title,
                "body": post.selftext,
                "subreddit": str(post.subreddit),
                "url": "https://reddit.com" + post.permalink
            })
        for comment in user.comments.new(limit=limit):
            combined_data.append({
                "type": "Comment",
                "body": comment.body,
                "subreddit": str(comment.subreddit),
                "url": "https://reddit.com" + comment.permalink
            })
    except Exception as e:
        print(f"Scraping error: {e}")
    
    return combined_data


#Generating prompt from LLaMA 
def build_prompt(username, data):
    samples = []
    for i, item in enumerate(data[:40]):
        if item['type'] == 'Post':
            sample = f"""[# {i+1}] Post in r/{item['subreddit']}
Title: {item['title']}
Body: {item['body'][:500]}...
Source: {item['url']}"""
        else:
            sample = f"""[# {i+1}] Comment in r/{item['subreddit']}
Comment: {item['body'][:500]}...
Source: {item['url']}"""
        samples.append(sample)

    history = "\n\n".join(samples)

    prompt = f"""
You are an expert in user behavior analysis and persona design.

Based on the Reddit history below, build a **complete user persona** for u/{username} in the following structured format. Your output should be professional, well-organized, and match the following structure exactly.

---

**Basic Info**
- **Name**: (Make up a realistic first + last name)
- **Age**: (Estimated range, like 25–34)
- **Occupation**: (Based on posts, comments, or inferred subreddits)
- **Status**: (E.g., single, married, student)
- **Location**: (If inferable, include country or city)
- **Persona Type**: (Summarize in 1–2 words, like "The Planner" or "The Explorer")

---

 **Personality & Archetype**
Use MBTI-style sliders:
- Introvert / Extrovert
- Intuition / Sensing
- Thinking / Feeling
- Judging / Perceiving

Also include descriptive traits like:
- Practical, Spontaneous, Adaptable, Detail-Oriented, etc.

---

**Motivations**
Create a horizontal bar chart style (use ██████████ or to visualize):
- Convenience: 
- Wellness: 
- Speed: 
- Preferences: 
- Comfort: 
- Dietary Needs: 

Adjust the bars based on what matters most to this user.

---

**Behaviour & Habits**
Write 5–7 bullet points describing their habits, preferences, or patterns on Reddit and in life (if inferable). Example:
- Frequently orders food online and avoids cooking
- Often posts in fitness subreddits about home workouts
- Active during late-night hours (based on timestamps)

---

**Frustrations**
List 4–6 frustrations based on complaints, tone, or repetitive mentions. Example:
- Confused by restaurant menu layouts
- Struggles to find healthy options when ordering takeaway

---

**Goals & Needs**
Summarize 3–5 needs that guide this user's decisions. Example:
- Wants healthier meals without sacrificing speed
- Prefers platforms that clearly label ingredients and dietary options

---

For every section above, include **citations** from the Reddit history, use urls.
**For every trait above, include at least 1–2 full Reddit URLs** from their history that support your reasoning. Cite like this:

Cited from: https://reddit.com/r/AskMen/comments/x7k123/example_post/

for example :-Cited from: https://reddit.com/r/teenagers/comments/xyz...
 For **every trait**, cite 1–2 **direct Reddit post URLs** from the user’s history that support your reasoning.

Make sure you copy and paste the full URL (e.g., `https://reddit.com/r/xyz/comments/post123`) after each attribute.
Avoid using [#1] or numbers. Use real URLs from the Reddit history below.
---

 Reddit History:
{history}

---

Now generate the user persona like this:

**Occupation:** Software Engineer  
Cited from: https://reddit.com/r/cscareerquestions/comments/abc123/xyz789

**Hobbies:** Gaming, hiking  
Cited from: https://reddit.com/r/gaming/comments/post1, https://reddit.com/r/hiking/comments/post2
---

Now generate the full persona using this structure.
"""
    return prompt.strip()



#Streaming persona from Groq LLaMA 4
def stream_persona(prompt):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=1024,
        top_p=1,
        stream=True
    )

    persona_text = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            persona_text += chunk.choices[0].delta.content

    return persona_text


#Saving persona to file
import os

def save_to_file(text, username, folder_path="output"):
    # Ensuring the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Defining the full file path
    file_path = os.path.join(folder_path, f"{username}_persona.txt")

    # Write to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\n User persona saved to: {file_path}")

if __name__ == "__main__":
    reddit_url = input("Enter Reddit profile URL: ").strip()
    match = re.search(r"reddit\.com/user/([^/]+)/?", reddit_url)
    if not match:
        print("Invalid URL format.")
    else:
        username = match.group(1)
        print(f"Fetching data for u/{username}...")
        data = scrape_user(username)
        print(f"Building persona...")
        prompt = build_prompt(username, data)
        persona_text = stream_persona(prompt)
        save_to_file(persona_text, username, folder_path="C:/Users/agnih/OneDrive/Desktop/beyond chats")
