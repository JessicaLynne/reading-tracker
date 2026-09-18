#==================================================================
# READING TRACKER 1.0 IT-140
# Manages personal library, logs daily reading activity,
# and calculates monthly/weekly and lifetime reading statistics.
#==================================================================

# Imports modules for file management, dates, calendar, and text formatting.
import csv
import calendar
from datetime import date, datetime
from string import capwords

# Allows the user to add a new book to the library.
def add_book():
    print("-Add to Library-")
    while True:
        # Gather title and author; capitalize the first letter of each word.
        title = capwords(input("Enter book title: "))
        author = capwords(input("Enter author name: "))
        while True:
            try:
                # Gather book length in number of pages and make sure the user typed a valid number.
                length = int(input("Enter book length: "))
                break
            except ValueError:
                print("Invalid entry, please enter a number.")
        # Check if the user is adding an already completed book.
        completed_input = input("Completed? (1 for Yes, 2 for No): ")
        if completed_input == "1":
            # If the book is finished, set completed to True and progress to 100.
            completed = True
            progress = "100"

            while True:
                # Check if the book was completed today.
                today_input = input("Completed today? (1 for Yes, 2 for No): ")
                if today_input == "1":
                    # If the book was completed today, get the current system date
                    # and save records to both the library and the log.
                    entry_date = date.today().strftime("%m-%d-%Y")
                    with open("book_library.csv", "a", newline="") as rlib:
                        writer = csv.writer(rlib)
                        # The library contains the title, author, book length,
                        # and True or False for completion status.
                        writer.writerow([title, author, length, completed])
                    with open("reading_log.csv", "a", newline="") as rlog:
                        writer = csv.writer(rlog)
                        # The log contains the title, author,
                        # progress percentage as an integer,
                        # and the date of the log entry.
                        writer.writerow([title, author, progress, entry_date])
                    print("Book added!")
                    break

                elif today_input == "2":
                    while True:
                        # Allow the user to enter a specific completion date or
                        # a "Completed" placeholder so the book is reported in All Time Stats.
                        entry_date = input("Enter completion date as MM-DD-YYYY or unknown: ")
                        if entry_date.lower() == "unknown":
                            entry_date = "Completed"
                            break
                        else:
                            try:
                                # Make sure dates follow the correct format.
                                datetime.strptime(entry_date, "%m-%d-%Y")
                                break
                            except ValueError:
                                print("Invalid entry, please enter a valid date.")
                    # Write historical book progress information to the library and the log.
                    with open("book_library.csv", "a", newline="") as rlib:
                        writer = csv.writer(rlib)
                        writer.writerow([title, author, length, completed])
                    with open("reading_log.csv", "a", newline="") as rlog:
                        writer = csv.writer(rlog)
                        writer.writerow([title, author, progress, entry_date])
                    print("Book added!")
                    break
                else:
                    print("Invalid entry, please type 1 or 2.")

        elif completed_input == "2":
            # Flag the book as incomplete and save only to the library
            completed = False

            with open("book_library.csv", "a", newline="") as rlib:
                writer = csv.writer(rlib)
                writer.writerow([title, author, length, completed])
            print("Book added!")

        else:
            # Check to make sure the user selected a valid option.
            # Otherwise, reprompt with criteria.
            print("Invalid entry, please type 1 or 2.")
            continue

    while True:
        add_more = input("Add another book? (1 for Yes, 2 for No): ")
        if add_more == "1":
            break
        elif add_more == "2":
            return

# Read and display all books stored in the user's library file.
def view_library():
    print("-Library Contents-")
    # Open the library file in read-only mode
    with open("book_library.csv", "r", newline="") as rlib:
        reader = csv.reader(rlib)
        count = 1
        # Read the contents of each row
        for row in reader:
            title, author, length, completed = row
            # Translate the status to "Completed" or "In Progress".
            if completed == "True":
                status = "Completed"
            else:
                status = "In progress"
            # Print a numbered list of all books and their details to the screen.
            print(f"{count}. {title}, {author}, {length} pages, {status}")
            count = count + 1

    # Keep the library open until the user is ready to leave.
    while True:
        go_back = input("Back to Menu? (1 for Yes, 2 for No): ").strip()
        if go_back == "1":
            return
        elif go_back == "2":
            continue
        else:
            print("Invalid entry, please type 1 or 2.")

