# imports
import sqlite3
from datetime import datetime
from datetime import timedelta
import math

# connect database
db = sqlite3.connect('data/bia')
cursor = db.cursor()

#cursor.execute("""DROP TABLE IF EXISTS intervals""")

# create table for reaction data
cursor.execute("""
CREATE TABLE IF NOT EXISTS intervals(
    dt1 DATETIME UNIQUE NOT NULL,
    dt2 DATETIME NOT NULL,
    interval TIME,
    type TEXT,
    epi TEXT,
    CONSTRAINT pk_intervals PRIMARY KEY (dt1,dt2))
""")
db.commit()


# Reaction class
class Reaction:

    # init
    def __init__(self, dt1, dt2, rtype, epi):
        self.dt1 = dt1
        self.dt2 = dt2
        self.rtype = rtype
        self.epi = epi

    # get dt1
    def get_dt1(self):
        return self.dt1

    # get dt2
    def get_dt2(self):
        return self.dt2

    # calculate reaction interval
    def interval(self):

        start = self.get_dt1()
        end = self.get_dt2()

        # convert to datetime
        if type(start) == str:

            if len(start) > 16:
                start = start[:-3]
                end = end[:-3]

            start = datetime.strptime(start, '%Y-%m-%d %H:%M')
            end = datetime.strptime(end, '%Y-%m-%d %H:%M')

        total_seconds = (end - start).seconds
        total_minutes = math.floor(total_seconds / 60)

        hours = math.floor(total_minutes / 60)
        minutes = total_minutes % 60

        interval = f'{hours:0>2d}:{minutes:0>2d}'

        return interval

    # string
    def __str__(self):
        interval = self.interval()
        interval_split = interval.split(':')
        hours = interval_split[0]
        minutes = interval_split[1]

        dt1 = self.get_dt1()
        dt2 = self.get_dt2()

        # remove seconds parameter from datetime
        if len(dt1) > 16:
            dt1 = dt1[:-3]
            dt2 = dt2[:-3]

        output = ''
        output += f'First reaction: {dt1}\n'
        output += f'Second reaction: {dt2}\n'
        output += f'Interval: {hours} hours {minutes} minutes\n'
        output += f'Type: {self.rtype}\n'
        output += f'Adrenaline: {self.epi}\n'

        return output


# interval as hours and minutes string
def str_interval(i):
    interval_split = i.split(':')
    hours = interval_split[0]
    minutes = interval_split[1]

    return f'{hours} hours {minutes} minutes'


# calculate total longest interval
def longest_total():

    try:
        # read db
        cursor.execute("""
            SELECT interval
            FROM intervals""")
        li_intervals = cursor.fetchall()

        # error handling for empty list
        if len(li_intervals) > 0:
            i_longest = max(li_intervals)
            output = str_interval(i_longest)
        else:
            output = 'No data available.'

        return output

    except Exception as e:
        raise e


# calculate total shortest interval
def shortest_total():

    try:
        # read db
        cursor.execute("""
            SELECT interval
            FROM intervals""")
        li_intervals = cursor.fetchall()

        # error handling for empty list
        if len(li_intervals) > 0:
            i_shortest = min(li_intervals)
            output = str_interval(i_shortest)
        else:
            output = 'No data available.'

        return output

    except Exception as e:
        raise e


# calculate total average
def average_total():
    try:
        # read db
        cursor.execute("""
            SELECT interval
            FROM intervals""")
        li_ints = cursor.fetchall()

        li_intervals = []
        for i in li_ints:
            li_intervals.append(f'{i[0]}')

        # calculate total time in minutes and no. of reactions
        tot_minutes = 0
        reactions = 0
        for i in li_intervals:
            m = datetime.strptime(i, '%H:%M')
            tot_minutes += m
            reactions += 1

        # average interval in minutes
        try:
            avg_minutes = tot_minutes / reactions

        except ZeroDivisionError:
            avg_minutes = 0

        hours = math.floor(avg_minutes / 60)
        minutes = tot_minutes % 60

        # avg interval in hours and minutes
        if len(li_intervals) > 0:
            avg_interval = f'{hours} hours {minutes} minutes'
        else:
            avg_interval = 'No data available.'

        return avg_interval

    except Exception as e:
        raise e


# calculate longest interval by type of reaction
def longest_type(rtype):

    try:
        # read db
        cursor.execute("""
            SELECT interval
            FROM intervals
            WHERE type=?""",
            [rtype])
        li_intervals = cursor.fetchall()

        # error handling for empty list
        if len(li_intervals) > 0:
            i_longest = max(li_intervals)
            output = str_interval(i_longest)
        else:
            output = 'No data available.'

        return output

    except Exception as e:
        raise e


# calculate shortest interval by reaction type
def shortest_type(rtype):

    try:
        # read db
        cursor.execute("""
            SELECT interval
            FROM intervals
            WHERE type=?""",
            [rtype])
        li_intervals = cursor.fetchall()

        # error handling for empty list
        if len(li_intervals) > 0:
            i_shortest = min(li_intervals)
            output = str_interval(i_shortest)
        else:
            output = 'No data available.'

        return output

    except Exception as e:
        raise e


