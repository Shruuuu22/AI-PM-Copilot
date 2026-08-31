import os
import openai
import textwrap
from utils.helpers import redact_pii

class LLMService:
    def __init__(self):
        # provider selection logic
        self.anthropic = os.getenv('ANTHROPIC_API_KEY')
        self.openai = os.getenv('OPENAI_API_KEY')
        self.gemini = os.getenv('GEMINI_API_KEY')
        if self.anthropic:
            self.provider_name = 'anthropic'
        elif self.openai:
            self.provider_name = 'openai'
        elif self.gemini:
            self.provider_name = 'gemini'
        else:
            self.provider_name = 'fallback'

    def generate_theme_label(self, keywords, examples):
        # fallback deterministic label
        if self.provider_name == 'fallback':
            return ' & '.join([k.title().replace('_',' ') for k in keywords[:3]])
        # For prototype: use simple prompt to OpenAI if key exists
        prompt = f"Create a concise theme label (3 words max) from keywords: {keywords} and examples: {examples[:3]}"
        if self.provider_name == 'openai':
            openai.api_key = self.openai
            resp = openai.Completion.create(engine='text-davinci-003', prompt=prompt, max_tokens=30)
            return resp.choices[0].text.strip()
        # Other providers could be added
        return ' & '.join(keywords[:3])

    def generate_theme_summary(self, theme_label, keywords, examples):
        if self.provider_name == 'fallback':
            return f"Customers are asking about {', '.join(keywords[:5])}. Representative quotes: {examples[:2]}"
        # else call provider (omitted for brevity)
        return f"Customers are asking about {', '.join(keywords[:5])}. Representative quotes: {examples[:2]}"

    def generate_prd(self, theme_label, theme_summary, stats, quotes):
        # redact quotes before sending out
        redacted = [redact_pii(q) for q in quotes]
        if self.provider_name == 'fallback':
            # deterministic template
            parts = []
            parts.append(f"Title: {theme_label}")
            parts.append(f"Problem Statement: {theme_summary}")
            parts.append("Customer Evidence:\n" + '\n'.join([f'- {q}' for q in quotes[:5]]))
            parts.append("Target Users: See evidence by customer_segment")
            parts.append("User Need / JTBD: Requires PM input")
            parts.append("Proposed Solution Direction: Requires PM input")
            parts.append("Goals: Requires PM input")
            parts.append("Non-Goals: Requires PM input")
            parts.append("Success Metrics: Requires PM input")
            parts.append("Risks: Review technical feasibility")
            parts.append("Open Questions: Requires PM input")
            parts.append("Evidence References: " + str(stats))
            return '\n\n'.join(parts)
        # For providers, call their APIs (not implemented in this simplified prototype)
        return '\n\n'.join(parts)
