import unittest, time

from src.magic_eight.magic_eight import get_answers, get_questions, ask_question, shake_ball, questions, answers

class TestMagicEight(unittest.TestCase):
## testing get_answers
    def test_get_answers_just_language(self):
        """Test the get_answers function with just language input"""
        expected = answers["en"]
        result = get_answers("en")
        self.assertEqual(result, expected)

    def test_get_answers_language_and_valid_count(self):
        """Test the get_answers function with language and count input"""
        expected = [
            "¡Sí, definitivamente!",
            "Es cierto.",
            "Sin duda.",
        ]
        result = get_answers("es", 3)
        self.assertEqual(result, expected)

    def test_get_answers_language_and_invalid_count(self):
        """Test the get_answers function with language and count input beyond size of answers[]"""
        expected = answers["fr"]
        result = get_answers("fr",-3)
        self.assertEqual(result, expected)
        
## testing get_questions
    def test_get_questions_just_language(self):
        """Test the get_questions function with just language input"""
        expected = questions["en"]
        result = get_questions("en")
        self.assertEqual(result, expected)

    def test_get_questions_language_and_valid_count(self):
        """Test the get_questions function with language and count input"""
        expected = [
            "Vais-je passer une bonne journée aujourd'hui?",
        ]
        result = get_questions("fr", 1)
        self.assertEqual(result, expected)

    def test_get_questions_language_and_invalid_count(self):
        """Test the get_questions function with language and count input beyond size of questions[]"""
        expected = questions["es"]
        result = get_questions("es",100)
        self.assertEqual(result, expected)

## testing ask_question
    def test_ask_question_specific(self):
        """Test ask_question with a specific question"""
        question, answer = ask_question("en", "Will I pass this class")
        expected_question = "Will I pass this class"
        expected = answers["en"]
        self.assertEqual(question, expected_question)
        self.assertIn(answer, expected)

    def test_ask_question_random(self):
        """Test ask_question with random question generation"""
        question, answer = ask_question("es")
        expected_questions = questions["es"]
        expected_answer = answers["es"]
        self.assertIn(question, expected_questions)
        self.assertIn(answer, expected_answer)

    def test_ask_question_invalid_language(self):
        """Test ask_question with an invalid language"""
        result = ask_question("frr") 
        self.assertEqual(result, [])

## testing shake_ball 
    def test_shake_ball_no_delay(self):
        """Test shake_ball with a valid language and no delay"""
        result = shake_ball("fr", 0)
        expected = answers["fr"]
        self.assertIn(result, expected)

    def test_shake_ball_invalid_language(self):
        """Test shake_ball with an invalid language"""
        result = shake_ball("it", 0)
        self.assertEqual(result, "invalid")

    def test_shake_ball_with_delay(self):
        """Test shake_ball with a valid language and 1 sec shake time"""
        expected = answers["es"]
        start_time = time.time()
        result = shake_ball("es", 2)
        delay_time = time.time() - start_time
        self.assertIn(result, expected)
        # make sure the delay time calculated is less not more than .1 seconds than expected to account for overhead
        self.assertLessEqual(delay_time - 2, .1)

    def test_shake_ball_non_integer_shake_time(self):
        """Test shake_ball with a non-integer shake time (i.e. a float)"""
        expected = answers["fr"]
        start_time = time.time()
        result = shake_ball("fr", 2.1) 
        delay_time = time.time() - start_time
        self.assertIn(result, expected)
        # make sure the delay time calculated is less not more than .1 seconds than expected to account for overhead
        self.assertLessEqual(delay_time - 2.1, .1)

if __name__ == "__main__":
    unittest.main()