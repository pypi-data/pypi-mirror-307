# outbound.py
import requests
import nlpearl  # Import the main module to access the global api_key

API_URL = "https://api.nlpearl.ai/v1"


class Outbound:
    @classmethod
    def get_all(cls):
        """Get all outbounds."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Outbound"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get(cls, outbound_id):
        """Get a specific outbound by ID."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Outbound/{outbound_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @classmethod
    def set_active(cls, outbound_id, is_active):
        """Activate or deactivate an outbound."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/Active"
        data = {"isActive": is_active}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_calls(cls, outbound_id, skip=0, limit=100, sort_prop=None, is_ascending=True,
                  from_date=None, to_date=None, tags=None):
        """Get calls for an outbound with optional filters."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/Calls"
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

    @classmethod
    def add_lead(cls, outbound_id, phone_number=None, external_id=None, call_data=None):
        """Add a lead to an outbound."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/Lead"
        data = {}

        if phone_number:
            data["phoneNumber"] = phone_number
        if external_id:
            data["externalId"] = external_id
        if external_id:
            data["CallData"] = call_data

        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_leads(cls, outbound_id, skip=0, limit=100, sort_prop=None,
                  is_ascending=True, status=None):
        """Get leads for an outbound with optional filters."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/Leads"
        data = {
            "skip": skip,
            "limit": limit,
            "isAscending": is_ascending,
        }
        if sort_prop:
            data["sortProp"] = sort_prop
        if status:
            data["status"] = status

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_lead_by_id(cls, outbound_id, lead_id):
        """Get a specific lead by lead ID."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Outbound/{outbound_id}/Lead/{lead_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_lead_by_external_id(cls, outbound_id, external_id):
        """Get a lead by external ID."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Outbound/{outbound_id}/Lead/External/{external_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @classmethod
    def make_call(cls, outbound_id, to, call_data=None):
        """Make a call in an outbound campaign."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/Call"
        data = {"to": to}
        if call_data:
            data["callData"] = call_data

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_call_request(cls, request_id):
        """Get details of a specific call request."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {"Authorization": f"Bearer {nlpearl.api_key}"}
        url = f"{API_URL}/Outbound/CallRequest/{request_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_call_requests(cls, outbound_id, skip=0, limit=100, sort_prop=None,
                          is_ascending=True, from_date=None, to_date=None):
        """Get call requests for an outbound with optional filters."""
        if nlpearl.api_key is None:
            raise ValueError("API key is not set.")

        headers = {
            "Authorization": f"Bearer {nlpearl.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{API_URL}/Outbound/{outbound_id}/CallRequest"
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

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
