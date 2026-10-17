import unittest

from assistant import answer, retrieve, route_to_specialist


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

    def test_support_routes_to_specialist(self):
        self.assertEqual(
            route_to_specialist("I need help with a suspicious card transaction")["name"],
            "Fraud safety",
        )

    def test_credentials_are_refused_without_faq_answer(self):
        response, references = answer("Here is my password and PIN")
        self.assertIn("never share", response)
        self.assertEqual(references, [])


if __name__ == "__main__":
    unittest.main()
