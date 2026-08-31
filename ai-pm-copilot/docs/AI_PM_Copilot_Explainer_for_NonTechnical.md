# AI PM Copilot — Plain-English Explainer (Downloadable)

Version: 1.0

This document explains the AI PM Copilot project to someone encountering it for the first time, without assuming technical background. It describes what the product does, why it matters, how it works (step-by-step), how people should use it, important safeguards, limitations, and how to run the demo.

---

What is AI PM Copilot?

AI PM Copilot is a software tool that helps Product Managers (PMs) turn messy customer feedback into evidence-based product decisions faster. Instead of asking a PM to read hundreds of support tickets, feature requests, interview notes, and app reviews, the Copilot groups similar feedback into themes, shows the real customer quotes that back each theme, and provides a draft Product Requirements Document (PRD) that the PM can review and edit.

It is not a decision engine — it helps a PM make better decisions faster. The PM always has the final say.

Why this matters (the problem we solve)

Many product teams receive lots of feedback from customers across channels (support tickets, sales calls, interviews, community forums, and app reviews). Reading and synthesizing all of it is time-consuming and error-prone:

- It can take hours for a PM to read and summarize 100 pieces of feedback. 
- Important signals get buried under noise. 
- A single loud customer can unintentionally skew prioritization. 
- Writing a first PRD draft consumes time that PMs could use for strategic tasks.

AI PM Copilot accelerates this process and makes it defensible by ensuring every claim is backed by the exact customer feedback it came from.

Who is this for?

Primary user: Product Managers at B2B software companies (SaaS) who receive high volumes of feedback and must prioritize what to build next. 

Secondary users: Designers, customer success managers, and executives who want an evidence-backed summary to inform discussions.

High-level promise

- Reduce the time spent synthesizing feedback (prototype estimate: about 67% time saved for a 100-item dataset).
- Produce ranked, traceable themes that a PM can inspect and approve.
- Provide an AI-assisted PRD draft that is explicitly a starting point for PM editing.

Key design principles (what we enforce)

1. Evidence-first: Every AI-generated claim must trace back to customer feedback. 
2. Human-in-the-loop: A PM must approve themes before any PRD is generated. 
3. Deterministic logic is used for scoring and confidence so the system is transparent and auditable. 
4. Privacy-by-design: PII (emails, phone numbers) is redacted before any external AI call. 
5. The app must work even if there is no external AI key — it uses safe deterministic fallbacks.

Overview of the user flow (simple)

1. Upload your feedback CSV or use the demo dataset. 
2. The system validates the data and reports any missing or malformed rows. 
3. The system analyzes the feedback and groups similar items into themes. 
4. For each theme, the system shows supporting quotes, the number of customers who mentioned it, and a score showing how important it looks (the Evidence Priority Score). 
5. The PM inspects a theme, can rename/approve/reject it, and then (when approved) asks the Copilot to generate an initial PRD draft. 
6. The PM edits and approves the PRD. All actions are saved to an audit log for traceability.

Step-by-step: What happens inside the app (non-technical explanation)

1) Ingestion and validation
- You upload a CSV file with customer feedback or press “Use Demo Dataset”.
- The app checks the file for required columns (like date, customer id, text). If rows are missing critical fields, the app tells you and counts how many rows are invalid or duplicates.
- The ingestion report is shown. No data is silently tossed – you see exactly what happened.

2) Cleaning and privacy
- The app creates a cleaned version of each feedback item for analysis (fixes spacing and removes obvious noise) but keeps the original text intact so evidence quotes remain untouched for display.
- The system automatically redacts obvious personal information such as email addresses and phone numbers before anything is sent to an external AI service. The original (unredacted) text remains stored locally for internal evidence display only.

