import random

def createcaptcha():
    a = random.randint(0,5)
    b = random.randint(0,5)
    c = random.randint(0,5)
    return [f"({a}+{b})*{c}", (a+b)*c]


def is_name_ok(name):
    #Проверить что разделено пробелом
    #Начинаетс с больших букв
    #Нет цифр
    lst = name.split()
    if len(lst) != 2:
        return False
    
    if not(lst[0][0].isupper()) or not(lst[1][0].isupper()):
        return False

    if not(lst[0].isalpha()) or not(lst[1].isalpha()):
        return False

    return True

def is_number_ok(number):
    if len(number) != 10:
        return False

    if not(number.isdigit()):
        return False

    return True
    

def is_course_ok(current, all_courses):
    print(current)
    for key in all_courses:
        if current == all_courses[key]:
            return True
    return False