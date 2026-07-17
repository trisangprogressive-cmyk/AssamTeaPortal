import os
import json
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("data/raw_results.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

OUTPUT = "data/structured_traders.json"

results = []

BATCH_SIZE = 10

for start in range(0, len(pages), BATCH_SIZE):

    batch = pages[start:start+BATCH_SIZE]

    text = ""

    for i, page in enumerate(batch):
        text += f"""

PAGE {i+1}

TITLE:
{page.get('title','')}

URL:
{page.get('url','')}

CONTENT:
{page.get('content','')[:3000]}

"""

    prompt = f"""
You are extracting Assam Tea Trader information.

Extract ONLY real tea businesses.

Return ONLY a JSON array.

Example:

[
 {{
   "company_name":"",
   "district":"",
   "phone":"",
   "email":"",
   "address":"",
   "website":""
 }}
]

If none exist return []

{text}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        ans = response.text.replace("```json","").replace("```","").strip()

        data = json.loads(ans)

        results.extend(data)

        print(f"Batch {start//BATCH_SIZE+1} Done")

        with open(OUTPUT,"w",encoding="utf-8") as f:
            json.dump(results,f,indent=4,ensure_ascii=False)

        time.sleep(35)   # stay within free-tier rate limits

    except Exception as e:
        print(e)

print("Completed")
print("Total Traders:",len(results))