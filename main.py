import time
import argparse
from src import menu_functions as mf


def main(run_alerts_command=False):
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
        '2': lambda: run_alerts(args.run_alerts_command),
        '3': mf.delete_type_alerts,
        '4': mf.delete_alerts_for_stock,
        '5': mf.print_symbol_alert,
        '6': lambda: [mf.create_alerts_for_new_highs(), mf.create_alerts_for_new_lows()],
        '7': lambda: [mf.create_moving_average_alerts(50)],
        '8': mf.create_bollinger_bands_alerts,
        '9': mf.create_rsi_alerts,       
        '10': exit_program,
    }

    while True:
        print_menu()
        if not run_alerts_command:
            choice = input('Enter your choice: ')
        else: 
            choice = '2'
            run_alerts_command = False
        func = menu_options.get(choice)
        if func:
            func()
            choice = None  # Reset choice after executing the function
        else:
            print('Invalid choice. Please try again.')
            choice = None  # Reset choice to prompt user for input in the next iteration

def run_alerts(run_alerts_command):
    try:
        print("Running alerts...")
        while True:
            mf.run_alerts(run_alerts_command, False)
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
    print('3. Delete type alerts')
    print('4. Delete alerts for a symbol')
    print('5. Print symbol alerts')
    print('6. Create alerts for new highs/lows')
    print('7. Create alerts 50 DMA')
    print('8. Create alerts BBbands outside bands')
    print('9. Create alerts RSI')
    print('10. Exit')


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--run_alerts_command", action='store_true', help="Enter your command")
        args = parser.parse_args()
        main(args.run_alerts_command) 
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting...")