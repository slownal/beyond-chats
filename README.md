# Reddit User Persona Generator

This script generates a detailed user persona for any Reddit user by analyzing their posts and comments using a state-of-the-art LLM (LLaMA 4 via Groq API). The persona includes inferred traits, motivations, habits, frustrations, and goals, with direct citations from the user’s Reddit history.

---

## Features

- Scrapes a Reddit user’s recent posts and comments (up to 50 each)
- Builds a structured persona (name, age, occupation, personality, motivations, etc.)
- Cites Reddit URLs for every trait and insight
- Uses LLaMA 4 (Groq API) for persona generation
- Saves output as a text file in a specified folder

---

## Requirements

- Python 3.8+
- [praw](https://praw.readthedocs.io/en/stable/)  
- [groq](https://pypi.org/project/groq/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Install dependencies:
```bash
pip install praw groq python-dotenv
```

---

## Setup

1. **Reddit API Credentials**  
   - Create a Reddit app at https://www.reddit.com/prefs/apps  
   - Note your `client_id`, `client_secret`, and set a `user_agent`.

2. **Groq API Key**  
   - Get your free API key from https://console.groq.com/keys

3. **Environment Variables**  
   - Create a `.env` file in the same directory as the script:
     ```
     client_id=YOUR_REDDIT_CLIENT_ID
     secret_key=YOUR_REDDIT_CLIENT_SECRET
     user_agent=YOUR_USER_AGENT
     GROQ_API_KEY=YOUR_GROQ_API_KEY
     ```

---

## Usage

1. **Run the script:**
   ```bash
   python reddit.py
   ```

2. **Enter the Reddit profile URL** when prompted, e.g.:
   ```
   https://www.reddit.com/user/kojied/
   ```

3. **Output:**  
   - The script will fetch the user’s posts and comments, generate a persona, and save it as a text file in the specified folder (default: `C:/Users/agnih/OneDrive/Desktop/beyond chats`).
   - The filename will be `<username>_persona.txt`.

---

## Output Example

```
**Basic Info**
- **Name**: Kojie Kim
- **Age**: 25–34
- **Occupation**: Software Engineer / Developer
...
Cited from: https://reddit.com/r/newyorkcity/comments/1lykkqf/i_feel_violated_by_intern_season/
...
```

---

## Customization

- **Change Output Folder:**  
  Edit the `folder_path` in the `save_to_file` function call at the end of the script.

- **Change Number of Posts/Comments Scraped:**  
  Adjust the `limit` parameter in the `scrape_user` function.

---

## Troubleshooting

- **PermissionError:**  
  Make sure the output folder exists and you have write permissions, or change the folder path to a directory you own.

- **Unicode Error in Paths:**  
  Use raw strings (`r"path\to\folder"`) or forward slashes (`"path/to/folder"`).

- **API Errors:**  
  Double-check your credentials in the `.env` file.

---

