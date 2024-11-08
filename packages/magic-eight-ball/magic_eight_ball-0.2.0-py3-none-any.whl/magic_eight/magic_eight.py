from .answers import answers
from .questions import questions
from .shakes import shakes
import random
import time

# return list of sample questions, either to the specific count or all available questions
def get_questions(language, count = 0):
    if language not in questions.keys():
        # return error message that specific language is not available
        return []
    
    sample_questions = []
    # return array with all sample questions
    if count == 0 or count > len(questions[language]):
        for question in questions[language]:
            sample_questions.append(question)
            # print(question)
    # return array with count sample questions
    else:
        for i in range(count):
            sample_questions.append(questions[language][i])
            # print(questions[language][i])
    return sample_questions
# ask a question and receive a response
def ask_question(language, question=""):
    if language not in questions.keys():
        # return error message that specific language is not available
        return []
    
    if question == "":
        # generate a random question
        index = random.randint(0, len(questions[language])-1)
        question = questions[language][index]
        # print("Random question:",question)
    
    index = random.randint(0, len(answers[language])-1)
    answer = answers[language][index]
    return (question, answer)
    # shake_ball(language)
    # print(answer)

# shake the ball to get another answer to the previous question, specify language and optionally the amount of time to shake
def shake_ball(language, shake_time=10):
    if language not in questions.keys():
        # return error message that specific language is not available
        return "invalid"
    time.sleep(shake_time)
    index = random.randint(0, len(answers[language])-1)
    answer = answers[language][index]
    return answer

# similar to get_questions, return list of all sample answers or to specified count
def get_answers(language, count=0):
    if language not in questions.keys():
        # return error message that specific language is not available
        return []
    
    # handle invalid count
    if count < 0:
        count = 0

    sample_answers = []
    if count == 0 or count > len(answers[language]):
        for answer in answers[language]:
            sample_answers.append(answer)
            # print(answer)
    else:
        for i in range(count):
            sample_answers.append(answers[language][i])
            # print(answers[language][i])
    return sample_answers
