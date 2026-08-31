from services.llm_service import LLMService

class PRDService:
    def __init__(self, llm: LLMService):
        self.llm = llm

    def generate_prd(self, theme_row, df_feedback):
        theme_label = theme_row['label']
        theme_summary = theme_row['summary']
        idxs = theme_row['representative_examples']
        # collect representative quotes from df_feedback by matching texts
        quotes = theme_row['representative_examples']
        stats = {
            'mentions': int(theme_row['mentions']),
            'unique_customers': int(theme_row['unique_customers']),
            'enterprise_customers': int(theme_row['enterprise_customers']),
            'priority_score': float(theme_row['priority_score'])
        }
        prd = self.llm.generate_prd(theme_label, theme_summary, stats, quotes)
        return prd
