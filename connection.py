# In the name of God

# https://github.com/jadolg/rocketchat_API
import requests
from rocketchat_API.rocketchat import RocketChat
from names_urls_tokens import rocket_chat_server, user_id, tocken, channel_name


def send_news(text):
    with requests.sessions.Session() as session:
        rocket = RocketChat(
            user_id=user_id,
            auth_token=tocken,
            server_url=rocket_chat_server,
            session=session,
        )
        try:
            rocket.chat_post_message(
                text,
                room_id=channel_name,
            ).json()
        except Exception as e:
            print("\n\nRocket API error:\n" + str(e) + "\n--------------\n")
