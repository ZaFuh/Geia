from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class LeadQualifier:
    def __init__(self, ideal_customer_profile):
        self.ideal_profile = ideal_customer_profile
        self.vectorizer = TfidfVectorizer()
    
    def score_lead(self, company_data, profile_data):
        """Score lead based on similarity to ideal customer profile"""
        # Convert data to comparable text
        company_text = f"{company_data['name']} {company_data['description']} {' '.join(company_data.get('specialties', []))}"
        profile_text = f"{profile_data['headline']} {' '.join(profile_data.get('experience', []))}"
        
        # Vectorize and compare
        vectors = self.vectorizer.fit_transform([self.ideal_profile, company_text + " " + profile_text])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        
        return {
            'score': similarity,
            'company': company_data,
            'profile': profile_data
        }