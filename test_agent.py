import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

import handler


class AgentDeploymentTest(unittest.TestCase):
    def test_deployment_is_healthy_without_a_runtime_secret(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            response = handler.lambda_handler({"action": "control"}, object())
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"])["telemetry"], "not-configured")

    def test_repeat_delivery_reuses_the_immutable_revision(self) -> None:
        workflow = Path(".github/workflows/ultra13-delivery.yml").read_text(encoding="utf-8")
        self.assertIn('--image-ids "imageTag=${GITHUB_SHA}"', workflow)
        self.assertIn('if [ "${current_image}" != "${image}" ]', workflow)
        self.assertIn('Lambda already runs the immutable image for ${GITHUB_SHA}.', workflow)


if __name__ == "__main__":
    unittest.main()
