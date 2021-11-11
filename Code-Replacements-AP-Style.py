from datetime import datetime
from sys import platform, version_info, hexversion, version
import os

PRINT = True
ACS = 0 #assistant coaches
HCS = 0 #head coaches
CS = 0  #coaches
AT = 0  #athletic trainers
AS = 0  #assistants

def dprint(arg):
    global PRINT
    if PRINT == True:
        print(arg)
    else:
        pass

def platform_check():
    if hexversion >= 3070000:
        if platform.lower() == "linux":
            #file path isntructions for linux
            dprint("Linux")
            pass
        elif platform.lower() == "darwin":
            dprint("MacOS")
            pass
        elif platform.lower() == "win32":
            #file platform instructions for windows
            dprint("Windows")
            pass
        else:
            print(f"Platform not supported. Please try again on Windows, MacOS, or Linux.")
            raise OSError("Unsupported platform")
    else:
        print(f"Python version too old. Python >3.7 required, found Python {version}.")
        raise OSError("Unsupported platform")



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

def sport():
    sports={"hockey":"hky", "basketball":"bb", "soccer":"soc", "volleyball":"vball", "lacrosse":"lax", "baseball":"bsb", "softball":"sb"}
    spt = sports.get(input("sport: ").lower())
    if spt == "vball" or spt == "sb" or spt == "bsb":
        return spt, 1
    else:
        return spt, 0



def basic_info():
    """
    Prompts the user for basic info and passes it back to the main function.
    :return: (Tuple) basic info for the school and sport and sex of the athletes.
    """
    school = input("School long name: ").title().split(" ") # make each word start w/ caps letter
    # school = school.split(" ")
    # for item in school:
    #     item[0] = item[0].upper()
    # school = " ".join(school)
    no_lst = ["Of", "The", "In", "At", "For"]
    for i in range(len(school)):
        name = school[i]
        name = name.capitalize()
        dprint(name)
        for item in no_lst:
            if name == item:
                dprint("test == true")
                school[i] = name.lower()
    sch = " ".join(school)
    dprint(sch)
    while True:
        sex = input("sex (m/w): ").lower()
        if sex == "m" or sex == "w":
            break
        else:
            print(f"Expected <m> or <f>, got <{sex}>")
    while True:
        spt = sport()
        if spt is not None:
            break
    dprint(school_abbreviation(sch))
    if school_abbreviation(sch) == "rit":
        if spt[1] == 1:
            return spt[0], sch
        else:
            return sex + spt[0], sch
    if spt[1] == 1:
        return school_abbreviation(sch) + spt[0], sch
    else:
        return school_abbreviation(sch) + sex + spt[0], sch


def position(lst):
    """
    Properly formats player position.
    :param lst: player's position, given by the user.
    :return: (None or String) the player's position, if applicable.
    """
    return f'{lst}, '


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
    # print(g:=f.split())
    # print(len(g))
    first, last, number, pos = (f + ['']) if len(f:=f.split("\t")) == 3 else (f[:3] + [position(f[3])])
    # padding with empty string if length is less than 4
    # if this doesn't work, go yell at Jonah (@TG-Techie)
    first = first.capitalize()
    last = last.capitalize()
    return f"""{call}{number}\t{school}'s {pos}{first} {last} ({number}),\t{first} {last} ({number}),\t{last}\n"""


def coach_input_line(call, school, f):
    """
    Returns a properly formatted line about a coach.
    :param call: (String) The beginning of the line, includes the gender, sport, and school abbreviation.
    :param school:(String) The longform name of the school.
    :param f: (String) The input line from the user.
    :return: (String) A properly formatted line with all necessary information about a coach.
    """
    f=f.split("\t")
    print(f"{f[0]}, {f[1]}, {coachformat(f[2])}, {len((f[0], f[1], coachformat(f[2])))}")
    first, last, pos = (f[0].capitalize(), f[1].capitalize(), coachformat(f[2]))
    newCall = f[2].split(" ")
    for item in newCall:
        call += item[0].lower()
    return f"{call}\t{school}'s {pos}, {first} {last},\t{first} {last},\t{last}\n"

def filename(*, call) -> str:
    return f"Out/{call.upper()}{(year:=datetime.now().year)}-{year+1}.txt"

def main():
    '''
    Runs the program to create properly formatted player and coach files.
    :return: None.
    '''

    platform_check()

    call, school = basic_info()
    roster = list()
    print("Entries are tab-spaced. Use the tab key between entries on a line. ")
    print("Line input is <FirstName> <Lastname> <Number> " + \
          "optional <Position> (use <Position> for goaltender, captain, etc).")
    print("To add coaches, type 'coach'. To finish and save the file, type 'exit'.")
    print(f"The file will be saved to .{filename(call=call)}.")
    while True:
        inpt = input(">")
        if inpt == "exit":
            print("Saving and exiting...")
            try:
                with open(filename(call=call), "x+") as f:
                    for line in roster:
                        f.write(line)
                return # do not call exit here
            except IOError:
                print("File already exists. Copy this output to a new file if you wish to save it.")
                if len(roster) == 1:
                    print(roster[0])
                else:
                    for line in roster:
                        print(line)
                return # do not call exit here
        elif inpt == "coach":
            print("Entries are tab spaced. Use the tab key between entries on a line.")
            print("Input format is <FirstName> <LastName> <Coach Position> (<Coach Position> is head coach, assistant coach, etc.).")
            inpt = input(">")
            try:
                assert (ln:=len(inpt.split("\t"))) == 3, f'Expected a list of len 3, got len {ln}'
                roster += coach_input_line(call, school, inpt)
            except IndexError:
                continue
            except AssertionError as e:
                print(e)
                continue
        else:
            if inpt == '\n':
                continue
            try:
                assert (ln:=len(inpt.split("\t"))) in (3, 4), f'Expected a list of len 3 or 4, got len {ln}'
                roster += player_input_line(call, school, inpt)
            except IndexError:
                continue
            except AssertionError as e:
                print(e)
                continue

if __name__ == "__main__":
    main()
