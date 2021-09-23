from datetime import datetime


def school_abbreviation(name):
    """
    Creates the abbreviation used for the school based on the long name. Removes intermediary words.
    :param name: (String) Long name for the school
    :return: (String) abbreviated name for the school
    """
    name = name.split()
    abbv = ""
    no_lst = ["of", "the", "in", "at"]
    for no in no_lst:
        for item in name:
            if item.lower() == no:
                name.remove(item)
    for item in name:
        abbv += item[0].lower()
    return abbv


def basic_info():
    """
    Prompts the user for basic info and passes it back to the main function.
    :return: (Tuple) basic info for the school and sport and sex of the athletes.
    """
    school = input("School long name: ")
    school = school.split(" ")
    for item in school:
        item[0] = item[0].upper()
    school = " ".join(school)
    while True:
        sex = input("sex: ").lower()
        if sex == "m" or sex == "f":
            break
        else:
            print("incorrect input, please try again.")
    sport_abbv = input("sport abbreviation: ")
    return school_abbreviation(school) + sex + sport_abbv, school


def position(lst):
    """
    Tries to input a position fo the player. If none given, returns nothing.
    :param lst: (List) Input given by the user about a certain player.
    :return: (None or String) the player's position, if applicable.
    """
    return f'{lst[3]}, ' if len(lst)==4 else ''


def coachformat(st):
    """
    Formats a coach's title properly and returns it.
    :param st: (String) Coach's title, any formatting.
    :return: (String) Properly formatted Coach's title (capitalized first letters, lowercase the rest).
    """
    return ' '.join([word.lower() for word in st.split(' ')])


def player_input_line(call, school, f:str):
    """
    Returns a properly formatted line about a player.
    :param call: (String) The beginning of the line, includes the gender, sport, and school abbreviation.
    :param school: (String) The longform name of the school.
    :param f: (String) The input line from the user.
    :return: (String) A properly formatted line with all necessary information about a player.
    """

    # Original version of this code
    # f = f.split("\t")
    # return f"{call}{f[2]}\t{school}'s {position(f)} {f[0]} {f[1]}, #{f[2]},\t{f[0]} {f[1]}, #{f[2]},\t{f[1]}\n"

    first, last, number, pos = (f + ['']) if len(f:=f.split("\t")) == 3 else (f)
    # padding with empty string if length is less than 4
    # if this doesn't work, go yell at Jonah (@TG-Techie)
    return f"""{call}{number}\t{school}'s {pos}, {first} {last}, #{number},\t{first} {last}, #{number},\t{last}\n"""


def coach_input_line(call, school, f):
    """
    Returns a properly formatted line about a coach.
    :param call: (String) The beginning of the line, includes the gender, sport, and school abbreviation.
    :param school:(String) The longform name of the school.
    :param f: (String) The input line from the user.
    :return: (String) A properly formatted line with all necessary information about a coach.
    """
    f = f.split("\t")
    newCall = f[2].split(" ")
    for item in newCall:
        call += item[0].lower()
        print(call)
    print(f[2])
    return f"{call}\t{school}'s {coachformat(f[2])}, {f[0]} {f[1]},\t{f[0]} {f[1]},\t{f[1]}\n"


def main():
    """
    Runs the program to create properly formatted player and coach files.
    :return: None.
    """
    ret = basic_info()
    call = ret[0]
    school = ret[1]
    roster = list()
    print("the word tab needs to be replaced by a press of the tab key when it is typed in. ")
    print("Line input is FirstName tab Lastname tab Number " + \
          "(tab Position, if they have a position like goalie or captain).")
    print("To add coaches, type 'coach'. To finish and save the file, type 'exit'.")
    print("The file will be saved to the folder you ran this application from.")
    while True:
        inpt = input(">")
        if inpt == "exit":
            print("Saving and exiting...")
            try:
                with open(f"Out/{call.upper()}{year:=datetime.now().year}-{year+1}.txt", "x+") as f:
                    for line in roster:
                        f.write(line)
                exit()
            except IOError:
                print("File already exists. Copy this output to a new file if you wish to save it.")
                for line in roster:
                    print(line)
                exit()
        elif inpt == "coach":
            print("Line input is FirstName tab LastName tab Head Coach/Assistant Coach/Associate Coach/etc.")
            inpt = input(">")
            try:
                roster += coach_input_line(call, school, inpt)
            except IndexError:
                continue
        else:
            if inpt == '\n':
                continue
            try:
                assert (ln:=len(inpt.split("\t"))) in (3, 4), f'Expected a list of len 3 or 4, got len {ln}'
                roster += player_input_line(call, school, inpt)
            except IndexError:
                print("Incorrect command. please try again.")
                continue
            except AssertionError as e:
                print(e)
                continue

if __name__ == "__main__":
    main()
