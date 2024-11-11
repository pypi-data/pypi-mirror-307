from __future__ import absolute_import

# flake8: noqa

# import apis into api package
from zarban.service.openapi_client.api.accounts_api import AccountsApi
from zarban.service.openapi_client.api.addresses_api import AddressesApi
from zarban.service.openapi_client.api.borrows_api import BorrowsApi
from zarban.service.openapi_client.api.collector_api import CollectorApi
from zarban.service.openapi_client.api.deposits_api import DepositsApi
from zarban.service.openapi_client.api.ilks_api import IlksApi
from zarban.service.openapi_client.api.lending_pool_api import LendingPoolApi
from zarban.service.openapi_client.api.logs_api import LogsApi
from zarban.service.openapi_client.api.orders_api import OrdersApi
from zarban.service.openapi_client.api.permissions_api import PermissionsApi
from zarban.service.openapi_client.api.permit_api import PermitApi
from zarban.service.openapi_client.api.prices_api import PricesApi
from zarban.service.openapi_client.api.proxies_api import ProxiesApi
from zarban.service.openapi_client.api.stable_coin_system_api import StableCoinSystemApi
from zarban.service.openapi_client.api.swap_api import SwapApi
from zarban.service.openapi_client.api.vaults_api import VaultsApi
from zarban.service.openapi_client.api.websocket_api import WebsocketApi
