import abc
import os
from typing import Any, Awaitable, Dict, Union

import jwt

from original_sdk.types.environment import Environment, get_environment
from original_sdk.types.exceptions import is_error_status_code, parse_and_raise_error
from original_sdk.types.original_response import OriginalResponse

DEVELOPMENT_BASE_URL = "https://api-dev.getoriginal.com"
PRODUCTION_BASE_URL = "https://api.getoriginal.com"
DEFAULT_API_VERSION = "v1"


class BaseOriginalClient(abc.ABC):
    def __init__(
        self, api_key: str, api_secret: str, timeout: float = 6.0, **options: Any
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout

        if os.getenv("ORIGINAL_TIMEOUT"):
            self.timeout = float(os.environ["ORIGINAL_TIMEOUT"])

        self.options = options
        self.base_url = PRODUCTION_BASE_URL
        self.env = None
        self.api_version = DEFAULT_API_VERSION

        if options.get("base_url"):
            self.base_url = options["base_url"]
        elif os.getenv("ORIGINAL_URL"):
            self.base_url = os.environ["ORIGINAL_URL"]

        if options.get("env"):
            self.env = get_environment(options["env"])
        elif os.getenv("ORIGINAL_ENV"):
            self.env = get_environment(os.environ["ORIGINAL_ENV"])

        if self.env == Environment.Development:
            self.base_url = DEVELOPMENT_BASE_URL
        elif self.env == Environment.Production:
            self.base_url = PRODUCTION_BASE_URL

        if options.get("api_version"):
            self.api_version = options["api_version"]
        elif os.getenv("API_VERSION"):
            self.api_version = os.environ["API_VERSION"]

        self.base_url = self.base_url.rstrip("/")

        self.token = jwt.encode(
            {"resource": "*", "action": "*", "user_id": "*", "api_key": api_key},
            api_secret,
        )

    def get_default_params(self) -> Dict[str, str]:
        return {"api_key": self.api_key, "api_secret": self.api_secret}

    def create_token(self) -> str:
        return jwt.encode(
            {"resource": "*", "action": "*", "user_id": "*", "api_key": self.api_key},
            self.api_secret,
        )

    def create_search_params(
        self,
        filter_conditions: Dict,
        query: Union[str, Dict],
        **options: Any,
    ) -> Dict[str, Any]:
        params = options.copy()
        if isinstance(query, str):
            params.update({"query": query})
        else:
            params.update({"message_filter_conditions": query})

        params.update({"filter_conditions": filter_conditions})

        return params

    def handle_parsed_response(
        self, parsed_result: dict, reason: str, status: int, headers: dict
    ) -> OriginalResponse:
        if is_error_status_code(status):
            parse_and_raise_error(parsed_result, reason, status)
        return OriginalResponse(parsed_result, headers, status)

    @abc.abstractmethod
    def create_user(
        self,
        email: Union[None, str] = None,
        user_external_id: Union[None, str] = None,
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Create an Original user.
        """
        pass

    @abc.abstractmethod
    def get_user(
        self, uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get an Original user.

        :param uid: the user uid
        :return:
        """
        pass

    @abc.abstractmethod
    def get_user_by_email(
        self, email: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Gets a user by email

        :param email: the user's email
        :return:
        """
        pass

    @abc.abstractmethod
    def get_user_by_user_external_id(
        self, user_external_id: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Gets a user by user_external_id

        :param user_external_id: the user's user_external_id
        :return:
        """
        pass

    @abc.abstractmethod
    def get_collection(
        self, uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get an Original collection.

        :param uid: the collection uid
        :return:
        """
        pass

    @abc.abstractmethod
    def create_asset(
        self, **asset_data: Any
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Create an Original asset.

        :param asset_data: the asset data
        :return:
        """
        pass

    @abc.abstractmethod
    def edit_asset(
        self, uid: str, **asset_data: Any
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Update an Original asset.

        :param uid: the asset uid
        :param asset_data: the asset data
        :return:
        """
        pass

    @abc.abstractmethod
    def get_asset(
        self, uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get an Original asset.

        :param uid: the asset uid
        :return:
        """
        pass

    @abc.abstractmethod
    def get_assets_by_user_uid(
        self, user_uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get a list of Original assets by user uid.

        :param user_uid: the user uid
        :return:
        """
        pass

    @abc.abstractmethod
    def create_transfer(
        self, **transfer_data: Any
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Create an Original transfer.

        :param transfer_data: the transfer data
        :return:
        """
        pass

    @abc.abstractmethod
    def get_transfer(
        self, uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get an Original transfer.

        :param uid: the transfer uid
        :return:
        """
        pass

    @abc.abstractmethod
    def get_transfers_by_user_uid(
        self, user_uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get a list of Original transfers by user uid.

        :param user_uid: the user uid
        :return:
        """
        pass

    @abc.abstractmethod
    def create_burn(
        self, **burn_data: Any
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Create an Original burn.

        :param burn_data: the burn data
        :return:
        """
        pass

    @abc.abstractmethod
    def get_burn(
        self, uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get an Original burn.

        :param uid: the burn uid
        :return:
        """
        pass

    @abc.abstractmethod
    def get_burns_by_user_uid(
        self, user_uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get a list of Original burns by user uid.

        :param user_uid: the user uid
        :return:
        """
        pass

    @abc.abstractmethod
    def get_deposit(
        self, user_uid: str, collection_uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get an Original deposit by user uid and collection uid.

        :param user_uid: the user uid
        :param collection_uid: the collection uid
        :return:
        """
        pass

    @abc.abstractmethod
    def get_reward(
        self, uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get an Original reward.

        :param uid: the reward uid
        :return:
        """
        pass

    @abc.abstractmethod
    def create_allocation(
        self, **allocation_data: Any
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Create an Original allocation.

        :param allocation_data: the allocation data
        :return:
        """
        pass

    @abc.abstractmethod
    def get_allocation(
        self, uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get an Original allocation.

        :param uid: the allocation uid
        :return:
        """
        pass

    @abc.abstractmethod
    def get_allocations_by_user_uid(
        self, user_uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get a list of Original allocations by user uid.

        :param user_uid: the user uid
        :return:
        """
        pass

    @abc.abstractmethod
    def create_claim(
        self, **claim_data: Any
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Create an Original claim.

        :param claim_data: the claim data
        :return:
        """
        pass

    @abc.abstractmethod
    def get_claim(
        self, uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get an Original claim.

        :param uid: the claim uid
        :return:
        """
        pass

    @abc.abstractmethod
    def get_claims_by_user_uid(
        self, user_uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get a list of Original claims by user uid.

        :param user_uid: the user uid
        :return:
        """
        pass

    @abc.abstractmethod
    def get_balance(
        self, reward_uid: str, user_uid: str
    ) -> Union[OriginalResponse, Awaitable[OriginalResponse]]:
        """
        Get a user's reward balance.

        :param reward_uid: the reward uid
        :param user_uid: the user uid
        :return:
        """
        pass
