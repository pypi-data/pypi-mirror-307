import json
from dataclasses import dataclass
from uuid import UUID


@dataclass
class VerificationToken:
    api_endpoint: str
    verification_id: UUID
    encrypted_access_token: str

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        return cls(
            api_endpoint=data['apiEndpoint'],
            verification_id=UUID(data['verificationId']),
            encrypted_access_token=data['encryptedAccessToken'],
        )
