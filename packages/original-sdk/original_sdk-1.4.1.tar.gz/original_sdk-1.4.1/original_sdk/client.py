import json
from typing import Any, Callable, Dict, Tuple, Union

import requests

from original_sdk.types.exceptions import ClientError

from .__pkg__ import __version__
from .base.client import BaseOriginalClient
from .types.original_response import OriginalResponse
from .utils import get_default_error_message


def get_user_agent() -> str:
    return f"original_sdk-python-client-{__version__}"


def get_default_header() -> Dict[str, str]:
    base_headers = {
        "Content-type": "application/json",
        "X-ORIGINAL-Client": get_user_agent(),
    }
    return base_headers


class OriginalClient(BaseOriginalClient):
    def __init__(
        self, api_key: str, api_secret: str, timeout: float = 6.0, **options: Any
    ):
        super().__init__(
            api_key=api_key, api_secret=api_secret, timeout=timeout, **options
        )
        self.session = requests.Session()
        self.session.mount("http://", requests.adapters.HTTPAdapter(max_retries=1))
        self.session.mount("https://", requests.adapters.HTTPAdapter(max_retries=1))

    def set_http_session(self, session: requests.Session) -> None:
        """
        You can use your own `requests.Session` instance. This instance
        will be used for underlying HTTP requests.
        """
        self.session = session

    def _get_response_details(
        self, response: requests.Response
    ) -> Tuple[Any, Dict[str, str], int]:
        try:
            json_response = response.json()
            headers = dict(response.headers)
            status = response.status_code
            return json_response, headers, status
        except ValueError:
            message = get_default_error_message(response.status_code) or response.text
            raise ClientError(
                message=message, status=response.status_code, data=message
            )

    def _parse_response(self, response: requests.Response) -> OriginalResponse:
        parsed_result, headers, status = self._get_response_details(response)
        return self.handle_parsed_response(
            parsed_result, response.reason, response.status_code, headers
        )

    def _make_request(
        self,
        method: Callable[..., requests.Response],
        relative_url: str,
        params: Dict = None,
        data: Any = None,
    ) -> OriginalResponse:
        params = params or {}
        data = data or {}
        serialized = None
        default_params = self.get_default_params()
        default_params.update(params)
        headers = get_default_header()
        headers["Authorization"] = f"Bearer {self.token}"
        headers["X-API-KEY"] = self.api_key

        url = f"{self.base_url}/{self.api_version}/{relative_url}"
        if method.__name__ in ["post", "put", "patch"]:
            serialized = json.dumps(data)

        response = method(
            url,
            data=serialized,
            headers=headers,
            params=default_params,
            timeout=self.timeout,
        )
        return self._parse_response(response)

    def put(
        self, relative_url: str, params: Dict = None, data: Any = None
    ) -> OriginalResponse:
        return self._make_request(self.session.put, relative_url, params, data)

    def post(
        self, relative_url: str, params: Dict = None, data: Any = None
    ) -> OriginalResponse:
        return self._make_request(self.session.post, relative_url, params, data)

    def get(self, relative_url: str, params: Dict = None) -> OriginalResponse:
        return self._make_request(self.session.get, relative_url, params, None)

    def delete(self, relative_url: str, params: Dict = None) -> OriginalResponse:
        return self._make_request(self.session.delete, relative_url, params, None)

    def patch(
        self, relative_url: str, params: Dict = None, data: Any = None
    ) -> OriginalResponse:
        return self._make_request(self.session.patch, relative_url, params, data)

    def create_user(
        self,
        email: Union[None, str] = None,
        user_external_id: Union[None, str] = None,
    ) -> OriginalResponse:
        return self.post(
            "user",
            data={
                "email": email,
                "user_external_id": user_external_id,
            },
        )

    def get_user(self, uid: str) -> OriginalResponse:
        return self.get(f"user/{uid}")

    def get_user_by_email(self, email: str) -> OriginalResponse:
        return self.get("user", params={"email": email})

    def get_user_by_user_external_id(self, user_external_id: str) -> OriginalResponse:
        return self.get("user", params={"user_external_id": user_external_id})

    def get_collection(self, uid: str) -> OriginalResponse:
        return self.get(f"collection/{uid}")

    def create_asset(self, **asset_data: Any) -> OriginalResponse:
        return self.post("asset", data=asset_data)

    def edit_asset(self, uid: str, **asset_data: Any) -> OriginalResponse:
        return self.put(f"asset/{uid}", data=asset_data)

    def get_asset(self, uid: str) -> OriginalResponse:
        return self.get(f"asset/{uid}")

    def get_assets_by_user_uid(self, user_uid: str) -> OriginalResponse:
        return self.get("asset", params={"user_uid": user_uid})

    def create_transfer(self, **transfer_data: Any) -> OriginalResponse:
        return self.post("transfer", data=transfer_data)

    def get_transfer(self, uid: str) -> OriginalResponse:
        return self.get(f"transfer/{uid}")

    def get_transfers_by_user_uid(self, user_uid: str) -> OriginalResponse:
        return self.get("transfer", params={"user_uid": user_uid})

    def create_burn(self, **burn_data: Any) -> OriginalResponse:
        return self.post("burn", data=burn_data)

    def get_burn(self, uid: str) -> OriginalResponse:
        return self.get(f"burn/{uid}")

    def get_burns_by_user_uid(self, user_uid: str) -> OriginalResponse:
        return self.get("burn", params={"user_uid": user_uid})

    def get_deposit(self, user_uid: str, collection_uid: str) -> OriginalResponse:
        params = {"user_uid": user_uid, "collection_uid": collection_uid}
        return self.get("deposit", params=params)

    def get_reward(self, uid: str) -> OriginalResponse:
        return self.get(f"reward/{uid}")

    def create_allocation(self, **allocation_data: Any) -> OriginalResponse:
        return self.post("reward/allocate", data=allocation_data)

    def get_allocation(self, uid: str) -> OriginalResponse:
        return self.get(f"reward/allocate/{uid}")

    def get_allocations_by_user_uid(self, user_uid: str) -> OriginalResponse:
        return self.get("reward/allocate", params={"user_uid": user_uid})

    def create_claim(self, **claim_data: Any) -> OriginalResponse:
        return self.post("reward/claim", data=claim_data)

    def get_claim(self, uid: str) -> OriginalResponse:
        return self.get(f"reward/claim/{uid}")

    def get_claims_by_user_uid(self, user_uid: str) -> OriginalResponse:
        return self.get("reward/claim", params={"user_uid": user_uid})

    def get_balance(self, reward_uid: str, user_uid: str) -> OriginalResponse:
        return self.get(
            "reward/balance", params={"reward_uid": reward_uid, "user_uid": user_uid}
        )
