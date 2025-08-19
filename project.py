import PySimpleGUI as sg
import sys
import csv


def main():
    layout = [
        [
            sg.T("Username:", size=(10, 1), font=("None 16")),
            sg.I(key="-USER-", font=("None 16"), size=(32, 1)),
        ],
        [
            sg.T("Password:", size=(10, 1), font=("None 16")),
            sg.I(key="-PASS-", font=("None 16"), size=(32, 1)),
        ],
        [
            sg.Exit(size=(10, 1), button_color="red"),
            sg.B("Login", key="-LOG-", size=(10, 1), button_color="blue"),
            sg.B("Register", key="-REG-", size=(10, 1), button_color="green"),
        ],
    ]

    window = sg.Window("Login To Do", layout)

    while True:
        event, value = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            sys.exit()
        elif event == "-REG-":
            register(value["-USER-"], value["-PASS-"], window)
        elif event == "-LOG-":
            if login(value["-USER-"], value["-PASS-"], window):
                break
            else:
                login(value["-USER-"], value["-PASS-"], window)
    todo()


# register user


def register(username, password, window):
    if not username or not password:
        sg.popup(
            "Username or password cannot be empty", text_color="red", font=("None 16")
        )
        return False
    else:
        with open("logins.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
            sg.popup("Registered!", font=("None 16"))
            window["-USER-"].update("")
            window["-PASS-"].update("")
        return True


# login user


def login(username, password, window, close_window=True):
    if not username or not password:
        sg.popup(
            "Username or password cannot be empty", text_color="red", font=("None 16")
        )
        return False
    else:
        with open("logins.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
                    sg.popup("Login Successful", font=("None 16"))
                    if close_window:
                        window.close()
                    return True
    sg.popup("Invalid username or password", font=("None 16"))
    return False


# todo list GUI


def todo():
    layout = [
        [
            sg.CalendarButton("Set date", size=(10, 1)),
            sg.T("-- -- -- --", key="-DATE-"),
        ],
        [
            sg.T("What To Do:", font=("None 16"), size=(9, 1)),
            sg.I(key="-TASK-", font=("None 16"), size=(38, 1)),
        ],
        [
            sg.Table(
                values="",
                headings=["Date", "Task"],
                key="-TABLE-",
                enable_events=True,
                size=(500, 10),
                auto_size_columns=False,
                col_widths=[9, 35],
                justification="c",
                font=("None 16"),
            )
        ],
        [
            sg.Exit(size=(10, 1), button_color="red"),
            sg.B("Complete", key="-COMP-", size=(10, 1), button_color="orange"),
            sg.B("Add", size=(10, 1), button_color="green"),
        ],
    ]

    window = sg.Window("To-Do List", layout)
    tasks = []
    while True:
        event, value = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            window.close()
            break
        elif event == "Add":
            date = window["-DATE-"].get().split()[0]
            task = [[date, value["-TASK-"]]]
            tasks += task
            window["-TABLE-"].update(tasks)
            window["-TASK-"].update("")
        elif event == "-COMP-":
            if value["-TABLE-"]:
                index = value["-TABLE-"][0]
                del tasks[index]
                window["-TABLE-"].update(tasks)


if __name__ == "__main__":
    main()
