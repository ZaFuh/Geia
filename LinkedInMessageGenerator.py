from openai import OpenAI
import jinja2

class LinkedInMessageGenerator:
    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)
        self.template_env = jinja2.Environment(loader=jinja2.BaseLoader())
    
    def generate_connection_request(self, lead_data):
        """Generate personalized connection request"""
        template = """
        Hi {{first_name}},
        
        I noticed your work at {{company}} around {{keywords}}. As someone interested in {{topics}}, 
        I'd love to connect and learn more about your experience with {{specific_interest}}.
        
        {% if mutual_connections %}
        We're both connected with {{mutual_connections|join(', ')}} which made me think we should connect too.
        {% endif %}
        
        Best regards,
        {{your_name}}
        """
        
        compiled = self.template_env.from_string(template)
        message = compiled.render({
            **lead_data,
            'your_name': 'Your Name'
        })
        
        return self._polish_with_ai(message, lead_data)
    
    def _polish_with_ai(self, draft, context):
        """Refine message with AI"""
        prompt = f"""
        Improve this LinkedIn message to be more personalized and engaging:
        Context: {context}
        Draft: {draft}
        
        Make it:
        1. More specific to the recipient's profile
        2. Conversational but professional
        3. Under 300 characters
        4. Include a clear call-to-action
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content