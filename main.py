from typing import Any, Dict, Optional
from requests import Response, request

API_URL = "https://restful-booker.herokuapp.com"
API_KEY = "Basic YWRtaW46cGFzc3dvcmQxMjM="


class TestAPI:
    @classmethod
    def _api_request(
            cls,
            url: str,
            headers: Dict[str, Any],
            method: str,
            timeout: int = 100,
            json: Optional[Dict[str, Any]] = None,
    ) -> Response:
        url = f"{API_URL}/{url}"
        return request(
            method=method,
            url=url,
            timeout=timeout,
            headers=headers,
            json=json,
        )

    @classmethod
    def _add_headers(cls, auth_method: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if auth_method == "api_key":
            headers.update({"Authorization": {API_KEY}})
        elif auth_method == "cookie_token":
            headers.update({"Cookie": "token=abc123"})
        return headers

    @classmethod
    def _get_auth_token(cls) -> str:
        url = "auth"
        response = cls._api_request(
            url=url,
            headers=cls._add_headers(),
            method="POST",
            json={"username": "admin", "password": "password123"},
        )
        return response.json()["token"]

    @classmethod
    def create_booking(cls, request_payload: Dict[str, Any]) -> Response:
        url = "booking"
        response = cls._api_request(
            url=url, headers=cls._add_headers(), method="POST", json=request_payload
        )
        return response

    @classmethod
    def list_booking_ids(cls, search_by_firstname: Optional[str]) -> Response:
        url = "/booking"
        # I only added functionality for searching with first name
        if search_by_firstname:
            url = url + "?firstname=" + search_by_firstname
        response = cls._api_request(url=url, headers=cls._add_headers(), method="GET")
        return response

    @classmethod
    def get_booking_by_id(cls, search_by_id: Optional[int]) -> Response:
        url = "/booking/"
        if search_by_id:
            url += str(search_by_id)
        response = cls._api_request(url=url, headers=cls._add_headers(), method="GET")
        return response

    @classmethod
    def update_booking(cls, id_to_update: [int], update_payload: Dict[str, Any], partial_or_full_update: [str]):
        url = "/booking/"
        method = ""
        if id_to_update:
            url += str(id_to_update)

        if partial_or_full_update.lower() == "partial":
            method = "PATCH"
        elif partial_or_full_update.lower() == "full":
            method = "PUT"
        response = cls._api_request(url=url, headers=cls._add_headers("api_key"), json=update_payload, method=method)
        return response

    @classmethod
    def delete_booking(cls, booking_to_delete: [int]):
        url = "/booking" + str(booking_to_delete)
        response = cls._api_request(url=url, headers=cls._add_headers("api_key"), method="DELETE")
        return response

    @classmethod
    def ping_api(cls):
        url = "ping"
        response = cls._api_request(url=url, headers=cls._add_headers(), method="GET")
        return response

