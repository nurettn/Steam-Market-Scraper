import requests #dependency
import json

class Discord(object):

    @staticmethod
    def Sender(message):
        url = "DISCORD_WEBHOOK_API_LINK" 
        data = {}
        #for all params, see
        #https://discordapp.com/developers/docs/resources/webhook#execute-webhook
        data["username"] = "Ayakkabı Botu"
        data["content"] = message
        result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            pass
            



