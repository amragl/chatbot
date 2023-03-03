import pandas
from nltk.inference.resolution import Clause, BindingDict
from nltk.sem import Expression
from nltk.inference import ResolutionProver
from nltk.sem import Valuation, Model
read_expr = Expression.fromstring
#######################################################
#  Initialise Knowledgebase.
#######################################################
kb=[]
data = pandas.read_csv('info/kb.csv', header=None)
[kb.append(read_expr(row)) for row in data[0]]

def inference_kb():
    for item in Clause(kb):
        print(item)

def inference_check (exprsion):
    string_is = "is"
    string_server = "server"
    string_os = "OS"
    string_manage = "manage"
    string_use = "use"
    string_comma = ","

    def clean_subject (subject):
        if string_server in subject: subject = string_server
        elif string_os in subject: subject = string_os
        return subject

    if string_is in exprsion:
        object, subject =exprsion.split(' is ')
        subject = clean_subject(subject)
        object, subject = remove_spaces(object, subject)
        expr = read_expr(subject + '(' + object + ')')
    if string_manage in exprsion:
        object, subject = exprsion.split(' manage ')
        object, subject = remove_spaces(object, subject)
        expr = read_expr('manage (' + object + ',' + subject + ')')
    if string_use in exprsion:
        object, subject = exprsion.split(' use ')
        object, subject = remove_spaces(object, subject)
        expr = read_expr('use (' + object + ',' + subject + ')')
    elif string_comma in exprsion:
        object, subject = exprsion.split(',')
        object, subject = remove_spaces(object, subject)
        expr = read_expr(subject + '(' + object + ')')

    null_answer = ResolutionProver().prove(None, kb, verbose=False)

    #print("exprsion:", exprsion, " expr: ", expr, "subject: ", subject, " object: ", object)
    print("Joe: Wait a minute, I am thinking about it....")
    if null_answer:  # True&True -> Contradiction
        print('Joe: A rule within KB contradict each other, please review KB')
    else:
        org_answer = ResolutionProver().prove(expr, kb, verbose=False)
        neg_answer = ResolutionProver().prove(expr.negate(), kb, verbose=False)
        #print("original answer: ", org_answer, " negated_answer: ", neg_answer)
        if org_answer and not neg_answer:  # True&False -> org_answer is true
            print("Joe: You are right")
        elif not org_answer and neg_answer:  # False&True -> neg_answer is false
            print("Joe: You are wrong")
        elif not org_answer and not neg_answer:  # False&False -> Not rule found
            user_answer = input(
                "Joe: Sorry, I dont know, should I add this to my KB? y or n: ")
            if user_answer == 'y':
                kb.append(expr)
                print("Joe: OK, I'll remember that ", exprsion, expr)
            elif user_answer == 'n':
                print("Joe: OK, I'll forget about it.")
            else:
                print("Joe: You have to choose Y or N")
        else:  # True&True -> Contradiction
            print("Joe: Not sure how you got here, but there is a contradiction.")


def remove_spaces(object, subject):
    object = object.replace(" ", "_")
    subject = subject.replace(" ", "_")
    return object, subject




