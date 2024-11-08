# inbound.py
import requests
import nlpearl  # Import the main module to access the global api_key

API_URL = "https://api.nlpearl.ai/v1"

class Inbound:
    @classmethod
    def get_all(cls):
        """Get all inbounds."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set. Set it using 'pearl.api_key = YOUR_API_KEY'.")

        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Inbound"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get(cls, inbound_id):
        """Get a specific inbound by ID."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Inbound/{inbound_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @classmethod
    def set_active(cls, inbound_id, is_active):
        """Activate or deactivate an inbound."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Inbound/{inbound_id}/Active"
        data = {"isActive": is_active}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_calls(cls, inbound_id, skip=0, limit=100, sort_prop=None, is_ascending=True,
                  from_date=None, to_date=None, tags=None):
        """Get calls for an inbound with optional filters."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Inbound/{inbound_id}/Calls"
        data = {
            "skip": skip,
            "limit": limit,
            "isAscending": is_ascending,
        }
        if sort_prop:
            data["sortProp"] = sort_prop
        if from_date:
            data["fromDate"] = from_date
        if to_date:
            data["toDate"] = to_date
        if tags:
            data["tags"] = tags

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
