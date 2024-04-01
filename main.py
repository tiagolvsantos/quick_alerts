import time
import argparse
from src import menu_functions as mf


def main(choice=None):
    """
    The main function that runs the menu loop.

    Parameters:
    - choice (str): The user's choice for the menu option. Defaults to None.

    Returns:
    - None

    This function displays a menu and executes the corresponding function based on the user's choice.
    It keeps running in a loop until the user chooses to exit the program.
    """
    menu_options = {
        '1': mf.add_alert_interactive,
        '2': run_alerts,
        '3': mf.delete_all_alerts,
        '4': mf.delete_alerts_for_stock,
        '5': mf.print_all_alerts,
        '6': mf.create_alerts_for_new_all_time_highs,
        '7': mf.create_alerts_for_new_all_time_lows,
        '8': mf.create_moving_average_alerts,
        '9': exit_program,
    }

    while True:
        print_menu()
        if not choice:
            choice = input('Enter your choice: ')
        func = menu_options.get(choice)
        if func:
            func()
            choice = None  # Reset choice after executing the function
        else:
            print('Invalid choice. Please try again.')
            choice = None  # Reset choice to prompt user for input in the next iteration

def run_alerts():
    try:
        while True:
            print("Running alerts...")
            mf.run_alerts()
            time.sleep(600)  # Sleep for 10 minutes
    except KeyboardInterrupt:
        print("Interrupted by user. Returning to main menu...")

def exit_program():
    print('Exiting...')
    exit()
def print_menu():
    """
    Prints the menu.
    """
    print('1. Add alert')
    print('2. Run alerts')
    print('3. Delete all alerts')
    print('4. Delete alerts for a stock')
    print('5. Print all alerts')
    print('6. Create alerts for new all-time highs')
    print('7. Create alerts for new all-time lows')
    print('8. Create alerts 50 DMA')
    print('9. Exit')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--choice", help="Enter your choice")
    args = parser.parse_args()
    main(args.choice)

