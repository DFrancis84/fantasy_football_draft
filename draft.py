"""Fantasy Football Draft Tool"""
import csv
import sqlite3
import time
import pyfiglet
from prettytable import PrettyTable

def print_banner():
    """Print Title Banner"""
    ascii_banner = pyfiglet.figlet_format('DRAFT.PY')
    print(ascii_banner)

def enter_league_definitions():
    """Enter league parameters"""
    league_name = input('Please enter league name: ')
    number_teams = input('How many teams are drafting? ')
    number_rounds = input('How many rounds in this draft? ')
    draft_type = input('Draft Type: Snake or Custom? ').upper()
    number_picks = int(number_teams)*int(number_rounds)
    print("This draft will contain {} picks.".format(number_picks))
    return league_name, number_teams, number_rounds, draft_type, number_picks

def create_manager_list(number_teams):
    """Create List of all Managers Drafting"""
    managers = []
    i = 1
    # Adds a team to the list based on number_teams input
    for _ in range(int(number_teams)):
        manager = input('Enter name for Team #{}: '.format(i)).capitalize()
        managers.append(manager)
        i += 1
    return managers

def create_managers_list_for_snake_draft(number_teams, number_rounds):
    """Creates list of managers for snake draft format"""
    managers = []
    i = 1
    for _ in range(int(number_teams)):
        manager = input('Enter name for Team #{}: '.format(i)).capitalize()
        managers.append(manager)
        i += 1
    new_managers = managers.copy()
    for i in range(number_rounds+1):
        if i == 0:
            i += 1
            continue
        if i == 1:
            i += 1
            continue
        if i%2 == 0:
            new_managers.extend(managers[::-1])
            i += 1
            continue
        if i%2 == 1:
            new_managers.extend(managers)
            i += 1
            continue
        if i == number_rounds:
            break
    return new_managers

def create_board(league_name):
    """Create DraftBoard"""
    print("Creating DraftBoard for", league_name)
    conn = sqlite3.connect('{}.db'.format(league_name))
    cur = conn.cursor()
    # Create table - DraftBoard
    cur.execute('''
CREATE TABLE IF NOT EXISTS {}(
pick INTEGER PRIMARY KEY AUTOINCREMENT,
manager TEXT,
player_first_name TEXT,
player_last_name TEXT,
position TEXT,
nfl_team TEXT)
    '''.format(league_name))
    conn.commit()
    conn.close()

def insert_draft_pick(league_name, managers):
    """Insert Draft Picks"""
    conn = sqlite3.connect('{}.db'.format(league_name))
    cur = conn.cursor()
    # Allow input for draft picks
    manager_name = select_manager(managers)
    player_first_name = input('Please enter Players First Name: ').capitalize()
    player_last_name = input('Please enter Players Last Name: ').capitalize()
    player_position = input('Please enter Players Position: ').upper()
    nfl_team = input('Please enter Players Team: ').upper()
    # Enter draft picks to db
    cur.execute('''
INSERT INTO {}(manager, player_first_name, player_last_name, position, nfl_team) VALUES(?,?,?,?,?)
    '''.format(league_name),
                (manager_name, player_first_name, player_last_name, player_position, nfl_team))
    conn.commit()
    conn.close()

def insert_draft_pick_for_snake_draft(league_name, manager):
    """Insert Draft Picks"""
    conn = sqlite3.connect('{}.db'.format(league_name))
    cur = conn.cursor()
    # Allow input for draft picks
    print("{} is on the clock...".format(manager))
    player_first_name = input('Please enter Players First Name: ').capitalize()
    player_last_name = input('Please enter Players Last Name: ').capitalize()
    player_position = input('Please enter Players Position: ').upper()
    nfl_team = input('Please enter Players Team: ').upper()
    # Enter draft picks to db
    cur.execute('''
INSERT INTO {}(manager, player_first_name, player_last_name, position, nfl_team) VALUES(?,?,?,?,?)
    '''.format(league_name),
                (manager, player_first_name, player_last_name, player_position, nfl_team))
    conn.commit()
    conn.close()

