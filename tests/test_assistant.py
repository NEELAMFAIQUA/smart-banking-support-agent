import unittest

from assistant import answer, retrieve


class AssistantTests(unittest.TestCase):
    def test_fraud_question_retrieves_safety_guidance(self):
        results = retrieve("I saw a suspicious transaction")
        self.assertEqual(results[0]["title"], "Suspected fraud")

    def test_unrelated_question_has_no_match(self):
        self.assertEqual(retrieve("pasta recipe"), [])
        self.assertIn("couldn't find", answer("pasta recipe")[0])

    def test_limit_must_be_positive(self):
        with self.assertRaises(ValueError):
            retrieve("checking", 0)


if __name__ == "__main__":
    unittest.main()
