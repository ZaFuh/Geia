from linkedin_api import Linkedin  # Unofficial API wrapper
import time
import random

class LinkedInConnector:
    def __init__(self, username, password):
        self.api = Linkedin(username, password)
        self.rate_limit_delay = (2, 5)  # seconds between actions
    
    def search_companies(self, keywords, limit=50):
        """Search for companies by keywords"""
        results = self.api.search_companies(keywords=keywords, limit=limit)
        time.sleep(random.uniform(*self.rate_limit_delay))
        return results
    
    def get_company_details(self, public_id):
        """Get detailed company information"""
        details = self.api.get_company(public_id)
        time.sleep(random.uniform(*self.rate_limit_delay))
        return details
    
    def search_employees(self, company_urn, titles=None, limit=20):
        """Find employees at a company"""
        results = self.api.search_people(
            current_company=[company_urn],
            titles=titles,
            limit=limit
        )
        time.sleep(random.uniform(*self.rate_limit_delay))
        return results
    
    def get_profile(self, public_id):
        """Get full profile details"""
        profile = self.api.get_profile(public_id)
        time.sleep(random.uniform(*self.rate_limit_delay))
        return profile
    
    def send_inmail(self, recipient_urn, message):
        """Send LinkedIn message (requires proper permissions)"""
        # Note: This typically requires a Sales Navigator account
        result = self.api.send_inmail(
            recipient_urn=recipient_urn,
            message=message
        )
        time.sleep(random.uniform(*self.rate_limit_delay))
        return result