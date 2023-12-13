import requests
import json
from streamlit.connections import ExperimentalBaseConnection

class EdamamConnectionProvider(ExperimentalBaseConnection[requests.Session]):
    """
    A connection class to fetch nutritional data from the Edamam API.

    Attributes:
        connection_name (str): The name of the connection (optional).
    """
    def __init__(self, *args, connection_name=None, **kwargs):
        super().__init__(*args, connection_name=connection_name, **kwargs)
        self._resource = self._connect()

    def _connect(self) -> requests.Session:
        return requests.Session()

    def cursor(self):
        return self._resource
    
    def query(self, ingredients_list):
        """
       Fetches nutritional information for the specified ingredients list from the Edamam API.

        Args:
            ingredients_list (list): A list of ingredients for which nutritional information is to be fetched.
            

        Returns:
            list: A list containing nutritional information for each ingredient.
        """
        def get_nutritional_data(ingredients):
            nutritional_info_list = []
          
            url = 'https://api.edamam.com/api/nutrition-details'
            headers = {
                'Content-Type': 'application/json',
            }
            params = {
                'app_id': 'abcde',  # Write your APP ID here
                'app_key': 'abcdefgh',  # Write your APP KEY here
            }

            for ingredient in ingredients:
                payload = {
                    'ingr': [ingredient],
                }
                response = self._resource.post(url, headers=headers, params=params, data=json.dumps(payload))

                if response.status_code == 200:
                    data = response.json()
                    nutritional_info = {
                        "ingredient": ingredient,
                        "calories": data['calories'],
                        "totalWeight": data['totalWeight'],
                        "dietLabels": data['dietLabels'],
                        "healthLabels": data['healthLabels'],
                        "totalNutrients": data['totalNutrients'],
                    }
                    nutritional_info_list.append(nutritional_info)
                else:
                    raise Exception(f"Failed to fetch nutritional information for {ingredient}.")

            return nutritional_info_list

        return get_nutritional_data(ingredients_list)
