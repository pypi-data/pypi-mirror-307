# __init__.py

from opyngpt import prompt

class TurboTalk:
    def __init__(self):
        self.response_content = ""

    def give_response(self, company_name, bot_name, behaviour, user_message):
        messages = [{
            "content": (
                f"Follow the below given commands strictly. {user_message} "
                f"and behave very very strongly just like {behaviour} as I am a/an {behaviour} type person. "
                f"If asked any questions regarding identity, introduce yourself as {bot_name} by {company_name}, "
                f"and mention it's a learning/developing stage. "
                f"Your purpose is to assist me in almost every possible way."
            )
        }]

        try:
            user_input = messages
            self.response_content = prompt(user_input)

        except Exception as e:
            self.response_content = f"An error occurred: {e}"

    def get_response(self):
        return self.response_content


# Create an instance of TurboTalk and make it easily accessible
turbo_talk_instance = TurboTalk()