3) Grouping feedback into themes (discovery)
- The app uses modern language analysis to group similar feedback items together. Think of it like the app reading and sorting feedback into piles where each pile represents a single topic (e.g., "Advanced Reporting", "Slack integration", or "Performance").
- The groups are called “themes.” For a dataset of about 100 items the app typically finds 7–10 themes.
- The app also extracts the important words that make up each theme (keywords) and shows a few representative quotes from customers.

4) Multi-theme detection
- Sometimes a single comment talks about two things (for example: “The mobile app is slow and notifications are too noisy”). The app detects when a feedback item belongs to more than one theme and tags it with a primary and optional secondary theme. You will see this in the UI.

5) Priority scoring (how the app decides what looks important)
- The app does NOT just count how often a theme appears. It calculates a transparent score called the Evidence Priority Score using several factors:
  - Frequency: How many feedback items mention the theme.
  - Customer Value: Are customers who mentioned this theme high-value (for example, Enterprise accounts) or on paid plans?
  - Urgency: Do the feedback texts use urgent words like "blocked" or "critical"?
  - Sentiment Severity: Is the feedback around this theme mainly negative?
  - Breadth: Does the theme appear across different customer segments and sources (support, sales, interviews)?
- Each factor is converted to a 0–100 scale and combined using a set of weights so PMs can understand and change how the score is calculated.
- The result is an Evidence Priority Score (also shown as 0–100). This score is only an organizing aid — it does not tell you to build something automatically.

6) Confidence scoring (how trustworthy is the evidence)
- Separately, the app runs a Confidence Engine that looks at how much evidence there is for a theme: number of items, unique customers, source diversity, segment diversity, and how consistent the cluster is.
- The confidence result is expressed as HIGH / MEDIUM / LOW and comes with an explanation (e.g., "Supported by 24 feedback items from 19 customers across 4 sources").
- This helps PMs decide whether to do more research before committing to a roadmap change.

7) Human review
- For each theme, PMs can Approve, Rename, Reject, or Merge. Every action records who did what and when. This ensures accountability and traceability.

8) PRD generation
- Once a theme is approved, the PM can request a draft PRD. The system sends only verified, redacted evidence and summary statistics to an external AI (if an API key is present) or uses a deterministic template when no key is present.
- The AI draft includes sections like Problem Statement, Customer Evidence, Target Users, JTBD (job-to-be-done), Proposed Solution Direction, Goals, Non-Goals, Success Metrics, Risks, and Open Questions.
- The LLM is instructed not to invent numbers, revenue impact, or other facts. If the evidence is insufficient for a section, the draft explicitly says "Requires PM input." The PM must review and edit the draft before approval.

9) Audit and trust
- The app stores an append-only audit log of major events (theme generated, theme renamed, theme approved, PRD generated). The Trust Center page explains what the AI does and what deterministic logic does.

Data privacy notes

- The app redacts obvious PII (emails and phone numbers) before anything is sent to an external AI.
- Original feedback remains stored locally in the app and database for evidence traceability, but only redacted text is used for third-party AI calls.
- If your organization has stricter privacy rules, you should avoid providing API keys or omit sending text to external AI entirely.

What the system does and does not do (very important)

Does:
- Group feedback into themes using language analysis.
- Show representative quotes so every claim can be traced back.
- Compute transparent scores and confidence using deterministic rules.
- Draft PRD content from verified evidence, with clear labels where PM input is required.

Does NOT:
- Make roadmap decisions automatically.
- Invent customer evidence, numbers, or revenue impacts.
- Approve PRDs or push changes without explicit PM approval.

Evaluation & the 67% time-saved figure (what it means)

- The 67% number is a prototype estimate for a 100-item dataset: we assume manual synthesis takes about 90 minutes, while the Copilot-assisted workflow (including review and editing) takes about 30 minutes.
- This is a benchmark estimate to show potential efficiency gains, not a production-proven metric.

Common example: the demo story

