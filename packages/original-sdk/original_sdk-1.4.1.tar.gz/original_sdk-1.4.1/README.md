# Official Python SDK for [Original](https://getoriginal.com) API

## Table of Contents

- [Getting Started](#-getting-started)
- [Documentation](#-documentation)
  - [Initialization](#initialization)
  - [User](#user)
    - [Create a new user](#create-a-new-user)
    - [Get a user by UID](#get-a-user-by-uid)
    - [Get a user by email](#get-a-user-by-email)
    - [Get a user by user external ID](#get-a-user-by-client-id)
  - [Asset](#asset)
    - [Create a new asset](#create-a-new-asset)
    - [Get an asset by UID](#get-an-asset-by-asset-uid)
    - [Get assets by user UID](#get-assets-by-user-uid)
    - [Edit an asset](#edit-an-asset)
  - [Transfer](#transfer)
    - [Create a new transfer](#create-a-new-transfer)
    - [Get a transfer](#get-a-transfer-by-transfer-uid)
    - [Get transfers by user UID](#get-transfers-by-user-uid)
  - [Burn](#burn)
    - [Create a new burn](#create-a-new-burn)
    - [Get a burn by burn UID](#get-a-burn-by-burn-uid)
    - [Get burns by user UID](#get-burns-by-user-uid)
  - [Deposit](#deposit)
    - [Get deposit details for a user](#get-deposit-details-by-user-uid)
  - [Collection](#collection)
    - [Get a collection by UID](#get-a-collection-by-collection-uid)
  - [Allocation](#allocation)
    - [Create a new allocation](#create-a-new-allocation)
    - [Get an allocation by UID](#get-an-allocation-by-allocation-uid)
    - [Get allocations by user UID](#get-allocations-by-user-uid)
  - [Claim](#claim)
    - [Create a new claim](#create-a-new-claim)
    - [Get a claim by UID](#get-a-claim-by-claim-uid)
    - [Get claims by user UID](#get-claims-by-user-uid)
  - [Reward](#reward)
    - [Get a reward by UID](#get-a-reward-by-reward-uid)
    - [Get a user's reward balance](#get-a-users-reward-balance)
  - [Handling Errors](#handling-errors)


## ✨ Getting started

Ensure you have registered for an account at [Original](https://app.getoriginal.com) before getting started.
You will need to create an app and note down your API key and secret from the [API Keys page](https://docs.getoriginal.com/docs/create-your-api-key) to use the Original SDK.

Install Original

```bash
$ pip install original-sdk
```

## 📚 Documentation

### Initialization

The Original SDK is set up to expose the Original API.

Read the full [Original API documentation](https://docs.getoriginal.com).


Create a new instance of the Original client by passing in your api key and secret, with the environment associated with that app.

### Development
For development apps, you must pass the environment:

```python
from original_sdk import OriginalClient, Environment

client = OriginalClient(api_key='YOUR_DEV_APP_API_KEY', api_secret='YOUR_DEV_APP_SECRET', env=Environment.Development)
```

### Production
For production apps, you can optionally pass the production environment:

```python
from original_sdk import OriginalClient, Environment

client = OriginalClient(api_key='YOUR_PROD_APP_API_KEY', api_secret='YOUR_PROD_APP_SECRET', env=Environment.Production)
```

or omit the environment, which will default to production:

```python
from original_sdk import OriginalClient

client = OriginalClient(api_key='YOUR_PROD_APP_API_KEY', api_secret='YOUR_PROD_APP_SECRET')
```

### Async Client
There is also an async client available for use with async/await syntax:

```python
from original_sdk import OriginalAsyncClient, Environment

client = OriginalAsyncClient(api_key='YOUR_DEV_APP_API_KEY', api_secret='YOUR_DEV_APP_SECRET', env=Environment.Development)
```

## User

The user methods exposed by the sdk are used to create and retrieve users from the Original API.

### Create a new user

```python
# Returns a response object. Access the user's UID through the `data` attribute.
create_response = client.create_user()
new_user_uid = create_response['data']['uid']
# Sample create_response:
{
    "success": True,
    "data": {
        "uid": "175324281338"
    }
}

# You can also pass in a user_external_id and/or email for your external reference.
# The user_external_id and/or email supplied must be unique per app
create_response = client.create_user(email='YOUR_EMAIL', user_external_id='YOUR_USER_EXTERNAL_ID')
new_user_uid = create_response['data']['uid']
# ...
```

### Get a user by UID
```python
# Get a user by UID
# Returns their details in a response object if the user exists. If not, a 404 client error will be raised.
user_response = client.get_user(new_user_uid)
user_details = user_response['data']  # Contains user details such as UID, email, etc.
# Sample user_response:
{
    "success": True,
    "data": {
        "uid": "754566475542",
        "user_external_id": "user_external_id_1",
        "created_at": "2024-02-26T13:12:31.798296Z",
        "email": "user_email@email.com",
        "wallets": [
            { 
                "address": "0x1d6169328e0a2e0a0709115d1860c682cf8d1398",
                "chain_id": 80001,
                "explorer_url": "https://amoy.polygonscan.com/address/0x1d6169328e0a2e0a0709115d1860c682cf8d1398"
                "network": "Amoy",
            }
        ]
    }
}
```

### Get a user by email
```python
# Get a user by email
# Attempts to retrieve a user by their email address. If the user does not exist, `data` will be None.
user_by_email_response = client.get_user_by_email('YOUR_EMAIL')
user_by_email_details = user_by_email_response['data']
# Sample user_by_email_response on success:
{
    "success": True,
    "data": {
        "uid": "754566475542",
        "user_external_id": "user_external_id_1",
        "created_at": "2024-02-26T13:12:31.798296Z",
        "email": "user_email@email.com",
        "wallet_address": "0xa22f2dfe189ed3d16bb5bda5e5763b2919058e40"
    }
}

# Sample user_by_email_response (if user does not exist) on failure
{
    "success": False,
    "data": None
}
```

### Get a user by user external ID
```python
# Get a user by user external ID
# Retrieves a user by their user external ID. If the user does not exist, `data` will be None.
user_by_user_external_id_response = client.get_user_by_user_external_id('YOUR_USER_EXTERNAL_ID')
user_by_user_external_details = user_by_user_external_id_response['data']
# Sample user_by_user_external_id_response on success:
{
    "success": True,
    "data": {
        "uid": "754566475542",
        "user_external_id": "user_external_id",
        "created_at": "2024-02-26T13:12:31.798296Z",
        "email": "user_email@email.com",
        "wallet_address": "0xa22f2dfe189ed3d16bb5bda5e5763b2919058e40"
    }
}
# Sample user_by_user_external_id_response on failure:
{
    "success": False,
    "data": None
}
```

## Asset

The asset methods exposed by the sdk are used to create (mint) assets and retrieve assets from the Original API.

### Create a new asset

```python
# prepare the new asset params
new_asset_params = {
    "user_uid": "324167489835",
    "asset_external_id": "asset_external_id_1",
    "collection_uid": "221137489875",
    "sale_price_in_usd": 9.99,
    "data": {
        "name": "Dave Starbelly",
        "unique_name": True,
        "image_url": "https://storage.googleapis.com/opensea-prod.appspot.com/puffs/3.png",
        "store_image_on_ipfs": True,
        "description": "Friendly OpenSea Creature that enjoys long swims in the ocean.",
        "external_url": "https://openseacreatures.io/3",
        "attributes": [
            {
                "trait_type": "Base",
                "value": "Starfish"
            },
            {
                "trait_type": "Stamina Increase",
                "display_type": "boost_percentage",
                "value": 10
            },
        ]
    }
}

# Create a new asset
create_asset_response = client.create_asset(**new_asset_params)
new_asset_uid = create_asset_response['data']['uid']
# Sample create_asset_response:
{
    "success": True,
    "data": {
        "uid": "151854912345"
    }
}
```

### Get an asset by asset UID

```python
# Get an asset by UID, returns the asset details in a response object if the asset exists. If not, a 404 client error will be raised.
asset_response = client.get_asset(new_asset_uid)
asset_details = asset_response['data']
# Sample asset_response:
{
    "success": True,
    "data": {
        "uid": "151854912345",
        "name": "random name #2",
        "asset_external_id": "asset_external_id_1",
        "collection_uid": "471616646163",
        "collection_name": "Test SDK Collection 1",
        "token_id": 2,
        "created_at": "2024-02-16T11:33:19.577827Z",
        "is_minted": True,
        "is_burned": False,
        "is_transferring": False,
        "is_transferable": True,
        "is_editing": False,
        "mint_for_user_uid": "885810911461",
        "owner_user_uid": "885810911461",
        "owner_address": "0x32e28bfe647939d073d39113c697a11e3065ea97",
        "metadata": {
            "name": "random name",
            "image": "https://cryptopunks.app/cryptopunks/cryptopunk1081.png",
            "description": "nft_description",
            "original_id": "151854912345",
            "external_url": "external_url@example.com",
            "org_image_url": "https://cryptopunks.app/cryptopunks/cryptopunk1081.png",
            "attributes": [
                {
                    "trait_type": "Stamina Increase",
                    "display_type": "boost_percentage",
                    "value": 10
                }
            ]
        },
        "explorer_url": "https://mumbai.polygonscan.com/token/0x124a6755ee787153bb6228463d5dc3a02890a7db?a=2",
        "token_uri": "https://storage.googleapis.com/{...}.json"
    }
}

```

### Get assets by user UID

```python
# Get assets by the owner's UID
assets_response = client.get_assets_by_user_uid("user_uid")
assets_list = assets_response['data']
# Sample assets_response (showing one asset for brevity, wrapped in a response object):
{
    "success": True,
    "data": [
        {
            "uid": "151854912345",
            "name": "random name #2",
            "asset_external_id": "asset_external_id_1",
            "collection_uid": "471616646163",
            "collection_name": "Test SDK Collection 1",
            "token_id": 2,
            "created_at": "2024-02-16T11:33:19.577827Z",
            "is_minted": True,
            "is_burned": False,
            "is_transferring": False,
            "is_transferable": True,
            "is_editing": False,
            "mint_for_user_uid": "885810911461",
            "owner_user_uid": "885810911461",
            "owner_address": "0x32e28bfe647939d073d39113c697a11e3065ea97",
            "metadata": {
                "name": "random name",
                "image": "https://cryptopunks.app/cryptopunks/cryptopunk1081.png",
                "description": "nft_description",
                "original_id": "151854912345",
                "external_url": "external_url@example.com",
                "org_image_url": "https://cryptopunks.app/cryptopunks/cryptopunk1081.png",
                "attributes": [
                    {
                        "trait_type": "Stamina Increase",
                        "display_type": "boost_percentage",
                        "value": 10
                    }
                ]
            },
            "explorer_url": "https://mumbai.polygonscan.com/token/0x124a6755ee787153bb6228463d5dc3a02890a7db?a=2",
            "token_uri": "https://storage.googleapis.com/original-production-media/data/metadata/9ac0dad4-75ae-4406-94fd-1a0f6bf75db3.json"
        }
        # Additional assets would be listed here
    ]
}

```

### Edit an asset

NOTE: Editing an asset will overwrite the existing asset data with the new data provided.
If you want to maintain any of the existing data, you must include it in the new data.

NOTE: You must include all the required fields. See https://docs.getoriginal.com/docs/edit-asset for more information.
```python
# prepare the edit asset params
edit_asset_params = {
    "data": {
        "name": "Dave Starbelly Edited",
        "unique_name": True,
        "image_url": "https://storage.googleapis.com/opensea-prod.appspot.com/puffs/3.png",
        "description": "Friendly OpenSea Creature that enjoys long swims in the ocean. Edited",
        "attributes": [
            {
                "trait_type": "Base",
                "value": "Starfish"
            },
        ]
    }
}

# Edits an asset by UID, by passing in the new asset data
edit_asset_response = client.edit_asset(new_asset_uid, **edit_asset_params)
edit_success = edit_asset_response['success']
# Sample edit_asset_response:
{
    "success": True,
    "data": None
}
```

## Transfer

The transfer methods exposed by the sdk are used to transfer assets from one user to another wallet.

### Create a new transfer

```python

# Prepare the transfer parameters
transfer_params = {
    "asset_uid": "708469717542",
    "from_user_uid": "149997600351",
    "to_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
}

# Create a transfer of an asset
transfer_response = client.create_transfer(**transfer_params)
transfer_uid = transfer_response['data']['uid']
# Sample transfer_response:
{
    "success": True,
    "data": {
        "uid": "883072660397"
    }
}
```

### Get a transfer by transfer UID

```python
# Get a transfer by transfer UID, will throw a 404 Not Found error if the transfer does not exist
transfer_response = client.get_transfer("883072660397")
transfer_details = transfer_response['data']
# Sample transfer_response:
{
    "success": True,
    "data": {
        "uid": "883072660397",
        "status": "done",
        "asset_uid": "708469717542",
        "from_user_uid": "149997600351",
        "to_address": "0xe02522d0ac9f53e35a56f42cd5e54fc7b5a12f05",
        "created_at": "2024-02-26T10:20:17.668254Z"
    }
}
```

### Get transfers by user UID

```python
# Get transfers by user UID
transfers_response = client.get_transfers_by_user_uid("149997600351")
transfers_list = transfers_response['data']
# Sample transfers_response:
{
    "success": True,
    "data": [
        {
            "uid": "883072660397",
            "status": "done",
            "asset_uid": "708469717542",
            "from_user_uid": "149997600351",
            "to_address": "0xe02522d0ac9f53e35a56f42cd5e54fc7b5a12f05",
            "created_at": "2024-02-26T10:20:17.668254Z"
        }
        # Additional transfers would be listed here
    ]
}
```

## Burn

The burn methods exposed by the sdk are used to burn assets from a user's wallet.

### Create a new burn
```python

# Prepare the burn parameters
burn_params = {
    "asset_uid": "708469717542",
    "from_user_uid": "483581848722",
}

# Create a burn of an asset
burn_response = client.create_burn(**burn_params)
burn_uid = burn_response['data']['uid']
# Sample burn_response:
{
    "success": True,
    "data": {
        "uid": "365684656925",
    }
}
```

### Get a burn by burn UID
```python

# Get a burn by UID, will throw a 404 Not Found error if the burn does not exist
burn_response = client.get_burn("365684656925")
burn_details = burn_response['data']
# Sample burn_response:
{
    "success": True,
    "data": {
        "uid": "365684656925",
        "status": "done",
        "asset_uid": "708469717542",
        "from_user_uid": "483581848722",
        "created_at": "2024-02-26T10:20:17.668254Z"
    }
}
```

### Get burns by user UID
```python
# Get burns by user UID
burns_response = client.get_burns_by_user_uid("483581848722")
burns_list = burns_response['data']
# Sample burns_response:
{
    "success": True,
    "data": [
        {
            "uid": "365684656925",
            "status": "done",
            "asset_uid": "708469717542",
            "from_user_uid": "483581848722",
            "created_at": "2024-02-26T10:22:47.848973Z"
        }
        # Additional burns would be listed here
    ]
}
```

## Deposit

The deposit methods exposed by the sdk are used to return the details for depositing assets.

### Get deposit details by user UID and collection UID
```python
# Get deposit details for a user and collection
deposit_response = client.get_deposit("user_uid", "collection_uid")
deposit_details = deposit_response['data']
# Sample deposit_response:
{
    "success": True,
    "data": {
        "network": "Amoy",
        "chain_id": 80002,
        "wallet_address": "0x1d6169328e0a2e0a0709115d1860c682cf8d1398",
        "qr_code_data": "ethereum:0x1d6169328e0a2e0a0709115d1860c682cf8d1398@80001"
    }
}
```

## Collection

The collection methods exposed by the sdk are used to retrieve collection details from the Original API.

### Get a collection by collection UID
```python
# Get a collection by UID, will throw a 404 Not Found error if the collection does not exist
collection_response = client.get_collection('221137489875')
collection_details = collection_response['data']
# Sample collection_response:
{
    "success": True,
    "data": {
        "uid": "471616646163",
        "name": "Test SDK Collection 1",
        "status": "deployed",
        "type": "ERC721",
        "created_at": "2024-02-13T10:45:56.952745Z",
        "editable_assets": True,
        "contract_address": "0x124a6755ee787153bb6228463d5dc3a02890a7db",
        "symbol": "SYM",
        "description": "Description of the collection",
        "explorer_url": "https://mumbai.polygonscan.com/address/0x124a6755ee787153bb6228463d5dc3a02890a7db"
    }
}
```

## Allocation

The allocation methods exposed by the sdk are used to create and retrieve allocations from the Original API.

### Create a new allocation
```python

# Prepare the allocation parameters
allocation_params = {
    "amount": 123.123,
    "nonce": "nonce1",
    "to_user_uid": "483581848722",
    "reward_uid": "708469717542",
}

# Create an allocation
allocation_response = client.create_allocation(**allocation_params)
allocation_uid = allocation_response['data']['uid']
# Sample allocation_response:
{
    "success": True,
    "data": {
        "uid": "365684656925",
    }
}
```

### Get an allocation by allocation UID
```python

# Get an allocation by UID, will throw a 404 Not Found error if the allocation does not exist
allocation_response = client.get_allocation("365684656925")
allocation_details = allocation_response['data']
# Sample allocation_response:
{
    "success": True,
    "data": {
        "uid": "365684656925",
        "status": "done",
        "reward_uid": "reward_uid",
        "to_user_uid": "754566475542",
        "amount": 123.123,
        "nonce": "nonce1",
        "created_at": "2024-02-16T11:33:19.577827Z"
    }
}
```

### Get allocations by user UID
```python
# Get allocations by user UID
allocations_response = client.get_allocations_by_user_uid("483581848722")
allocations_list = allocations_response['data']
# Sample allocations_response:
{
    "success": True,
    "data": [
        {
            "uid": "365684656925",
            "status": "done",
            "reward_uid": "reward_uid",
            "to_user_uid": "754566475542",
            "amount": 123.123,
            "nonce": "nonce1",
            "created_at": "2024-02-16T11:33:19.577827Z"
        }
        # Additional allocations would be listed here
    ]
}
```

## Claim

The claim methods exposed by the sdk are used to create and retrieve claims from the Original API.

### Create a new claim
```python

# Prepare the claim parameters
claim_params = {
    "from_user_uid": "483581848722",
    "reward_uid": "708469717542",
    "to_address": '0x4881ab2f73c48a54b907a8b697b270f490768e6d'
}

# Create a claim
claim_response = client.create_claim(**claim_params)
claim_uid = claim_response['data']['uid']
# Sample claim_response:
{
    "success": True,
    "data": {
        "uid": "365684656925",
    }
}
```

### Get a claim by claim UID
```python

# Get a claim by UID, will throw a 404 Not Found error if the claim does not exist
claim_response = client.get_claim("365684656925")
claim_details = claim_response['data']
# Sample claim_response:
{
    "success": True,
    "data": {
        "uid": "365684656925",
        "status": "done",
        "reward_uid": "708469717542",
        "from_user_uid": "754566475542",
        "to_address": "0x4881ab2f73c48a54b907a8b697b270f490768e6d",
        "amount": 123.123,
        "created_at": "2024-02-16T11:33:19.577827Z"
    }
}
```

### Get claims by user UID
```python
# Get claims by user UID
claims_response = client.get_claims_by_user_uid("483581848722")
claims_list = claims_response['data']
# Sample claims_response:
{
    "success": True,
    "data": [
        {
            "uid": "365684656925",
            "status": "done",
            "reward_uid": "708469717542",
            "from_user_uid": "754566475542",
            "to_address": "0x4881ab2f73c48a54b907a8b697b270f490768e6d",
            "amount": 123.123,
            "created_at": "2024-02-16T11:33:19.577827Z"
        }
        # Additional claims would be listed here
    ]
}
```

## Reward

The reward methods exposed by the sdk are used to retrieve reward details from the Original API.

### Get a reward by reward UID
```python
# Get a reward by UID, will throw a 404 Not Found error if the reward does not exist
reward_response = client.get_reward('221137489875')
reward_details = reward_response['data']
# Sample reward_response:
{
    "success": True,
    "data": {
        "uid": "151854912345",
        "name": "Test SDK Reward 1",
        "status": "deployed",
        "token_type": "ERC20",
        "token_name": "TestnetORI",
        "created_at": "2024-02-13T10:45:56.952745Z",
        "contract_address": "0x124a6755ee787153bb6228463d5dc3a02890a7db",
        "withdraw_receiver": "0x4881ab2f73c48a54b907a8b697b270f490768e6d",
        "description": "Description of the reward",
        "explorer_url": "https://mumbai.polygonscan.com/address/0x124a6755ee787153bb6228463d5dc3a02890a7db"
    }
}
```

### Get a user's reward balance
```python
# Get a user's reward balance, will throw a 404 Not Found error if the reward does not exist
reward_response = client.get_balance(reward_uid='221137489875', user_uid='754566475542')
reward_details = reward_response['data']
# Sample reward_response:
{
    "success": True,
    "data": {
        "reward_uid": "221137489875",
        "user_uid": "754566475542",
        "amount": 100.0
    }
}
```

## Handling Errors

If something goes wrong, you will receive well typed error messages.

```python
class ClientError(OriginalError): ...
class ServerError(OriginalError): ...
class ValidationError(OriginalError): ...
```

All errors inherit from an `OriginalError` class where you can access the standard properties from the `Exception` class as well as the following:

```python
class OriginalErrorCode(Enum):
    client_error = "client_error"
    server_error = "server_error"
    validation_error = "validation_error"
    

class OriginalError(Exception):
    def __init__(self, message, status, data, code):
        self.message = message
        self.status = status
        self.data = data
        self.code = code.value # 'client_error' | 'server_error' | 'validation_error'
}
```

So when an error occurs, you can either catch all using the OriginalError class:

```python
from original_sdk import OriginalError

try:
    result = client.create_user(email='invalid_email', user_external_id='user_external_id');
except OriginalError as e:
    # handle all errors
```

or specific errors:

```python
from original_sdk import ClientError, ServerError, ValidationError

try:
    result = client.create_user(email='invalid_email', user_external_id='user_external_id');
except ClientError as e:
    # handle client errors
except ServerError as e:
    # handle server errors
except ValidationError as e:
    # handle validation errors
```

The error will have this structure:
```python
except OriginalError as error:
    # error.code == 'client_error' | 'server_error' | 'validation_error'
    # error.status == 400 | 404 | ...
    # error.message == 'Not Found' | 'Enter a valid email address.' | ...
    # error.data == { 
    #   "success": False, 
    #   "error": { 
    #       "type": "validation_error", 
    #       "detail": { 
    #           "code": "invalid",
    #           "message": "Enter a valid email address.",
    #           "field_name": "email"
    #        }  
    #    }
    # }
```

Please note, if you plan to parse the error detail, it can also be an array if there are multiple errors.
```python
    # ...
    # "detail": [
    #     {
    #         "code": "null",
    #         "message": "This field may not be null.",
    #         "field_name": "user_external_id"
    #     },
    #     {
    #         "code": "invalid",
    #         "message": "Enter a valid email address.",
    #         "field_name": "email"
    #     }
    # ]
```

If it's a client (SDK) error and not a json response error from our server/REST API, we will return data as a string.
```python
    # "error.data": "Not Found"
    # "error.status": 404
    # "error.code": "client_error"
```
