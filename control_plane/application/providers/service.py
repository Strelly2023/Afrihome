from dataclasses import dataclass
from core.kernel.invariants import assert_not_none
from core.errors import ValidationError, AuthorizationError
from control_plane.application.execution.models import ExecutionFrame
from .models import (
    ProviderRef, ProviderConfig, ProviderContext,
    CredentialPurpose, ResolvedCredential,
)
from .protocols import ProviderConfigRepository, CredentialResolver, ProviderPolicy

@dataclass(frozen=True, slots=True)
class ProviderConfigService:
    """
    Orchestration-only provider surface:
      1) Read non-sensitive ProviderConfig via repository protocol
      2) (Optionally) resolve credential *reference* via resolver protocol
      3) Apply pure ProviderPolicy guards (governance) before use
    NO IO, NO cleartext secrets, NO SDK calls in application layer.
    """
    repo: ProviderConfigRepository
    creds: CredentialResolver
    policy: ProviderPolicy | None = None

    # ---------- Queries ----------

    def get_config(
        self,
        frame: ExecutionFrame,
        provider_name: str,
        *,
        version: str | None = None
    ) -> ProviderConfig:
        assert_not_none(frame, "frame")
        name = (provider_name or "").strip().lower()
        if not name:
            raise ValidationError("provider_name must be a non-empty string")

        ref = ProviderRef(name=name, version=version)
        cfg = self.repo.get(frame.tenant_id, ref)
        if cfg is None:
            raise ValidationError(f"Provider config not found for '{name}'")
        return cfg

    def is_enabled(
        self,
        frame: ExecutionFrame,
        provider_name: str,
        *,
        version: str | None = None
    ) -> bool:
        cfg = self.get_config(frame, provider_name, version=version)
        return bool(cfg.enabled)

    def require_enabled(
        self,
        frame: ExecutionFrame,
        provider_name: str,
        *,
        version: str | None = None
    ) -> ProviderConfig:
        cfg = self.get_config(frame, provider_name, version=version)
        if not cfg.enabled:
            raise AuthorizationError(f"Provider '{cfg.provider.name}' disabled for tenant")
        self._check_policy(frame, cfg)
        return cfg

    # ---------- Context assembly ----------

    def build_context(
        self,
        frame: ExecutionFrame,
        provider_name: str,
        *,
        version: str | None = None,
        purpose: CredentialPurpose = CredentialPurpose.DEFAULT,
        require_enabled: bool = True,
        resolve_credentials: bool = True,
    ) -> ProviderContext:
        """
        Build an immutable ProviderContext for downstream orchestration.
        NOTE:
          - Secrets are never returned; only SecretRef inside ResolvedCredential.
          - Policy is enforced if present.
        """
        assert_not_none(frame, "frame")
        ref = ProviderRef(name=(provider_name or "").strip().lower(), version=version)
        if not ref.name:
            raise ValidationError("provider_name must be a non-empty string")

        cfg = self.repo.get(frame.tenant_id, ref)
        if cfg is None:
            raise ValidationError(f"Provider config not found for '{ref.name}'")

        if require_enabled and not cfg.enabled:
            raise AuthorizationError(f"Provider '{ref.name}' disabled for tenant")

        self._check_policy(frame, cfg)

        cred: ResolvedCredential | None = None
        if resolve_credentials:
            cred = self.creds.resolve(frame.tenant_id, ref, purpose)

        return ProviderContext(config=cfg, credential=cred)

    # ---------- Internals ----------

    def _check_policy(self, frame: ExecutionFrame, cfg: ProviderConfig) -> None:
        if self.policy is None:
            return
        allowed, reason = self.policy.evaluate(frame.tenant_id, cfg)
        if not allowed:
            raise AuthorizationError(f"deny: provider policy — {reason}")