1. PM loads the demo dataset (100 items). The system detects the most common themes including "Advanced Reporting".
2. The PM opens the Advanced Reporting theme and sees: 24 mentions, 19 unique customers, 7 Enterprise accounts, and 4 sources. Confidence: HIGH.
3. The PM reads five representative quotes (each quote tied to an actual feedback ID so you can inspect the original evidence).
4. The PM renames the theme to a clearer label and approves it. The rename and approval are recorded. 
5. The PM requests a PRD draft. The Copilot returns a structured draft that flags any unsupported item as "Requires PM input." The PM edits, approves, and exports the PRD.
6. The audit log shows the timeline of actions — which is useful for stakeholders and compliance.

Limitations you should know about

- Clustering quality depends on the dataset. Short, noisy, or domain-specific texts can reduce accuracy.
- The AI draft can summarize the supplied evidence but should not be treated as final — PM review is mandatory.
- PII detection uses simple rules (email and phone number patterns). The app cannot guarantee complete removal of all personal data without more sophisticated processing.
- The demo is tuned for around 100 feedback items. Larger datasets may need minor performance adjustments (saving embeddings to disk, more memory, or a vector database).

How to try the demo locally (simple steps)

1. Download the project folder or visit the repository. 
2. If you are comfortable with running local apps, the app uses Streamlit — a simple Python-based web app. Short steps:
   - Install Python 3.10+
   - Create a Python environment and install dependencies from the provided requirements.txt
   - Run: `streamlit run app.py`
3. On the app page, click "Use Demo Dataset" in the sidebar to load the 100-item demo dataset and explore.

If you do not want to run anything locally, you can still read the demo dataset file `data/customer_feedback.csv` to see what the raw feedback looks like.

Glossary (plain-language)

- Feedback item: One row from your input file (a support ticket, interview note, review, etc.).
- Theme: A group of feedback items that discuss the same underlying problem or request.
- Evidence Priority Score: A calculated number (0–100) that helps organize themes based on frequency, customer value, urgency, sentiment, and breadth.
- Confidence: A label (HIGH / MEDIUM / LOW) indicating how strong and diverse the evidence for a theme is.
- PRD: Product Requirements Document — a structured description of the problem, users, solution direction, goals, and metrics.
- LLM: Large Language Model (e.g., GPT, Claude) — the AI used for generating wording or drafts. The app only uses an LLM for optional tasks and always keeps human oversight.

Frequently Asked Questions (FAQ)

Q: Will the tool publish customer quotes publicly?
A: No. Quotes and original feedback stay in your local app instance. If you export them, you control where the exported files are stored or shared.

Q: Can the AI invent facts or numbers in the PRD?
A: The system is designed not to. The PRD generator receives only verified statistics and redacted quotes and is instructed to mark unsupported fields as "Requires PM input." Nevertheless, the PM must always review and confirm the content.

Q: What if my dataset contains sensitive information?
A: The app redacts simple PII patterns before any external AI call. For stricter privacy controls, do not provide API keys or disable external calls; the app has deterministic fallbacks that work without external AI.

Q: How accurate are the themes?
A: Reasonably accurate for mid-size datasets with clear feedback. Misclustering can happen; the UI allows a PM to rename, merge, or reject themes.

Where to go from here

- If you want to see the line-by-line results, open the "Feedback Explorer" in the app and read actual feedback entries with their assigned themes.
- Use the "Theme Intelligence" page to tune the ranking formula's weights to match your organization’s priorities.
- Approve a theme and use the PRD Copilot to get a draft you can edit and export.

Would you like this file as a downloadable PDF?

I can convert this Markdown into a PDF and add it to the project as `docs/AI_PM_Copilot_Explainer_for_NonTechnical.pdf`. Tell me if you want the PDF, and I will generate it and add it to the repository so you can download it directly.

---

If you want any changes to the tone, length, or sections (for example an executive one-page summary or a version tailored for customers vs. internal stakeholders), tell me how you'd like it adjusted and I will update the document and add a downloadable copy to the project.
