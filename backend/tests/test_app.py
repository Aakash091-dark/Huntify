import unittest

from fastapi.testclient import TestClient

from app.autonomous.agent import run_autonomous_job_hunt
from app.main import app


class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_root_endpoint(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_health_check(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_resume_summary(self) -> None:
        response = self.client.get("/api/v1/resume/summary")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("summary", payload)

    def test_autonomous_job_hunt(self) -> None:
        result = run_autonomous_job_hunt()
        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(result["jobs_evaluated"], 0)
        self.assertGreaterEqual(result["shortlisted_jobs"], 0)

    def test_autonomous_route(self) -> None:
        response = self.client.post("/api/v1/jobs/autonomous-run")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_start_applying_uses_backend_pipeline(self) -> None:
        response = self.client.post("/api/v1/applications/start")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "completed")
        self.assertEqual(payload["applications_created"], 0)
        self.assertEqual(payload["jobs_evaluated"], 0)
        self.assertIn("No verifiable job listings", payload["message"])


if __name__ == "__main__":
    unittest.main()
