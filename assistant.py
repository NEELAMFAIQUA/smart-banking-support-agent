"""Local retrieval over a small educational banking FAQ."""

import re
from collections import Counter

ARTICLES = [
    {"title": "Checking and savings", "tags": "checking savings account fees interest", "text": "Checking accounts are commonly used for frequent payments. Savings accounts are generally intended for holding money and may earn interest. Fees, rates, and rules vary; check the official account agreement."},
    {"title": "Deposit protection", "tags": "deposit insurance fdic protection limits", "text": "Deposit protection depends on country, institution, ownership category, and current limits. In the United States, the FDIC generally covers eligible deposits up to $250,000 per depositor, insured bank, and ownership category. Confirm current details with the official insurer."},
    {"title": "Interest rate and APR", "tags": "interest rate apr loan credit fees", "text": "An interest rate is the borrowing rate. APR can include the interest rate and certain fees depending on product and local rules. Compare official product disclosures and check whether a rate is fixed or variable."},
    {"title": "Suspected fraud", "tags": "fraud suspicious transaction scam account", "text": "Contact your bank promptly using a number on your card or a website or app you navigate to yourself. Never share a password, PIN, or one-time code. Follow official bank instructions to secure the account."},
    {"title": "Credit reports", "tags": "credit report score history", "text": "Credit reports summarize credit-account and payment-history information. Reporting agencies and access rights vary by country. Use official government or regulator resources to find authorized ways to request a report."},
]
_WORDS = re.compile(r"[a-z0-9]+")


def retrieve(question, limit=3):
    if limit < 1:
        raise ValueError("limit must be positive")
    terms = set(_WORDS.findall(question.lower()))
    if not terms:
        return []
    ranked = []
    for index, article in enumerate(ARTICLES):
        haystack = set(_WORDS.findall(
            f"{article['title']} {article['tags']} {article['text']}".lower()
        ))
        overlap = len(terms & haystack)
        if overlap:
            ranked.append((overlap, index, article))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [{**article, "score": score} for score, _, article in ranked[:limit]]


def answer(question):
    normalized = question.lower()
    if any(term in normalized for term in ("password", "pin", "one-time code", "otp")):
        return (
            "For your safety, never share passwords, PINs, or one-time codes here. "
            "If you disclosed one, contact your bank using its official number or app.",
            [],
        )

    specialist = route_to_specialist(normalized)
    matches = retrieve(question)
    if not matches:
        return (
            f"{specialist['greeting']} I couldn't find that topic in this demo FAQ. "
            "Contact your bank through its official channels for account-specific help.",
            [],
        )
    return "\n\n".join(
        f"**{specialist['name']} · {article['title']}**\n{article['text']}"
        for article in matches[:2]
    ), matches


_SPECIALISTS = [
    (("fraud", "suspicious", "scam", "stolen"), "Fraud safety", "Fraud support"),
    (("card", "debit", "credit", "atm"), "Card support", "Card support"),
    (("transfer", "payment", "transaction", "deposit"), "Payments support", "Payments support"),
    (("loan", "interest", "apr", "credit report"), "Borrowing support", "Borrowing support"),
    (("checking", "savings", "account"), "Account education", "Account guide"),
]


def route_to_specialist(question):
    """Choose a local specialist by intent; does not access bank systems."""
    for keywords, name, greeting in _SPECIALISTS:
        if any(keyword in question for keyword in keywords):
            return {"name": name, "greeting": greeting}
    return {"name": "General support", "greeting": "General support"}
