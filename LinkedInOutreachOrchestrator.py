import time
from datetime import datetime, timedelta
import json

class LinkedInOutreachOrchestrator:
    def __init__(self, config):
        self.connector = LinkedInConnector(config['linkedin_username'], config['linkedin_password'])
        self.qualifier = LeadQualifier(config['ideal_customer_profile'])
        self.message_gen = LinkedInMessageGenerator(config['openai_key'])
        self.sequence = OutreachSequence(DEFAULT_SEQUENCE)
        self.state_file = config.get('state_file', 'outreach_state.json')
        self.daily_limit = config.get('daily_limit', 50)
        
        # Load previous state
        self.state = self._load_state()
    
    def _load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'last_run': None,
                'today_count': 0,
                'processed_leads': []
            }
    
    def _save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
    
    def run_daily_outreach(self):
        """Main execution method to run daily"""
        # Reset daily count if new day
        if (self.state['last_run'] and 
            datetime.now().date() > datetime.fromisoformat(self.state['last_run']).date()):
            self.state['today_count'] = 0
        
        # Find and qualify leads
        companies = self.connector.search_companies("SaaS OR Tech OR Software")
        leads = []
        
        for company in companies[:10]:  # Limit for demo
            company_details = self.connector.get_company_details(company['urn_id'])
            employees = self.connector.search_employees(company['urn_id'], titles=["CTO", "CEO", "Founder"])
            
            for employee in employees[:3]:  # Limit per company
                profile = self.connector.get_profile(employee['public_id'])
                lead_score = self.qualifier.score_lead(company_details, profile)
                
                if lead_score['score'] > 0.5:  # Threshold
                    leads.append({
                        'company': company_details,
                        'profile': profile,
                        'score': lead_score['score']
                    })
        
        # Process qualified leads
        for lead in leads:
            if self.state['today_count'] >= self.daily_limit:
                break
                
            if lead['profile']['public_id'] not in self.state['processed_leads']:
                self._process_lead(lead)
                self.state['today_count'] += 1
                self.state['processed_leads'].append(lead['profile']['public_id'])
                time.sleep(random.uniform(10, 30))  # Natural pacing
        
        # Update state
        self.state['last_run'] = datetime.now().isoformat()
        self._save_state()
    
    def _process_lead(self, lead):
        """Execute full outreach sequence for a lead"""
        self.sequence.reset_for_new_lead()
        
        while action := self.sequence.get_next_action(lead):
            if action['type'] == 'connection_request':
                message = self.message_gen.generate_connection_request({
                    'first_name': lead['profile']['firstName'],
                    'company': lead['company']['name'],
                    'keywords': ', '.join(lead['company'].get('specialties', [])[:3]),
                    # Additional context fields...
                })
                
                self.connector.send_inmail(
                    recipient_urn=lead['profile']['urn_id'],
                    message=message
                )
            
            # Handle other action types...
            
            # Respect delay between steps
            time.sleep(action.get('delay_days', 0) * 86400)