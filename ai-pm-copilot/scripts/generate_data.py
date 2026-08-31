from faker import Faker
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker()
F = Faker()
F.seed_instance(SEED)

THEMES = {
    'Performance': [
        "The app is slow to load my dashboard, pages hang for 10+ seconds.",
        "Loading times are terrible when I open project boards.",
        "Performance has degraded since the latest release.",
    ],
    'Slack Integration': [
        "We need Slack notifications for task updates.",
        "Slack integration is missing most fields we need.",
        "Please support Slack threads and comments sync.",
    ],
    'Advanced Reporting': [
        "We need custom dashboards and exports to CSV/Excel.",
        "Advanced filtering and pivoting in reports would help leadership.",
        "Reporting lacks group-by and date range filters.",
    ],
    'Mobile': [
        "Mobile app frequently crashes on iOS.",
        "Missing key features on mobile, like subtasks.",
    ],
    'Notifications': [
        "We're getting too many notifications; too noisy.",
        "Notification controls are not granular enough.",
    ],
    'Permissions': [
        "Permissions are confusing; can't set per-project access.",
        "We need role-based access control and SSO for security.",
    ],
    'Search': [
        "Search results are inaccurate; can't find old tasks.",
        "Search should support filters and saved searches.",
    ],
    'Automation': [
        "Automation rules are limited; need condition-based triggers.",
        "We want automatic status updates when PRs merge.",
    ],
    'Export': [
        "Export to CSV doesn't include custom fields.",
        "Need better export templates for our reports.",
    ]
}

SOURCES = ['Support', 'Sales Call', 'Customer Interview', 'Community', 'App Review']
SEGMENTS = ['SMB', 'Mid-Market', 'Enterprise']
PLANS = ['Free', 'Pro', 'Business', 'Enterprise']
REGIONS = ['North America', 'Europe', 'Asia-Pacific']

rows = []

# Generate 100 rows
for i in range(1, 101):
    theme = random.choices(list(THEMES.keys()), weights=[15,12,14,8,10,7,9,10,5], k=1)[0]
    text = random.choice(THEMES[theme])
    # sometimes add ambiguity or multiple themes
    if random.random() < 0.12:
        other = random.choice(list(THEMES.keys()))
        if other != theme:
            text = text + " " + random.choice(THEMES[other])
    # add near duplicates
    if random.random() < 0.08:
        text = text
    # noise
    if random.random() < 0.05:
        text = text + " Also, the UI color needs work."

    date = (datetime.now() - timedelta(days=random.randint(0, 90))).date()
    customer_id = f"C{random.randint(10,200):03d}"
    customer_segment = random.choices(SEGMENTS, weights=[50,30,20], k=1)[0]
    source = random.choice(SOURCES)
    sentiment = random.choice([-1, -0.5, 0, 0.5, 1])
    account_value = random.choice([500, 2000, 15000, 75000, 250000])
    plan = random.choices(PLANS, weights=[30,40,20,10], k=1)[0]
    region = random.choice(REGIONS)
    rows.append({
        'feedback_id': f'F{i:04d}',
        'date': date.isoformat(),
        'customer_id': customer_id,
        'customer_segment': customer_segment,
        'source': source,
        'feedback_text': text,
        'sentiment': sentiment,
        'account_value': account_value,
        'plan': plan,
        'region': region
    })

df = pd.DataFrame(rows)
df.to_csv('ai-pm-copilot/data/customer_feedback.csv', index=False)
print('Generated', len(df), 'rows')
