import html
import re

def clean_text(text):
    if not text:
        return None
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

CITY_ALIASES = {
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "bombay": "Mumbai",
    "navi mumbai": "Mumbai",
    "gurgaon": "Gurugram",
    "gurugram": "Gurugram",
    "new delhi": "Delhi",
    "delhi ncr": "Delhi",
    "noida": "Noida",
    "madras": "Chennai",
    "calcutta": "Kolkata",
    "poona": "Pune",
}

def standardize_location(loc):
    if not loc:
        return "Unspecified"
    first = loc.split(",")[0].strip().lower()
    if first in ("india", ""):
        return "Unspecified"
    if "remote" in first:
        return "Remote"
    return CITY_ALIASES.get(first, first.title())

CITIES = ["Bengaluru", "Bangalore", "Mumbai", "Pune", "Hyderabad", "Chennai",
          "Delhi", "Gurugram", "Gurgaon", "Noida", "Kolkata", "Ahmedabad",
          "Jaipur", "Kochi", "Indore", "Chandigarh", "Coimbatore"]

def find_city_in_text(text):
    if not text:
        return None
    t = text.lower()
    for city in CITIES:
        if re.search(r"(?<![a-z])" + re.escape(city.lower()) + r"(?![a-z])", t):
            return standardize_location(city)
    return None

if __name__ == "__main__":
    for s in ["Bangalore, Karnataka", "Mumbai, MH", "India", "Hyderabad, Telangana", "Gurgaon", None]:
        print(s, "->", standardize_location(s))