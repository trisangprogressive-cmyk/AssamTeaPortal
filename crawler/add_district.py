import json

INPUT = "data/final_verified_businesses.json"
OUTPUT = "data/final_verified_businesses.json"

DISTRICTS = [
    "Baksa",
    "Barpeta",
    "Biswanath",
    "Bongaigaon",
    "Cachar",
    "Charaideo",
    "Chirang",
    "Darrang",
    "Dhemaji",
    "Dhubri",
    "Dibrugarh",
    "Goalpara",
    "Golaghat",
    "Hailakandi",
    "Hojai",
    "Jorhat",
    "Kamrup",
    "Kamrup Metro",
    "Karbi Anglong",
    "Karimganj",
    "Kokrajhar",
    "Lakhimpur",
    "Majuli",
    "Morigaon",
    "Nagaon",
    "Nalbari",
    "Sivasagar",
    "Sonitpur",
    "South Salmara",
    "Tamulpur",
    "Tinsukia",
    "Udalguri",
    "West Karbi Anglong"
]

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0

for trader in data:

    text = (
        trader.get("address", "") + " " +
        trader.get("website", "") + " " +
        trader.get("company_name", "")
    ).lower()

    for district in DISTRICTS:

        if district.lower() in text:

            trader["district"] = district
            count += 1
            break

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Districts Detected :", count)