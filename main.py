from modules import user,artisan,admin

if __name__ == "__main__":
    print("🛍️ Welcome to Local Artisan Wishlist Marketplace 🛍️")
    while True:
        print("\n--- Main Menu ---")
        print("[1]  User")
        print("[2]  Artisan")
        print("[3]  Admin")
        print("[0]  Exit")
        role_choice = input("Choose role: ")

        if role_choice == "1":
            while True:
                print("\n--- User Menu ---")
                print("[1]  Sign Up")
                print("[2]  Sign In")
                print("[0]  Back")
                choice = input("Choose an option: ")

                if choice == "1":
                    user.register_user()
                elif choice == "2":
                    user.login_user()
                elif choice == "0":
                    break
                else:
                    print("❌ Invalid option.")

        elif role_choice == "2":
            while True:
                print("\n--- Artisan Menu ---")
                print("[1]  Sign Up")
                print("[2]  Sign In")
                print("[0]  Back")
                choice = input("Choose an option: ")

                if choice == "1":
                    artisan.register_artisan()
                elif choice == "2":
                    artisan.login_artisan()
                elif choice == "0":
                    break
                else:
                    print("❌ Invalid option.")

        elif role_choice == "3":
            while True:
                print("\n--- Admin Menu ---")
                print("[1]  Sign Up")
                print("[2]  Sign In")
                print("[0]  Back")
                choice = input("Choose an option: ")

                if choice == "1":
                    admin.register_admin()
                elif choice == "2":
                    admin.login_admin()
                elif choice == "0":
                    break
                else:
                    print("❌ Invalid option.")

        elif role_choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")
