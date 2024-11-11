import torch
import requests
import base64

class Client:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://viturka.com/upload_model'

    def send_model(self, model, model_type):
        torch.save(model.state_dict(), 'temp_model.pth')
        with open("temp_model.pth", "rb") as f:
            files = {'model': f}
            response = requests.post(self.api_url, files=files, data={'api_key': self.api_key, 'model_type': model_type})

        if response.status_code == 200:
            # Deserialize the received global model
            data = response.json()
            if data['model'] == 200:
                model = model
            else:
                # Decode the base64 encoded string back to bytes
                torch_model = base64.b64decode(data['model'])

                model.load_state_dict(torch.load(torch_model))

        return model
