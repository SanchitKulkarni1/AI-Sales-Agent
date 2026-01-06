def engagement_score(row):
    visits = row.get("TotalVisits", 0) or 0
    time_spent = row.get("Total Time Spent on Website", 0) or 0
    pages = row.get("Page Views Per Visit", 0) or 0

    score = (
        min(visits / 10, 1.0) * 0.4 +
        min(time_spent / 300, 1.0) * 0.4 +
        min(pages / 5, 1.0) * 0.2
    )
    return round(score, 3)

HIGH_INTENT = {
    "Email Opened",
    "SMS Sent",
    "Olark Chat Conversation",
    "Email Clicked"
}

def intent_score(row):
    last_activity = row.get("Last Activity")
    if last_activity in HIGH_INTENT:
        return 1.0
    return 0.5

def authority_score(row):
    occupation = row.get("What is your current occupation")

    if occupation in {"Working Professional", "Business Owner"}:
        return 1.0
    elif occupation == "Student":
        return 0.4
    return 0.6

def penalty_score(row):
    penalty = 0.0
    if row.get("Do Not Call") == "Yes":
        penalty -= 0.3
    if row.get("Do Not Email") == "Yes":
        penalty -= 0.2
    return penalty

def compute_rule_score(row):
    engagement = engagement_score(row)
    intent = intent_score(row)
    authority = authority_score(row)
    penalty = penalty_score(row)

    score = (
        0.35 * engagement +
        0.30 * intent +
        0.25 * authority +
        penalty
    )

    return max(0.0, min(round(score, 3), 1.0))

