from typing import TypedDict, Optional, Dict, Any

from filum_utils.types.account import Account


class EngagementCampaign(TypedDict, total=False):
    id: str
    name: str
    account: Account
    data: Optional[Dict[str, Any]]
