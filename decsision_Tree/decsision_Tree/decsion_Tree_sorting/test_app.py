import unittest
import json
from app import app  # Ensure app is importable from app.py

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client
        app.testing = True
        self.client = app.test_client()

    def test_index_endpoint(self):
        # Test the root endpoint for welcome message
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("message", data)
        self.assertIn("Decision Tree Sorting Visualizer API", data["message"])

    def test_run_sort_valid(self):
        # Test the /api/run_sort endpoint with a valid request
        payload = {
            "algorithm": "bubble_sort",
            "list_size": 4
        }
        response = self.client.post(
            '/api/run_sort',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Check that response contains required keys
        self.assertEqual(data.get("algorithm"), "bubble_sort")
        self.assertIn("original_array", data)
        self.assertIn("sorted_array", data)
        self.assertIn("comparisons", data)
        self.assertIn("operations_log", data)
        self.assertIn("decision_tree", data)

    def test_run_sort_invalid_algorithm(self):
        # Test /api/run_sort with an unsupported algorithm
        payload = {
            "algorithm": "quick_sort",  # not implemented in our current version
            "list_size": 4
        }
        response = self.client.post(
            '/api/run_sort',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_analysis_endpoint(self):
        # Test the /api/analysis endpoint
        response = self.client.get('/api/analysis')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Check for expected keys in analysis results
        self.assertTrue("analysis_results" in data or "message" in data)

if __name__ == '__main__':
    unittest.main()
