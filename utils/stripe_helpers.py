"""Stripe test card constants from https://docs.stripe.com/testing"""

class CardDetails:
    """Class to hold card details for testing."""
    def __init__(self, number: str, expiry: str, cvc: str):
        self.number = number
        self.expiry = expiry
        self.cvc = cvc

VALID_CARD_DETAILS = CardDetails(number="4242424242424242",
                                expiry="12/30",
                                cvc="123"
                                )

DECLINED_CARD_DETAILS = CardDetails(number="4000000000000002",
                                    expiry="12/30",
                                    cvc="123"
                                    )

INSUFFICIENT_FUNDS_CARD_DETAILS = CardDetails(number="4000000000009995",
                                    expiry="12/30",
                                    cvc="123"
                                    )

EXPIRED_CARD_DETAILS = CardDetails(number="4000000000000069",
                                expiry="12/30",
                                cvc="123"
                                )
