"""All take a String as input
All return true is valid, false otherwise"""

import re


# has to be gmail
def isValidEmail(str):
    # ends with @gmail.com
    if "@gmail.com" == str[-10:]:
        str = str[0:len(str)-10]
    else:
        return False
    # 6-30 characters (not counting . or @gmail.com)
    length = 0
    for i in range(0, len(str)):
        if (not (str[i] == '.')):
            length = length + 1
    if (length > 30 or length < 6):
        return False

    # uses only letters numbers and periods
    regex = r".*[^a-zA-Z0-9\.].*"
    if (re.match(regex, str)):
        return False

    # first and last char must be letter or number
    if (str[0] == '.' or str[len(str)-1] == '.'):
        return False

    # no consecutive periods
    if (re.match(r".*\.\..*", str)):
        return False

    # 8 or more chars must contain a letter
    if (len(str) > 7):
        regex = r".*[a-zA-Z].*"
        if (not re.match(regex, str)):
            return False

    return True


# Assumptions for a valid name (subject to change):
#   Only letters, no more than three spaces,
#       0-2 non-consecutive or each hyphen, period, and single-quote
#   length has 1-50 letters
def isValidName(str):
    if (len(str) > 50 or len(str) < 1):
        return False

    regex = r".*[^a-zA-Z0-9\-\.' ].*"
    if (re.match(regex, str)):
        return False
    if (re.match(r".*\-\-.*", str)):
        return False
    if (re.match(r".*\.\..*", str)):
        return False
    if (re.match(r".*''.*", str)):
        return False
    if (re.match(r".*  .*", str)):
        return False
    if (re.match(r".*\-.*\-.*\-.*", str)):
        return False
    if (re.match(r".*\..*\..*\..*", str)):
        return False
    if (re.match(r".*'.*'.*'.*", str)):
        return False
    if (re.match(r".* .* .* .* .*", str)):
        return False

    return True


# may have a leading +
# may have one set of (), with 2-3 numbers inside
# may have to to 3 (non-consecutive) dashes, spaces or parenthesis
# all other characters must be numbers
# must end in a group of at least four numbers
# [5, 18] total characters
def isValidPhoneNumber(str):
    # [5, 18] total characters
    if (len(str) > 15 or len(str) < 5):
        return False

    # may have a leading + (removing if present)
    if (str[0] == '+'):
        str = str[1:len(str)]

    # may have one set of (), with 2-3 numbers inside
    hasParens = False
    regex = r".*\([0-9]{2,3}\).*"
    if (re.match(regex, str)):
        hasParens = True
        if (str.find('(') > 3):
            return False
    if (re.match(r".*\(.*", str) and not hasParens):
        return False
    if (re.match(r".*\).*", str) and not hasParens):
        return False
    if (re.match(r".*\(.*\(.*", str)):
        return False
    if (re.match(r".*\).*\).*", str)):
        return False

    # may have to to 3 (non-consecutive) dashes, spaces or parenthesis
    maxDashSpaceParen = 3
    if (hasParens):
        maxDashSpaceParen = 1
    for i in range(0, len(str)):
        if (str[i] == '-' or str[i] == ' '):
            maxDashSpaceParen = maxDashSpaceParen - 1
    if (maxDashSpaceParen < 0):
        return False
    if (re.match(r".*--.*", str) or re.match(r".*  .*", str)):
        return False

    # all other characters must be numbers
    regex = r".*[^0-9\(\)\- ].*"
    if (re.match(regex, str)):
        return False

    # must end in a group of at least four numbers
    regex = r".*[0-9]{4}$"
    if (not re.match(regex, str)):
        return False

    return True


# valid card number formats:
# #### #### #### ####
# ####-####-####-####
# ################
def isValidCardNumber(str):
    regex = r"[0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}"
    if (re.match(regex, str) and len(str) == 19):
        return True
    regex = r"[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}"
    if (re.match(regex, str) and len(str) == 19):
        return True
    regex = r"[0-9]{16}"
    if (re.match(regex, str) and len(str) == 16):
        return True
    return False


# 4 digits America Express, 3 otherwise
def isValidCVV(str):
    regex = r"[0-9]{3}"
    if (re.match(regex, str) and len(str) == 3):
        return True
    regex = r"[0-9]{4}"
    if (re.match(regex, str) and len(str) == 4):
        return True
    return False


# letters and numbers for now, can change latter
# length between 1 - 50, can also change later
def isValidUserID(str):
    if (len(str) > 50 or len(str) < 1):
        return False

    regex = r".*[^a-zA-Z0-9].*"
    if (re.match(regex, str)):
        return False
    return True


# security question answer
# letters, numbers, spaces (not consecutive)
# length between 1-50
def isValidAnswer(str):
    if (len(str) > 50 or len(str) < 1):
        return False

    regex = r".*[^a-zA-Z0-9 ].*"
    if (re.match(regex, str)):
        return False
    if (re.match(r".*  .*", str)):
        return False
    return True


# calender dates (MM/DD/YYYY)
def isValidDate(str):
    regex = r"[0-1][0-9]/[0-3][0-9]/[1-2][0-9]{3}"
    if (re.match(regex, str) and len(str) == 10):
        return True
    return False


# only numbers, possible leading $, and possible tailing .##
# setting a cap at $9999.99
def isValidDollarAmount(str):
    # remove leading $ if present
    if (str[0] == '$'):
        str = str[1:len(str)]

    # check for valid cents and remove if present
    regex = r"\.[0-9]{2}"
    if (re.match(regex, str[-3:])):
        str = str[0:len(str)-3]

    # check reasonable amount ( < 10000)
    if (len(str) > 4):
        return False

    regex = r".*[^0-9].*"
    if (re.match(regex, str)):
        return False
    return True


# Google authenticator code
# six digit number (I think)
# ### ### or ######
def isValidCode(str):
    regex = r"[0-9]{3} [0-9]{3}"
    if (re.match(regex, str) and len(str) == 7):
        return True
    regex = r"[0-9]{6}"
    if (re.match(regex, str) and len(str) == 6):
        return True
    return False
