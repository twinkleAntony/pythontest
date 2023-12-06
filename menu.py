def exit():
    pass


def main_menu():
    while True:
        print("\nSimple OS Menu:")
        print("1.Install modsecurity")
        print("2. configure mod sec")
        print("3. Add rule sets")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            print('choice 1')
        elif choice == "2":
            print('choice 2')

        elif choice == "3":
            print('choice 3')

        elif choice == "4":
            exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main_menu()
