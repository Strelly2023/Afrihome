from control_plane.governance.integrations import (
    ProviderConfig, ProviderKind, WebhookVerification, HttpMethod, SignatureAlgorithm
)

def test_integrations_governance_models():
    p = ProviderConfig(
        provider_key="stripe",
        kind=ProviderKind.PAYMENTS,
        display_name="Stripe",
        enabled=True,
        base_url="https://stripe.com/docs",
        event_namespace="provider.stripe",
        tags=(("region","global"),),
    )
    assert p.provider_key == "stripe" and p.enabled is True

    v = WebhookVerification(
        provider_key="stripe",
        path="/webhooks/stripe",
        methods=(HttpMethod.POST,),
        signature_header="stripe-signature",
        timestamp_header="stripe-timestamp",
        algorithm=SignatureAlgorithm.HMAC_SHA256,
        secret_ref="secret://providers/stripe/webhook",
        tolerance_ms=300000,
        scheme_prefix="v1=",
        required_headers=("content-type",),
        description="Verify Stripe hook with timestamp tolerance",
    )
    assert v.path == "/webhooks/stripe" and v.tolerance_ms == 300000