# calculate average for anaphylaxis/asthma
def average_type(rtype):
    try:
        # read db
        cursor.execute("""
            SELECT interval
            FROM intervals
            WHERE type=?""",
            [rtype])
        li_ints = cursor.fetchall()

        li_intervals = []
        for i in li_ints:
            li_intervals.append(f'{i[0]}')

        # calculate total time in minutes and no. of reactions
        tot_minutes = 0
        reactions = 0
        for i in li_intervals:
            m = datetime.strptime(i, '%H:%M')
            tot_minutes += m
            reactions += 1

        # average interval in minutes
        try:
            avg_minutes = tot_minutes / reactions

        except ZeroDivisionError:
            avg_minutes = 0

        hours = math.floor(avg_minutes / 60)
        minutes = tot_minutes % 60

        # avg interval in hours and minutes
        if len(li_intervals) > 0:
            avg_interval = f'{hours} hours {minutes} minutes'
        else:
            avg_interval = 'No data available.'

        return avg_interval

    except Exception as e:
        raise e


# calculate longest interval by adrenaline Y/N
def longest_epi(epi):

    try:
        # read db
        cursor.execute("""
            SELECT interval
            FROM intervals
            WHERE epi=?""",
            [epi])
        li_intervals = cursor.fetchall()

        # error handling for empty list
        if len(li_intervals) > 0:
            i_longest = max(li_intervals)
            output = str_interval(i_longest)
        else:
            output = 'No data available.'

        return output

    except Exception as e:
        raise e


# calculate shortest interval by adrenaline Y/N
def shortest_epi(epi):

    try:
        # read db
        cursor.execute("""
            SELECT interval
            FROM intervals
            WHERE epi=?""",
            [epi])
        li_intervals = cursor.fetchall()

        # error handling for empty list
        if len(li_intervals) > 0:
            i_shortest = min(li_intervals)
            output = str_interval(i_shortest)
        else:
            output = 'No data available.'

        return output

    except Exception as e:
        raise e


# calculate average for reactions treated with/without adrenaline
def average_epi(epi):
    try:
        # read db
        cursor.execute("""
            SELECT interval
            FROM intervals
            WHERE epi=?""",
            [epi])
        li_ints = cursor.fetchall()

        li_intervals = []
        for i in li_ints:
            li_intervals.append(f'{i[0]}')

        # calculate total time in minutes and no. of reactions
        tot_minutes = 0
        reactions = 0
        for i in li_intervals:
            m = datetime.strptime(i, '%H:%M')
            tot_minutes += m
            reactions += 1

        # average interval in minutes
        try:
            avg_minutes = tot_minutes / reactions

        except ZeroDivisionError:
            avg_minutes = 0

        hours = math.floor(avg_minutes / 60)
        minutes = tot_minutes % 60

        # avg interval in hours and minutes
        if len(li_intervals) > 0:
            avg_interval = f'{hours} hours {minutes} minutes'
        else:
            avg_interval = 'No data available.'

        return avg_interval

    except Exception as e:
        raise e


# welcome message and stats
def welcome():

    # stats
    total_average = average_total()
    total_longest = longest_total()
    total_shortest = shortest_total()

    # output
    welcome_output = ''
    welcome_output += 'Welcome!\n'
    welcome_output += '\n'
    welcome_output += 'Quick stats:\n'
    welcome_output += f'\tAverage interval: {total_average}\n'
    welcome_output += f'\tLongest interval: {total_longest}\n'
    welcome_output += f'\tShortest interval: {total_shortest}\n'

    print(welcome_output)


# add reaction
def add_reaction():

    # user inputs dates and times of reactions, reaction type, and treatment
    d1 = input('Date (YYYY-MM-DD): ')
    t1 = input('Time (HH:MM): ')
    d2 = input('Date (YYYY-MM-DD): ')
    t2 = input('Time (HH:MM): ')
    rtype = input('Anaphylaxis or asthma? ')
    epi = input('Adrenaline? (Yes/No): ')

    # create dt1 and dt2 from inputs
    dt1 = datetime.strptime(f'{d1} {t1}', '%Y-%m-%d %H:%M')
    dt2 = datetime.strptime(f'{d2} {t2}', '%Y-%m-%d %H:%M')

    # calculate interval
    reaction = Reaction(dt1, dt2, rtype, epi)
    interval = reaction.interval()

    # insert interval into db
    try:

        cursor.execute("""
            INSERT INTO intervals(dt1, dt2, interval, type, epi)
            VALUES (?,?,?,?,?)""",
        [dt1, dt2, interval, rtype, epi])
        db.commit()

        # print interval
        interval_split = interval.split(':')
        hours = interval_split[0]
        minutes = interval_split[1]

        success = f'\nInterval: {hours} hours {minutes} minutes\n'
        print(success)

    # error handling
    except Exception as e:
        raise e

    # return to menu
    finally:
        return


