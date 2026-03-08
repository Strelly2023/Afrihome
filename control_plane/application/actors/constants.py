# control_plane/application/actors/constants.py
# Canonical actor-related inbound headers (keys are expected lowercased)
HDR_ACTOR_KIND = "x-actor-kind"  # USER | API_KEY | SYSTEM | OPERATOR
HDR_USER_ID = "x-user-id"  # required when kind=USER
HDR_ROLES = "x-roles"  # optional, comma-separated RoleName values
HDR_PRINCIPAL = "x-principal"  # optional, opaque principal (api key id, service name)
