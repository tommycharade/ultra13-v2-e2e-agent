import json
import os
import unittest
from unittest.mock import patch

import handler


class AgentDeploymentTest(unittest.TestCase):
    def test_deployment_is_healthy_without_a_runtime_secret(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            response = handler.lambda_handler({"action": "control"}, object())
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"])["telemetry"], "not-configured")


if __name__ == "__main__":
    unittest.main()