# Create a new reading log entry for a book that is currently in progress.
def log_entry(entry_date):
    while True:
        # Open the library file and scan for active books.
        with open("book_library.csv", "r", newline="") as rlib:
            library = list(csv.reader(rlib))
            in_progress_books = []
            count = 1
            print("-Book List-")
            # Filter for books marked as incomplete; considered in progress.
            for book in library:
                if book[3] == "False":
                    in_progress_books.append(book)
                    print(f"{count}. {book[0]}, {book[1]}")
                    count = count + 1

        # If there are no books in progress, notify the user.
        if not in_progress_books:
            print("No books in progress.")
            return

        while True:
            try:
                # Prompt the user to select a book by its number.
                # Converts the user entry to an integer and adds it to the list.
                book_selection = list(in_progress_books[int(input("Select book: ")) -1])
                break
            except (ValueError, IndexError):
                # Check for typing errors.
                print("Invalid selection, please enter a valid number from the list.")
        while True:
            # Prompt the user for the completed page count or percentage completed.
            # The user must use % to indicate percentage otherwise it is read as a page number.
            progress_input = input("Enter progress as page number or percentage (requires% after number): ").strip()
            # Convert either input into a flat 0-100 percentage integer.
            if "%" in progress_input:
                user_progress = int(progress_input.replace("%", ""))
            elif progress_input.isdigit():
                # Uses index 2 to find the total pages from the library file.
                user_progress = int((int(progress_input) / int(book_selection[2]))* 100)
            else:
                user_progress = 0

            # Checks if the user entered progress at or over 100.
            if user_progress >= 100:
                if input("Book complete? (1 for Yes, 2 for No): ").strip() == "1":
                    book_selection[3] = "True"
                    progress = "100"
                    with open("book_library.csv", "w", newline="") as rlib:
                        writer = csv.writer(rlib)
                        writer.writerows(library)
                    with open("reading_log.csv", "a", newline="") as rlog:
                        writer = csv.writer(rlog)
                        writer.writerow([book_selection[0], book_selection[1], progress, entry_date])
                    print("Reading log updated!")
                    break
                else:
                    print("Entered progress was 100% or more.")
                    continue

            # If the book is still in progress, save the calculated percentage to the reading log.
            else:
                with open("reading_log.csv", "a", newline="") as rlog:
                    writer = csv.writer(rlog)
                    writer.writerow([book_selection[0], book_selection[1], user_progress, entry_date])
                print("Reading log updated!")
                break

        # Ask if the user wants to log additional books.
        add_more = input("Log another book? (1 for Yes, 2 for No): ").strip()
        if add_more == "1":
            continue
        elif add_more == "2":
            break
# Logs an entry with the current system date.
def quick_log():
    log_entry(date.today().strftime("%m-%d-%Y"))

# Allows the user to log an entry for a specific past date.
def log_prev():
    while True:
        entry_date = input("Enter reading log date as MM-DD-YYYY: ")
        try:
            datetime.strptime(entry_date, "%m-%d-%Y")
            break
        except ValueError:
            print("Invalid date, must be MM-DD-YYYY.")
    log_entry(entry_date)

# Processes reading statistics for a specific month and year.
def calc_monthly_stats(month, year):
    with open("reading_log.csv", "r", newline="") as rlog:
        rows = list(csv.reader(rlog))
        filtered_entries = []
        unique_days = set()
        total_compl = 0

        for row in rows:
            title, author, progress, entry_date = row

            # Locates only calendar dates and extracts the month, day, and year.
            if "-" in entry_date:
                row_month, row_day, row_year = entry_date.split("-")
            else:
                # The "Completed" placeholder is converted to dummy values.
                row_month, row_day, row_year = "00", "00", "0000"

            # Filters for books in the current month and aggregates active dates and book completions.
            if int(row_month) == int(month) and int(row_year) == int(year):
                filtered_entries.append(row)
                unique_days.add(int(row_day))
                if progress == "100":
                    total_compl += 1

        active_days = len(unique_days)
        # Builds a calendar for the month.
        cal_weeks = calendar.monthcalendar(int(year), int(month))
        total_weeks = len(cal_weeks)
        active_weeks = 0
        active_days_wk = []

        # Determines matching active dates.
        for week in cal_weeks:
            days_active_this_week = 0
            for day in week:
                if day in unique_days:
                    days_active_this_week += 1

            if days_active_this_week > 0:
                active_weeks += 1

            # Appends the calculated active day total to the list.
            active_days_wk.append(days_active_this_week)

        return active_days, active_weeks, total_weeks, active_days_wk, total_compl

