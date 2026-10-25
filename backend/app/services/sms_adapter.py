from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import uuid
import datetime
import httpx
from ..config import settings

class SMSDeliveryResult:
    def __init__(
        self,
        success: bool,
        status: str, # "SIMULATED", "DELIVERED", "FAILED"
        provider: str,
        provider_message_id: Optional[str] = None,
        error_message: Optional[str] = None
    ):
        self.success = success
        self.status = status
        self.provider = provider
        self.provider_message_id = provider_message_id
        self.error_message = error_message

class BaseSMSProvider(ABC):
    @abstractmethod
    async def send_sms(self, to_number: str, message: str) -> SMSDeliveryResult:
        pass

class DemoSMSProvider(BaseSMSProvider):
    """
    Demo SMS provider that safely simulates message delivery.
    Does NOT connect to external networks or bill credit cards.
    Messages are logged cleanly and tagged as SIMULATED.
    """
    async def send_sms(self, to_number: str, message: str) -> SMSDeliveryResult:
        simulated_id = f"SIM-{uuid.uuid4().hex[:10].upper()}"
        print(f"\n[DEMO SMS GATEWAY] Message queued for {to_number}:")
        print(f"ID: {simulated_id}")
        print(f"Content:\n{message}\n" + "-"*50)
        
        return SMSDeliveryResult(
            success=True,
            status="SIMULATED",
            provider="demo",
            provider_message_id=simulated_id,
            error_message=None
        )

class TwilioSMSProvider(BaseSMSProvider):
    """
    Live SMS Provider using Twilio REST API.
    Only active if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN are provided.
    """
    async def send_sms(self, to_number: str, message: str) -> SMSDeliveryResult:
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        from_num = settings.TWILIO_FROM_NUMBER

        if not account_sid or not auth_token or not from_num:
            return SMSDeliveryResult(
                success=False,
                status="FAILED",
                provider="twilio",
                error_message="Twilio credentials (ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER) are not configured."
            )

        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    url,
                    auth=(account_sid, auth_token),
                    data={"From": from_num, "To": to_number, "Body": message}
                )
                if res.status_code in (200, 201):
                    data = res.json()
                    return SMSDeliveryResult(
                        success=True,
                        status="DELIVERED",
                        provider="twilio",
                        provider_message_id=data.get("sid")
                    )
                else:
                    return SMSDeliveryResult(
                        success=False,
                        status="FAILED",
                        provider="twilio",
                        error_message=f"Twilio API Error {res.status_code}: {res.text}"
                    )
        except Exception as e:
            return SMSDeliveryResult(
                success=False,
                status="FAILED",
                provider="twilio",
                error_message=str(e)
            )

class GenericWebhookSMSProvider(BaseSMSProvider):
    """
    Adapter for generic SMS gateway webhooks (e.g. Fast2SMS, MSG91, Textlocal).
    Sends a JSON payload containing { to: to_number, text: message }.
    """
    async def send_sms(self, to_number: str, message: str) -> SMSDeliveryResult:
        webhook_url = settings.SMS_WEBHOOK_URL
        if not webhook_url:
            return SMSDeliveryResult(
                success=False,
                status="FAILED",
                provider="generic_webhook",
                error_message="SMS_WEBHOOK_URL environment variable is not configured."
            )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    webhook_url,
                    json={"to": to_number, "text": message, "timestamp": datetime.datetime.utcnow().isoformat()}
                )
                if res.status_code in (200, 201, 202):
                    return SMSDeliveryResult(
                        success=True,
                        status="DELIVERED",
                        provider="generic_webhook",
                        provider_message_id=f"WEBHOOK-{res.status_code}"
                    )
                else:
                    return SMSDeliveryResult(
                        success=False,
                        status="FAILED",
                        provider="generic_webhook",
                        error_message=f"Webhook returned status {res.status_code}: {res.text}"
                    )
        except Exception as e:
            return SMSDeliveryResult(
                success=False,
                status="FAILED",
                provider="generic_webhook",
                error_message=str(e)
            )

def get_sms_provider() -> BaseSMSProvider:
    """Factory selecting the SMS gateway adapter."""
    if settings.DEMO_MODE:
        return DemoSMSProvider()
    if settings.SMS_PROVIDER == "twilio":
        return TwilioSMSProvider()
    if settings.SMS_PROVIDER == "generic_webhook":
        return GenericWebhookSMSProvider()
    return DemoSMSProvider()