# edit reaction data
def edit():
    edit_options = input("""What would you like to edit?
1. Second reaction date or time
2. Type of reaction
3. Treatment with adrenaline
""")

    try:

        # edit second reaction date and time
        if edit_options == '1':

            d2 = input('Date  (YYYY-MM-DD): ')
            t2 = input('Time (HH:MM): ')
            dt2 = f'{d2}:{t2}'

            # insert into db
            cursor.execute("""
                INSERT INTO intervals(dt2)
                VALUES (?)""",
                [dt2])
            db.commit()

        # edit type of reaction
        if edit_options == '2':

            rtype = input('Type: ')

            # insert into db
            cursor.execute("""
                INSERT INTO intervals(type)
                VALUES (?)""",
                [rtype])
            db.commit()

        # edit treatment
        if edit_options == '3':

            epi = input('Was this reaction treated with adrenaline? ')

            # insert into db
            cursor.execute("""
                INSERT INTO intervals(epi)
                VALUES (?)""",
                [epi])
            db.commit()

    except Exception as e:
        raise e

    finally:
        return


# edit reaction initial menu
def edit_reaction():

    know_prev = input('Do you know the date and time of the first reaction? ')

    if know_prev.lower() == 'no':
        view_reactions()
        edit()

    if know_prev.lower() == 'yes':
        edit()


# view reactions
def view_reactions():
    try:
        # read db
        cursor.execute("""
            SELECT dt1, dt2, type, epi
            FROM intervals""")
        li_reactions = cursor.fetchall()

        # error handling empty list
        if len(li_reactions) > 0:
            # print reactions
            for row in li_reactions:
                print(Reaction(row[0], row[1], row[2], row[3]))
        else:
            print('No data available.\n')

    except Exception as e:
        raise e


# view averages
def view_averages():

    # calculate averages
    avg_total = average_total()
    avg_anaphylaxis = average_type('Anaphylaxis')
    avg_asthma = average_type('Asthma')
    avg_epi = average_epi('Yes')
    avg_no_epi = average_epi('No')

    # output
    avg_output = ''
    avg_output += f'Total: {avg_total}\n'
    avg_output += f'Anaphylaxis: {avg_anaphylaxis}\n'
    avg_output += f'Asthma: {avg_asthma}\n'
    avg_output += f'With adrenaline: {avg_epi}\n'
    avg_output += f'Without adrenaline: {avg_no_epi}\n'

    print(avg_output)


# view stats
def view_stats():

    # total
    avg_total = average_total()
    long_total = longest_total()
    short_total = shortest_total()

    # anapylaxis
    avg_anaphylaxis = average_type('Anaphylaxis')
    long_anaphylaxis = longest_type('Anaphylaxis')
    short_anaphylaxis = shortest_type('Anaphylaxis')

    # asthma
    avg_asthma = average_type('Asthma')
    long_asthma = longest_type('Asthma')
    short_asthma = shortest_type('Asthma')

    # with adrenaline
    avg_epi = average_epi('Yes')
    long_epi = longest_epi('Yes')
    short_epi = shortest_type('Yes')

    # without adrenaline
    avg_no_epi = average_epi('No')
    long_no_epi = longest_epi('No')
    short_no_epi = shortest_epi('No')

    # output
    stats_output = ''
    stats_output += f'Average: {avg_total}\n'
    stats_output += f'Longest: {long_total}\n'
    stats_output += f'Shortest: {short_total}\n'
    stats_output += '\n'
    stats_output += f'Average anaphylaxis: {avg_anaphylaxis}\n'
    stats_output += f'Longest anaphylaxis: {long_anaphylaxis}\n'
    stats_output += f'Shortest anaphylaxis: {short_anaphylaxis}\n'
    stats_output += '\n'
    stats_output += f'Average asthma: {avg_asthma}\n'
    stats_output += f'Longest asthma: {long_asthma}\n'
    stats_output += f'Shortest asthma: {short_asthma}\n'
    stats_output += '\n'
    stats_output += f'Average with adrenaline: {avg_epi}\n'
    stats_output += f'Longest with adrenaline: {long_epi}\n'
    stats_output += f'Shortest with adrenaline: {short_epi}\n'
    stats_output += '\n'
    stats_output += f'Average without adrenaline: {avg_no_epi}\n'
    stats_output += f'Longest without adrenaline: {long_no_epi}\n'
    stats_output += f'Shortest without adrenaline: {short_no_epi}\n'

    print(stats_output)


# display
welcome()

while True:

    # menu
    menu = input("""1. Add new reaction
2. Edit reaction
3. View reactions
4. View averages
5. View stats
0. Exit
""")

    # add new reaction
    if menu == '1':
        add_reaction()
        continue

    # edit reaction
    if menu == '2':
        edit_reaction()
        continue

    # view reactions
    if menu == '3':
        view_reactions()
        continue

    # view averages
    if menu == '4':
        view_averages()
        continue

    # view stats
    if menu == '5':
        view_stats()
        continue

    # exit
    if menu == '0':
        exit()

    # error handling
    else:
        print('Something went wrong.\nPlease try again.\n')
        continue
