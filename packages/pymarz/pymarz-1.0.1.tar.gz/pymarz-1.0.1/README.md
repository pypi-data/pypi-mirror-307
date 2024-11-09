
# pymarz
[![Stars](https://img.shields.io/github/stars/SSaeedhoseini/pymarz.svg?style=social)](https://github.com/SSaeedhoseini/pymarz/stargazers)
[![Forks](https://img.shields.io/github/forks/SSaeedhoseini/pymarz.svg?style=social)](https://github.com/SSaeedhoseini/pymarz/network/members)
[![Issues](https://img.shields.io/github/issues/SSaeedhoseini/pymarz.svg)](https://github.com/SSaeedhoseini/pymarz/issues)
[![Supported python versions](https://img.shields.io/pypi/pyversions/pymarz.svg)](https://pypi.python.org/pypi/pymarz)
[![Downloads](https://img.shields.io/pypi/dm/pymarz.svg)](https://pypi.python.org/pypi/pymarz)
[![PyPi Package Version](https://img.shields.io/pypi/v/pymarz)](https://pypi.python.org/pypi/pymarz)

**pymarz** is an asynchronous Python library designed for interacting with [Marzban](https://github.com/Gozargah/Marzban). It provides comprehensive methods for managing administrators, users, nodes, and system statistics.

## Requirements.

Python 3.7+

## Installation & Usage

### pip install
```sh
pip install pymarz
```
### install from repository

you can install directly form github repository using:

```sh
pip install git+https://github.com/SSaeedHoseini/pymarz.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/SSaeedHoseini/pymarz.git`)

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)


## Getting Started
Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from asyncio import run

from pymarz import MarzAPI

pyload = {
    "url": "your-domain",
    "username": "admin-username",
    "password": "admin-password",
}


async def main():
    client = MarzAPI(**pyload)

    hosts = await client.host.get_all()

    print(hosts)


if __name__ == "__main__":
    try:
        run(main())
    except Exception as e:
        print(str(e))

```


## Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AdminApi* | [**admin_token**](docs/AdminApi.md#admin_token) | **POST** /api/admin/token | Admin Token
*AdminApi* | [**create_admin**](docs/AdminApi.md#create_admin) | **POST** /api/admin | Create Admin
*AdminApi* | [**get_admins**](docs/AdminApi.md#get_admins) | **GET** /api/admins | Get Admins
*AdminApi* | [**get_current_admin**](docs/AdminApi.md#get_current_admin) | **GET** /api/admin | Get Current Admin
*AdminApi* | [**modify_admin**](docs/AdminApi.md#modify_admin) | **PUT** /api/admin/{username} | Modify Admin
*AdminApi* | [**remove_admin**](docs/AdminApi.md#remove_admin) | **DELETE** /api/admin/{username} | Remove Admin
*CoreApi* | [**get_core_config**](docs/CoreApi.md#get_core_config) | **GET** /api/core/config | Get Core Config
*CoreApi* | [**get_core_stats**](docs/CoreApi.md#get_core_stats) | **GET** /api/core | Get Core Stats
*CoreApi* | [**modify_core_config**](docs/CoreApi.md#modify_core_config) | **PUT** /api/core/config | Modify Core Config
*CoreApi* | [**restart_core**](docs/CoreApi.md#restart_core) | **POST** /api/core/restart | Restart Core
*NodeApi* | [**add_node**](docs/NodeApi.md#add_node) | **POST** /api/node | Add Node
*NodeApi* | [**get_node**](docs/NodeApi.md#get_node) | **GET** /api/node/{node_id} | Get Node
*NodeApi* | [**get_node_settings**](docs/NodeApi.md#get_node_settings) | **GET** /api/node/settings | Get Node Settings
*NodeApi* | [**get_nodes**](docs/NodeApi.md#get_nodes) | **GET** /api/nodes | Get Nodes
*NodeApi* | [**get_usage**](docs/NodeApi.md#get_usage) | **GET** /api/nodes/usage | Get Usage
*NodeApi* | [**modify_node**](docs/NodeApi.md#modify_node) | **PUT** /api/node/{node_id} | Modify Node
*NodeApi* | [**reconnect_node**](docs/NodeApi.md#reconnect_node) | **POST** /api/node/{node_id}/reconnect | Reconnect Node
*NodeApi* | [**remove_node**](docs/NodeApi.md#remove_node) | **DELETE** /api/node/{node_id} | Remove Node
*SubscriptionApi* | [**user_get_usage**](docs/SubscriptionApi.md#user_get_usage) | **GET** /sub/{token}/usage | User Get Usage
*SubscriptionApi* | [**user_subscription**](docs/SubscriptionApi.md#user_subscription) | **GET** /sub/{token}/ | User Subscription
*SubscriptionApi* | [**user_subscription_info**](docs/SubscriptionApi.md#user_subscription_info) | **GET** /sub/{token}/info | User Subscription Info
*SubscriptionApi* | [**user_subscription_with_client_type**](docs/SubscriptionApi.md#user_subscription_with_client_type) | **GET** /sub/{token}/{client_type} | User Subscription With Client Type
*SystemApi* | [**get_hosts**](docs/SystemApi.md#get_hosts) | **GET** /api/hosts | Get Hosts
*SystemApi* | [**get_inbounds**](docs/SystemApi.md#get_inbounds) | **GET** /api/inbounds | Get Inbounds
*SystemApi* | [**get_system_stats**](docs/SystemApi.md#get_system_stats) | **GET** /api/system | Get System Stats
*SystemApi* | [**modify_hosts**](docs/SystemApi.md#modify_hosts) | **PUT** /api/hosts | Modify Hosts
*UserApi* | [**add_user**](docs/UserApi.md#add_user) | **POST** /api/user | Add User
*UserApi* | [**delete_expired_users**](docs/UserApi.md#delete_expired_users) | **DELETE** /api/users/expired | Delete Expired Users
*UserApi* | [**get_expired_users**](docs/UserApi.md#get_expired_users) | **GET** /api/users/expired | Get Expired Users
*UserApi* | [**get_user**](docs/UserApi.md#get_user) | **GET** /api/user/{username} | Get User
*UserApi* | [**get_user_usage**](docs/UserApi.md#get_user_usage) | **GET** /api/user/{username}/usage | Get User Usage
*UserApi* | [**get_users**](docs/UserApi.md#get_users) | **GET** /api/users | Get Users
*UserApi* | [**get_users_usage**](docs/UserApi.md#get_users_usage) | **GET** /api/users/usage | Get Users Usage
*UserApi* | [**modify_user**](docs/UserApi.md#modify_user) | **PUT** /api/user/{username} | Modify User
*UserApi* | [**remove_user**](docs/UserApi.md#remove_user) | **DELETE** /api/user/{username} | Remove User
*UserApi* | [**reset_user_data_usage**](docs/UserApi.md#reset_user_data_usage) | **POST** /api/user/{username}/reset | Reset User Data Usage
*UserApi* | [**reset_users_data_usage**](docs/UserApi.md#reset_users_data_usage) | **POST** /api/users/reset | Reset Users Data Usage
*UserApi* | [**revoke_user_subscription**](docs/UserApi.md#revoke_user_subscription) | **POST** /api/user/{username}/revoke_sub | Revoke User Subscription
*UserApi* | [**set_owner**](docs/UserApi.md#set_owner) | **PUT** /api/user/{username}/set-owner | Set Owner
*UserTemplateApi* | [**add_user_template**](docs/UserTemplateApi.md#add_user_template) | **POST** /api/user_template | Add User Template
*UserTemplateApi* | [**get_user_template_endpoint**](docs/UserTemplateApi.md#get_user_template_endpoint) | **GET** /api/user_template/{id} | Get User Template Endpoint
*UserTemplateApi* | [**get_user_templates**](docs/UserTemplateApi.md#get_user_templates) | **GET** /api/user_template | Get User Templates
*UserTemplateApi* | [**modify_user_template**](docs/UserTemplateApi.md#modify_user_template) | **PUT** /api/user_template/{id} | Modify User Template
*UserTemplateApi* | [**remove_user_template**](docs/UserTemplateApi.md#remove_user_template) | **DELETE** /api/user_template/{id} | Remove User Template
*DefaultApi* | [**base**](docs/DefaultApi.md#base) | **GET** / | Base


## Documentation For Models

 - [Admin](docs/Admin.md)
 - [AdminCreate](docs/AdminCreate.md)
 - [AdminModify](docs/AdminModify.md)
 - [CoreStats](docs/CoreStats.md)
 - [HTTPValidationError](docs/HTTPValidationError.md)
 - [LocationInner](docs/LocationInner.md)
 - [NodeCreate](docs/NodeCreate.md)
 - [NodeModify](docs/NodeModify.md)
 - [NodeResponse](docs/NodeResponse.md)
 - [NodeSettings](docs/NodeSettings.md)
 - [NodeStatus](docs/NodeStatus.md)
 - [NodeUsageResponse](docs/NodeUsageResponse.md)
 - [NodesUsageResponse](docs/NodesUsageResponse.md)
 - [Port](docs/Port.md)
 - [ProxyHost](docs/ProxyHost.md)
 - [ProxyHostALPN](docs/ProxyHostALPN.md)
 - [ProxyHostFingerprint](docs/ProxyHostFingerprint.md)
 - [ProxyHostSecurity](docs/ProxyHostSecurity.md)
 - [ProxyInbound](docs/ProxyInbound.md)
 - [ProxyTypes](docs/ProxyTypes.md)
 - [SubscriptionUserResponse](docs/SubscriptionUserResponse.md)
 - [SystemStats](docs/SystemStats.md)
 - [Token](docs/Token.md)
 - [UserCreate](docs/UserCreate.md)
 - [UserDataLimitResetStrategy](docs/UserDataLimitResetStrategy.md)
 - [UserModify](docs/UserModify.md)
 - [UserResponse](docs/UserResponse.md)
 - [UserStatus](docs/UserStatus.md)
 - [UserStatusCreate](docs/UserStatusCreate.md)
 - [UserStatusModify](docs/UserStatusModify.md)
 - [UserTemplateCreate](docs/UserTemplateCreate.md)
 - [UserTemplateModify](docs/UserTemplateModify.md)
 - [UserTemplateResponse](docs/UserTemplateResponse.md)
 - [UserUsageResponse](docs/UserUsageResponse.md)
 - [UserUsagesResponse](docs/UserUsagesResponse.md)
 - [UsersResponse](docs/UsersResponse.md)
 - [UsersUsagesResponse](docs/UsersUsagesResponse.md)
 - [ValidationError](docs/ValidationError.md)


## Project Links
 - **PyPI**: [marzban](https://pypi.org/project/pymarz/)
- **GitHub Repository**: [pymarz](https://github.com/SSaeedhoseini/pymarz)

## Contributing

We welcome contributions! If you encounter any issues or have suggestions for improvements, please feel free to [open an issue](https://github.com/SSaeedhoseini/pymarz/issues) or submit a Pull Request (PR).

## Support

If you have any questions or need assistance, you can contact the author via:
- **Telegram**: [@SSaeedhoseini](https://t.me/SSaeedhoseini)

## License

This project is licensed under the MIT License. For more details, refer to the [LICENSE file](https://github.com/SSaeedhoseini/pymarz/blob/production/LICENSE).
