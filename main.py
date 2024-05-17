import time
import argparse
from src import menu_functions as mf

def set_play_sound(value):
    global play_sound
    play_sound = value
    print(f"Sound is now {'enabled' if play_sound else 'disabled'}")
    
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
    global play_sound
    play_sound = False

    print(play_sound)
    menu_options = {
        '1': mf.add_alert_interactive,
        '2': lambda: run_alerts(args.run_alerts_command, play_sound),
        '3': mf.delete_type_alerts,
        '4': mf.delete_alerts_for_stock,
        '5': mf.print_manual_alerts,
        '6': mf.print_symbol_alert,
        '7': lambda: [mf.create_alerts_for_new_highs(), mf.create_alerts_for_new_lows()],
        '8': lambda: [mf.create_moving_average_alerts(50)],
        '9': mf.create_bollinger_bands_alerts,
        '10': mf.create_rsi_alerts,       
        '11': exit_program,
        's': lambda: set_play_sound(True),
        'ba': mf.add_bulk_alerts,
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

def run_alerts(run_alerts_command, play_sound):
    try:
        print("Running alerts...")
        while True:
            mf.run_alerts(run_alerts_command, play_sound, False)
            time.sleep(1800)  # Sleep for 30 minutes
    except KeyboardInterrupt:
        print("Interrupted by user. Returning to main menu...")

def exit_program():
    print('Exiting...')
    exit()

def print_menu():
    """
    Prints the menu.
    """
    print('MENU_________________________________')
    print('1 -  Add alert')
    print('2 -  Run alerts')
    print('3 -  Delete type alerts')
    print('4 -  Delete alerts for a symbol')
    print('5 -  Print manual alerts')
    print('6 -  Print symbol alerts')
    print('7 -  Create alerts for new highs/lows')
    print('8 -  Create alerts 50 DMA')
    print('9 -  Create alerts BBbands outside bands')
    print('10 - Create alerts RSI')
    print('11 - Exit')
    print('OPTIONS______________________________')
    print('s -  Enable sound for alerts')
    print('ba -  Add multiple alerts at once from bulk_alerts.xls file')
    print()


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--run_alerts_command", action='store_true', help="Enter your command")
        args = parser.parse_args()
        main(args.run_alerts_command) 
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting...")