def test_allow_with_rbac_executes(
    handler, context, allow_decision, rbac_allow
):
    result = handler.authorize(
        decision=allow_decision,
        outcomes=(rbac_allow,),
        context=context,
    )

    assert result.actor == context.actor
    assert result.action == context.action
    assert result.resource == context.resource
    assert result.reasons == allow_decision.reasons
