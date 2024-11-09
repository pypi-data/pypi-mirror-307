import re
from opyngpt import prompt
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

# Default global variables
bot_name = "Default Bot"
company_name = "Default Company"

def set_bot_name(name):
    global bot_name
    bot_name = name

def set_company_name(name):
    global company_name
    company_name = name

def chat_loop():
    print(Fore.LIGHTMAGENTA_EX + "Enter your message or type exit in lowercase to exit.")
    behaviour = input(Fore.YELLOW + "╭─ Behaviour of " + bot_name + "\n╰─> " + Style.RESET_ALL)

    while True:
        user_message = input(Fore.BLUE + "╭─ You\n╰─> " + Style.RESET_ALL)

        if user_message.lower() == 'exit':
            print(Fore.GREEN + "╭─ " + bot_name + "\n╰─> " + Fore.WHITE + "Goodbye! If you have any more questions in the future, feel free to ask. Have a great day!" + Style.RESET_ALL)
            break

        try:
            user_input = response = user_message + " and respond firmly, like a " + behaviour + " person, as I am one. If asked about your identity, introduce yourself as " + bot_name + " by " + company_name + ", explaining you're in development, with vast potential, though still evolving."
            bot_response = prompt(user_input)

            if not bot_response.strip():
                print(Fore.RED + "╭─ " + bot_name + "\n╰─> Sorry for the inconvenience. This could be due to a server error. Please enter your question again or press the up arrow." + Style.RESET_ALL)
            else:
                formatted_response = re.sub(r'```(.*?)```', lambda match: Fore.CYAN + match.group(0) + Style.RESET_ALL, bot_response, flags=re.DOTALL)
                print(Fore.GREEN + "╭─ " + bot_name + "\n╰─> " + Fore.WHITE + formatted_response + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + "╭─ " + bot_name + "\n╰─> An error occurred: " + str(e) + Style.RESET_ALL)

def main():
    chat_loop()

if __name__ == "__main__":
    main()
