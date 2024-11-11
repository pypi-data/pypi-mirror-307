"""
Zarban API
~~~~~~~~~~~~~

API for Zarban Wallet and services.

:copyright: (c) 2024 by Zarban.
:license: MIT, see LICENSE for more details.
"""

from .service import openapi_client as service_api 
from .wallet import openapi_client as wallet_api

__all__ = ["service_api", "wallet_api"]