# Displays a performance dashboard for the current month.
def current_month_stats():
    today = date.today()
    month = today.month
    year = today.year
    month_name = today.strftime("%B")

    # Pulls the processed totals.
    active_days, active_weeks, total_weeks, active_days_wk, total_compl = calc_monthly_stats(month, year)
    print(f"-{month_name} Reading Stats-")
    print(f"You have been active during {active_weeks} of {total_weeks} week(s) so far this month.")
    print(f"you logged reading time on {active_days} day(s).")
    print("Progress by Week:")

    # Iterates through the weekly list array data to print the weekly progress lines.
    for week_num, days_count in enumerate(active_days_wk, start=1):
        print(f"W{week_num}: {days_count} day(s)")

    # Keeps the dashboard open until the user is ready to leave.
    while True:
        go_back = input("Back to Menu? (1 for Yes, 2 for No): ")
        if go_back == "1":
            return
        elif go_back == "2":
            continue
        else:
            print("Invalid entry, please type 1 or 2")
            continue

# Generates lifetime performance from the very first log entry forward
# including all completed books, even those without a specific date.
def all_time_stats():
    today = date.today()
    print("\n-All-Time Reading Stats-")

    total_compl = 0
    unique_all_time_days = set()
    all_dates = []

    #Opens reading log to find all progress and completions.
    with open("reading_log.csv", "r", newline="") as rlog:
        rows = list(csv.reader(rlog))
        for row in rows:
            title, author, progress, entry_date = row

            # Converts string to correct date format.
            if "-" in entry_date:
                unique_all_time_days.add(entry_date)
                date_obj = datetime.strptime(entry_date, "%m-%d-%Y").date()
                all_dates.append(date_obj)

            # Determines total completed books.
            if progress == "100" or entry_date == "Completed":
                total_compl += 1

    # Calculates total days from the first log entry to present day.
    if all_dates:
        # Finds the earliest reading log entry.
        first_date = min(all_dates)
        today = date.today()
        # Calculates the timeline in number of days.
        total_days = (today - first_date).days + 1

    else:
        total_days = 0

    # Displays a lifetime performance dashboard.
    print(f"You have completed {total_compl} books so far.")
    print(f"You logged reading time on {len(unique_all_time_days)} day(s) out of {total_days} so far.")

    while True:
        go_back = input("Back to Menu? (1 for Yes, 2 for No): ")
        if go_back == "1":
            return
        elif go_back == "2":
            continue
        else:
            print("Invalid entry, please type 1 or 2")
            continue

# Main menu functions
def main():
    while True:
        print("\n=== READING TRACKER 1.0 ===")
        print("1. Add Book")
        print("2. View Library")
        print("3. Quick Log")
        print("4. Log Previous")
        print("5. View Current Month Stats")
        print("6. View All Time Stats")
        print("To leave, type Bye")

        choice = input("Enter selection: ").strip()

        # Processes the user's choice and exits if they type "bye".
        if choice == "1":
            add_book()
        elif choice == "2":
            view_library()
        elif choice == "3":
            quick_log()
        elif choice == "4":
            log_prev()
        elif choice == "5":
            current_month_stats()
        elif choice == "6":
            all_time_stats()
        elif choice.lower() == "bye":
            # A goodbye quote from Derek (The Good Place).
            print("Thanks for tracking.\nGoodbob! I hope we same place again, very now!")
            break
        else:
            print("Invalid entry, please try again.")

if __name__ == "__main__":
        main()