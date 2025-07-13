from typing import TypedDict


class DevicePayload(TypedDict):
    id: int
    model: str
    carrier: str
    firmware: str


class ClanPayload(TypedDict):
    id: str
    name: str


class Payload(TypedDict):
    player_id: str
    credential: str
    created: str
    modified: str
    last_session: str
    total_spent: int
    total_refund: int
    total_transactions: int
    last_purchase: str
    active_campaigns: list[str]
    devices: list[DevicePayload]
    level: int
    xp: int
    total_playtime: int
    country: str
    language: str
    birthdate: str
    gender: str
    inventory: dict[str, int]
    clan: ClanPayload


player_payload: Payload = {
    "player_id": "97983be2-98b7-11e7-90cf-082e5f28d836",
    "credential": "apple_credential",
    "created": "2021-01-10T13:37:17Z",
    "modified": "2021-01-23T13:37:17Z",
    "last_session": "2021-01-23T13:37:17Z",
    "total_spent": 400,
    "total_refund": 0,
    "total_transactions": 5,
    "last_purchase": "2021-01-22T13:37:17Z",
    "active_campaigns": [],
    "devices": [
        {
            "id": 1,
            "model": "apple iphone 11",
            "carrier": "vodafone",
            "firmware": "123",
        }
    ],
    "level": 3,
    "xp": 1000,
    "total_playtime": 144,
    "country": "CA",
    "language": "fr",
    "birthdate": "2000-01-10T13:37:17Z",
    "gender": "male",
    "inventory": {
        "cash": 123,
        "coins": 123,
        "item_1": 1,
        "item_34": 3,
        "item_55": 2,
    },
    "clan": {"id": "123456", "name": "Hello world clan"},
}
