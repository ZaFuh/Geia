import datetime
from typing import List, Dict

class OutreachSequence:
    def __init__(self, steps: List[Dict]):
        self.sequence = steps
        self.current_step = 0
    
    def get_next_action(self, lead):
        """Get the next message in sequence for a lead"""
        if self.current_step >= len(self.sequence):
            return None
        
        step = self.sequence[self.current_step]
        self.current_step += 1
        
        return {
            'type': step['type'],
            'content': step['template'],
            'delay_days': step.get('delay_days', 0)
        }
    
    def reset_for_new_lead(self):
        self.current_step = 0

# Example sequence
DEFAULT_SEQUENCE = [
    {
        'type': 'connection_request',
        'template': 'generated',  # Will use message generator
        'delay_days': 0
    },
    {
        'type': 'follow_up',
        'template': 'Thanks for connecting! I noticed you work with X. Have you considered Y?',
        'delay_days': 3
    },
    {
        'type': 'value_message',
        'template': 'Here\'s an article I thought you might find interesting about Z...',
        'delay_days': 7
    }
]