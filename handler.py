"""AWS Lambda handler that emits deployment-bound Ultra13 runtime evidence."""

from __future__ import annotations

import json
import os

from ultra13_runtime.frameworks import OpenAIAgentsObserver


def _observer() -> OpenAIAgentsObserver | None:
    endpoint = os.getenv("ULTRA13_API_ENDPOINT", "").strip()
    token = os.getenv("ULTRA13_RUNTIME_TOKEN", "").strip()
    application = os.getenv("ULTRA13_APPLICATION_ID", "").strip()
    if not endpoint or not token or not application:
        return None
    return OpenAIAgentsObserver(
        endpoint,
        token,
        application,
        framework_version="0.19.4",
        capture_content=False,
    )


def lambda_handler(event: dict | None, _context: object) -> dict:
    event = event or {}
    action = str(event.get("action", "control"))
    observer = _observer()
    if observer is None:
        return {"statusCode": 200, "body": json.dumps({"telemetry": "not-configured", "action": action})}

    session = str(event.get("session", f"v2-e2e-{action}"))
    observer.emit_conformance()
    if action == "drift":
        observer.emit(
            "tool_call",
            "external_admin",
            agent_id="v2_release_agent",
            session_id=session,
            principal="github-actions",
            credential_type="oidc",
            scopes=["infra:admin"],
            resource="production-control-plane",
            resource_environment="production",
            destination="admin.example.invalid",
            input_source="ci-dispatch",
            input_trust="trusted",
            approval_required=True,
            approval_received=False,
            autonomy_mode="automatic",
        )
    else:
        observer.emit(
            "agent_execution",
            "v2_release_agent",
            agent_id="v2_release_agent",
            session_id=session,
            principal="github-actions",
            credential_type="oidc",
            input_source="ci-dispatch",
            input_trust="trusted",
        )
        observer.emit("model_call", "gpt-5-mini", agent_id="v2_release_agent", session_id=session)
        observer.emit(
            "tool_call",
            "read_status",
            agent_id="v2_release_agent",
            session_id=session,
            principal="github-actions",
            credential_type="oidc",
            scopes=["status:read"],
            resource="deployment-status",
            resource_environment="production",
            destination="local",
            input_source="ci-dispatch",
            input_trust="trusted",
            approval_required=False,
            approval_received=True,
            autonomy_mode="supervised",
        )
    if observer.last_error is not None:
        return {"statusCode": 502, "body": json.dumps({"telemetry": "failed", "error": str(observer.last_error)})}
    return {"statusCode": 200, "body": json.dumps({"telemetry": "accepted", "action": action})}

