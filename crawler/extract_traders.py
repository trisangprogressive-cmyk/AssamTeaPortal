import json
import re

PHONE_REGEX = r'(?:\+91[\-\s]?)?[6-9]\d{9}'
EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+\.\w+'

DISTRICTS = [
     "Jorhat",
    "Dibrugarh",
    "Tinsukia",
    "Golaghat",
    "Sivasagar"
]

with open("data/verified_traders.json","r",encoding="utf-8") as f:
    data=json.load(f)

traders=[]

for item in data:

    text=item.get("address","")

    phones=list(set(re.findall(PHONE_REGEX,text)))
    emails=list(set(re.findall(EMAIL_REGEX,text)))

    district="Unknown"

    for d in DISTRICTS:
        if d.lower() in text.lower():
            district=d
            break

    traders.append({

        "company_name":item.get("name",""),

        "district":district,

        "phone":", ".join(phones),

        "email":", ".join(emails),

        "address":text[:500],

        "website":item.get("url","")

    })

with open("data/final_traders.json","w",encoding="utf-8") as f:
    json.dump(traders,f,indent=4,ensure_ascii=False)

print("Final Traders :",len(traders))