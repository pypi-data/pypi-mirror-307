import base64
import requests

from .model.verification_result import VerificationResult
from .model.verification_token import VerificationToken
from .aes_encryption import AesEncryption


class CaptchaManager:

    @staticmethod
    def get_verification_result(base64_secret_key, base64_verification_token):

        verification_token = CaptchaManager.__get_verification_token(base64_verification_token)
        decrypted_access_token = CaptchaManager.__decrypt_access_token(CaptchaManager.__get_secret_key(base64_secret_key), verification_token)

        return CaptchaManager.__fetch_verification_result(verification_token, decrypted_access_token)

    @staticmethod
    def __get_secret_key(base64_secret_key):
        try:
            return AesEncryption.to_aes_secret_key(base64_secret_key)
        except Exception as e:
            raise SecretKeyInvalidException() from e

    @staticmethod
    def __get_verification_token(verification_token):

        try:
            decoded_bytes = base64.b64decode(verification_token)
            decoded_string = decoded_bytes.decode('utf-8')
            verification_token_model = VerificationToken.from_json(decoded_string)
            return verification_token_model
        except Exception as e:
            raise VerificationTokenInvalidException() from e

    @staticmethod
    def __decrypt_access_token(secret_key, verification_token):

        try:
            return AesEncryption.decrypt_to_string(secret_key, verification_token.encrypted_access_token)
        except Exception as e:
            raise TokenDecryptionFailedException() from e

    @staticmethod
    def __fetch_verification_result(verification_token, access_token):

        url = f"{verification_token.api_endpoint}/verifications/{verification_token.verification_id}/assessments?accessToken={access_token}&pl=py"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return VerificationResult.from_json(data)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise VerificationNotFoundException() from e
            else:
                raise RuntimeError("Failed to retrieve verification result") from e
        except Exception as e:
            raise RuntimeError("Failed to retrieve verification result") from e


class SecretKeyInvalidException(Exception):
    pass

class TokenDecryptionFailedException(Exception):
    pass

class VerificationTokenInvalidException(Exception):
    pass

class VerificationNotFoundException(Exception):
    pass
