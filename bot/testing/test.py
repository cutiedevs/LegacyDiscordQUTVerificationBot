from random import *
import ifb102_quiz_1 as q 

questions = []

topic_1_chosen = sample(list(q.topic_1), 5)
topic_2_chosen = sample(list(q.topic_2), 5)
topic_3_chosen = sample(list(q.topic_3), 5)
topic_4_chosen = sample(list(q.topic_4), 5)

questions.append(topic_1_chosen)
questions.append(topic_2_chosen)
questions.append(topic_3_chosen)
questions.append(topic_4_chosen)

score = 0
sections = 0

def section_check(sect):
    global score
    global sections
    match sect:
        case 0:
            for question in range(5):
                attempts = 3
                while attempts > 0:
                    print(q.topic_1[questions[0][question]]['question'])
                    answer = str(input("Enter Answer: "))
                    print(q.topic_1[questions[0][question]]['answer'])
                    if q.topic_1[questions[0][question]]['answer'] == answer:
                        score += 1
                        print(f"Correct Answer! \nYour score is {score + 1}")
                        attempts = 0
                    else:
                        attempts -= 1
                        print(f"Wrong Answer :( \nYou have {attempts - 1} left! \n Try Again!")
            sections += 1
        case 1:
            for question in range(5):
                attempts = 3
                print(question)
                print(questions[1][question])
                while attempts > 0:
                    print(q.topic_2[questions[1][question]]['question'])
                    answer = str(input("Enter Answer: "))
                    print(q.topic_2[questions[1][question]]['answer'])
                    if q.topic_2[questions[1][question]]['answer'] == answer:
                        score += 1
                        print(f"Correct Answer! \nYour score is {score + 1}")
                        attempts = 0
                    else:
                        attempts -= 1
                        print(f"Wrong Answer :( \nYou have {attempts - 1} left! \n Try Again!")
            sections += 1
        case 2:
            for question in range(5):
                attempts = 3
                while attempts > 0:
                    print(q.topic_3[questions[2][question]]['question'])
                    answer = str(input("Enter Answer: "))
                    print(q.topic_3[questions[2][question]]['answer'])
                    if q.topic_3[questions[2][question]]['answer'] == answer:
                        score += 1
                        print(f"Correct Answer! \nYour score is {score + 1}")
                        attempts = 0
                    else:
                        attempts -= 1
                        print(f"Wrong Answer :( \nYou have {attempts - 1} left! \n Try Again!")
            sections += 1
        case 3:
            for question in range(5):
                attempts = 3
                while attempts > 0:
                    print(q.topic_4[questions[3][question]]['question'])
                    answer = str(input("Enter Answer: "))
                    print(q.topic_4[questions[3][question]]['answer'])
                    if q.topic_4[questions[3][question]]['answer'] == answer:
                        score += 1
                        print(f"Correct Answer! \nYour score is {score + 1}")
                        attempts = 0
                    else:
                        attempts -= 1
                        print(f"Wrong Answer :( \nYou have {attempts - 1} left! \n Try Again!")
            sections += 1

while sections < 5:
    print(sections)
    print(questions)
    section_check(sections)