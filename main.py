import sys
from menu import Menu
from database import Database
import GUI

#added a comment
def main():

    connection = Database()
    connection.connect_to_database()
    menu = Menu(connection, None)
    username = menu.login_menu()
    #username = "jbascone"
    menu = Menu(connection, username)

    GUI.create_reservation_screen(connection, username)

    while menu:
        menu.display_menu(username)
        break
    connection.close()
    sys.exit()

if __name__ == "__main__":
    main()
