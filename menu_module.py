import config

def run_menu():
    print("--------------------------------------------------")
    print("Welcome to Reddit image extractor version 1.2.3")
    print("--------------------------------------------------" + "\n")
    prompt_subreddits()
    prompt_sort_type()
    prompt_down_limit()

def prompt_subreddits():
    while True:
        if not config.subreddit:
            edit_subreddits()
            break
        subreddits = get_subreddits()
        print("You have set: " + subreddits + "As your default, do you wish to change it? [y/N]" + "\n")
        change_subreddit_input = input().lower()
        print("")
        if change_subreddit_input == "" or change_subreddit_input == "n":
            break
        elif change_subreddit_input == "y":
            edit_subreddits()
            break

def get_subreddits():
    subreddits = ""
    for subreddit in config.subreddit:
        subreddits = subreddits + subreddit + " "
    return subreddits

def edit_subreddits():
    while True:
        if config.subreddit:
            print("You have set: " + get_subreddits() + "what do you wish to do?:" + "\n")
        else:
            print("You have not set any subreddits")
        print("1 Add subreddit")
        print("2 Clear")
        print("3 Done" + "\n")
        change_subreddit_choice = input()
        print("")
        if change_subreddit_choice == "1":
            new_subreddit_input = input("Enter subreddit: ")
            print("")
            config.subreddit.append(new_subreddit_input)
        elif change_subreddit_choice == "2":
            config.subreddit = []
        elif change_subreddit_choice == "3":
            if config.subreddit:
                break

def prompt_sort_type():
    while True:
        sort_type = config.sort_type
        if sort_type == "":
            sort_type = "Hot"
        print("You have set: " + sort_type + " as your default, do you wish to change it? [y/N]" + "\n")
        change_subreddit_input = input().lower()
        print("")
        if change_subreddit_input == "" or change_subreddit_input == "n":
            break
        elif change_subreddit_input == "y":
            edit_sort_type()
            break

def edit_sort_type():
    while True:
        print("What do you wish to choose?" + "\n")
        print("1 Hot")
        print("2 New")
        print("3 Rising")
        print("4 Controversial")
        print("5 Top")
        print("6 Gilded" + "\n")
        type_choice = input()
        print("")
        if type_choice == "1":
            break
        elif type_choice == "2":
            config.sort_type = "new"
            break
        elif type_choice == "3":
            config.sort_type = "rising"
            break
        elif type_choice == "4":
            config.sort_type = "controversial"
            prompt_sort_arg("controversial")
            break
        elif type_choice == "5":
            config.sort_type = "top"
            prompt_sort_arg("top")
            break
        elif type_choice == "6":
            config.sort_type = "gilded"
            break

def prompt_sort_arg(arg_type):
    while True:
        sort_arg = config.sort_arg
        if sort_arg == "":
            sort_arg = "Past 24 hours"
        print("You have set: " + sort_arg + " as your default, do you wish to change it? [y/N]" + "\n")
        change_subreddit_input = input().lower()
        print("")
        if change_subreddit_input == "" or change_subreddit_input == "n":
            break
        elif change_subreddit_input == "y":
            edit_sort_arg(arg_type)
            break

def edit_sort_arg(arg_type):
    while True:
        print("What time frame do you wish to choose?" + "\n")
        print("1 Past hour")
        print("2 Past 24 hours")
        print("3 Past week")
        print("4 Past month")
        print("5 Past year")
        print("6 All time" + "\n")
        type_choice = input()
        print("")
        if type_choice == "1":
            config.sort_arg = "?sort=" + arg_type + "&t=hour"
            break
        elif type_choice == "2":
            break
        elif type_choice == "3":
            config.sort_arg = "?sort=" + arg_type + "&t=week"
            break
        elif type_choice == "4":
            config.sort_arg = "?sort=" + arg_type + "&t=month"
            break
        elif type_choice == "5":
            config.sort_arg = "?sort=" + arg_type + "&t=year"
            break
        elif type_choice == "6":
            config.sort_arg = "?sort=" + arg_type + "&t=all"
            break

def prompt_down_limit():
    while True:
        if config.down_limit <= 0:
            edit_down_limit()
            break
        print("You have set: " + str(config.down_limit) + " As your default, do you wish to change it? [y/N]" + "\n")
        change_down_limit_input = input().lower()
        print("")
        if change_down_limit_input == "" or change_down_limit_input == "n":
            break
        elif change_down_limit_input == "y":
            edit_down_limit()
            break

def edit_down_limit():
    while True:
        user_input = input("Enter number of pictures you wish to download: ")
        print("")
        try:
            val = int(user_input)
            config.down_limit = val
            break
        except ValueError:
            print("That's not an int!" + "\n")
