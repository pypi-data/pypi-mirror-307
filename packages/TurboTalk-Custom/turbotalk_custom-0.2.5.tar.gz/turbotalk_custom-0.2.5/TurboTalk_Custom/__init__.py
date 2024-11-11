from opyngpt import prompt

class TurboTalk:
    def __init__(self, company_name, bot_name, behaviour):
        self.company_name = company_name
        self.bot_name = bot_name
        self.behaviour = behaviour
        self.user_input = None
        self.response = None

    def set_user_input(self, user_input):
        """Set the user input message."""
        self.user_input = user_input

    def give_response(self):
        """Generate the response based on user input and the provided parameters."""
        if self.user_input is None:
            raise ValueError("User input is required to generate a response.")
        
        content = (
            f"Follow the below given commands strictly. {self.user_input} "
            f"and behave very very strongly just like {self.behaviour} as I am a/an {self.behaviour} type person. "
            f"If asked any questions regarding identity, introduce yourself as {self.bot_name} by {self.company_name}, "
            f"and mention it's a learning/developing stage. "
            f"Your purpose is to assist me in almost every possible way."
        )
        
        # Call opyngpt to generate the response
        self.response = prompt(content)

    def get_response(self):
        """Return the generated response."""
        if self.response is None:
            raise ValueError("Response has not been generated yet.")
        return self.response

# Singleton instance to be accessed by the user
turbo_talk_instance = TurboTalk