def select_manager(managers):
    """Select Manager"""
    _m_ = 1
    # Iterate through list of teams and assign a number
    for _manager_ in managers:
        print("{}. {}".format(_m_, _manager_))
        _m_ += 1
    name = input("Select Manager: ")
    # Takes the users input, and subtracts one since lists start at 0. Converts input into name
    name = int(name) - 1
    return managers[name]

def create_table_per_round(league_name, number_teams):
    """Generate Table"""
    conn = sqlite3.connect('{}.db'.format(league_name))
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(league_name))
    rows = cur.fetchall()
    table = PrettyTable(['PickNumber', 'ManagerName', 'PlayerFirstName', 'PlayerLastName', 'PlayerPosition', 'NFLTeam'])
    table.align["ManagerName"] = "l"
    table.align["PlayerFirstName"] = "l"
    table.align["PlayerLastName"] = "l"
    table.align["PlayerPosition"] = "l"
    table.align["NFLTeam"] = "l"
    # Iterate through all the rows and add them to prettytable
    for row in rows:
        table.add_row([row[0], row[1], row[2], row[3], row[4], row[5]])
    # Notify that round has been completed
    print("Round {} Complete!".format(len(rows)/int(number_teams)))
    # Prints table at end of each round
    print(table[-int(number_teams):])

def custom_draft(number_picks, number_teams, league_name, managers):
    """The Entire Draft Process"""
    _r_ = 0
    for _ in range(number_picks):
        insert_draft_pick(league_name, managers)
        _r_ += 1
        if _r_%int(number_teams) == 0:
            create_table_per_round(league_name, number_teams)
        time.sleep(1)

def snake_draft(number_picks, number_teams, league_name, managers):
    """The Entire Draft Process"""
    _p_ = 0
    i = 0
    for _ in range(number_picks):
        insert_draft_pick_for_snake_draft(league_name, managers[i])
        _p_ += 1
        i += 1
        if _p_%int(number_teams) == 0:
            create_table_per_round(league_name, number_teams)
        time.sleep(1)

def show_draft_results(league_name):
    """Display Draft Results"""
    conn = sqlite3.connect('{}.db'.format(league_name))
    cur = conn.cursor()
    # Select everything from database for table output
    cur.execute("SELECT * FROM {}".format(league_name))
    rows = cur.fetchall()
    # Create and Print display table
    table = PrettyTable(['PickNumber', 'ManagerName', 'PlayerFirstName', 'PlayerLastName', 'PlayerPosition', 'NFLTeam'])
    table.align["ManagerName"] = "l"
    table.align["PlayerFirstName"] = "l"
    table.align["PlayerLastName"] = "l"
    table.align["PlayerPosition"] = "l"
    table.align["NFLTeam"] = "l"
    # Iterate through all the rows and add them to prettytable
    for row in rows:
        table.add_row([row[0], row[1], row[2], row[3], row[4], row[5]])
    # Prints final draft results
    print(table)

def create_csv_from_draft_database(league_name):
    """Convert Database to CSV file"""
    conn = sqlite3.connect('{}.db'.format(league_name))
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(league_name))
    result = cur.fetchall()
    headers = ["pickNumber", "managerName", "playerFirstName", "playerLastName", "playerPosition", "teamAbbreviation"]
    with open("{}.csv".format(league_name), "w") as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(headers)
        for _r_ in result:
            filewriter.writerow(_r_)

def start_draft():
    """Starts the Draft"""
    # Print program banner
    print_banner()
    # Set League Definitions
    league_name, number_teams, number_rounds, draft_type, number_picks = enter_league_definitions()
    # Create Draft Database
    create_board(league_name)
    # Run draft based on designated draft type
    if draft_type == "SNAKE":
        # Create list of teams
        managers = create_managers_list_for_snake_draft(int(number_teams), int(number_rounds))
        # Enter draft picks into database
        snake_draft(number_picks, number_teams, league_name, managers)
    else:
        # Create list of teams
        managers = create_manager_list(int(number_teams))
        # Enter draft picks into database
        custom_draft(number_picks, number_teams, league_name, managers)
    # Print notification to let user know draft is complete
    print("Your draft is complete for {}!".format(league_name))
    # Small sleep timer for fluiditiy
    time.sleep(3)
    # Display entire draft results
    show_draft_results(league_name)
    # Create csv file from draftboard
    create_csv_from_draft_database(league_name)

start_draft()
