# Ultra13 V2 end-to-end agent

This is a deliberately small OpenAI Agents SDK 0.19.4 application used to prove
the complete Ultra13 V2 lifecycle against a real repository and AWS deployment.

The GitHub Actions workflow tests the application, inventories and scans the
immutable deployment unit, validates its release policy, builds a Lambda
container, deploys it through GitHub OIDC, emits deployment-bound runtime
evidence, and publishes the revision decision plus SARIF into Ultra13 V2.

The application is content-free and does not call a model provider. Its normal
runtime path exposes only `read_status`. The `drift` invocation is an explicit
QA-only signal used to verify that an unapproved privileged tool call blocks the
current release decision.

