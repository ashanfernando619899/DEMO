import sqlite3
from abc import ABC, abstractmethod



# ABSTRACT PRODUCT CLASS
# FACTORY PATTERN PART


class Fish(ABC):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_category(self):
        pass



# CONCRETE PRODUCT CLASSES


class Goldfish(Fish):
    def get_name(self):
        return "Goldfish"

    def get_category(self):
        return "Freshwater Fish"


class Shark(Fish):
    def get_name(self):
        return "Shark"

    def get_category(self):
        return "Marine Fish"


class Angelfish(Fish):
    def get_name(self):
        return "Angelfish"

    def get_category(self):
        return "Tropical Fish"


class Tuna(Fish):
    def get_name(self):
        return "Tuna"

    def get_category(self):
        return "Marine Fish"


class Salmon(Fish):
    def get_name(self):
        return "Salmon"

    def get_category(self):
        return "Freshwater/Marine Fish"



# FISH FACTORY CLASS
# FACTORY PATTERN IMPLEMENTATION


class FishFactory:

    # This method creates fish objects based on user choice
    def create_fish(self, choice):

        if choice == "1":
            return Goldfish()

        elif choice == "2":
            return Shark()

        elif choice == "3":
            return Angelfish()

        elif choice == "4":
            return Tuna()

        elif choice == "5":
            return Salmon()

        else:
            return None



# SINGLETON DATABASE MANAGER
# SINGLETON PATTERN IMPLEMENTATION


class AquariumManager:

    _instance = None

    def __new__(cls):

        # Create object only once
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Create SQLite database connection
            cls._instance.connection = sqlite3.connect("aquarium.db")
            cls._instance.cursor = cls._instance.connection.cursor()

        # Return same object every time
        return cls._instance


    # Create fish table
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fish (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fish_name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                available_count INTEGER NOT NULL
            )
        """)
        self.connection.commit()


    # Add or update fish details
    def add_or_update_fish(self, fish, available_count):

        fish_name = fish.get_name()
        category = fish.get_category()

        self.cursor.execute(
            "SELECT available_count FROM fish WHERE fish_name = ?",
            (fish_name,)
        )

        record = self.cursor.fetchone()

        if record:
            self.cursor.execute(
                """
                UPDATE fish
                SET category = ?, available_count = ?
                WHERE fish_name = ?
                """,
                (category, available_count, fish_name)
            )
            print(f"{fish_name} record updated successfully.")

        else:
            self.cursor.execute(
                """
                INSERT INTO fish (fish_name, category, available_count)
                VALUES (?, ?, ?)
                """,
                (fish_name, category, available_count)
            )
            print(f"{fish_name} record added successfully.")

        self.connection.commit()


    # Display fish report
    def display_fish_report(self):

        self.cursor.execute("""
            SELECT fish_name, category, available_count
            FROM fish
            ORDER BY fish_name
        """)

        records = self.cursor.fetchall()

        print("\n===== Auckland Aquarium Fish Report =====")

        if len(records) == 0:
            print("No fish records available.")

        else:
            print(f"{'Fish Name':<15}{'Category':<25}{'Available Count'}")
            print("-" * 60)

            for fish_name, category, count in records:
                print(f"{fish_name:<15}{category:<25}{count}")


    # Close database connection
    def close_connection(self):
        self.connection.close()


# =====================================================
# INPUT VALIDATION
# =====================================================

def get_valid_count():

    while True:
        try:
            count = int(input("Enter number of fish currently available: "))

            if count < 0:
                print("Count cannot be negative. Please try again.")
            else:
                return count

        except ValueError:
            print("Invalid input. Please enter numbers only.")




def main():

    # Factory object creates fish objects
    fish_factory = FishFactory()

    # Singleton objects
    aquarium1 = AquariumManager()
    aquarium2 = AquariumManager()

    # Same ID proves Singleton Pattern
    print("Aquarium Manager 1 ID:", id(aquarium1))
    print("Aquarium Manager 2 ID:", id(aquarium2))

    aquarium1.create_table()

    while True:

        print("\n===== Auckland Aquarium Management System =====")
        print("1. Add / Update Goldfish")
        print("2. Add / Update Shark")
        print("3. Add / Update Angelfish")
        print("4. Add / Update Tuna")
        print("5. Add / Update Salmon")
        print("6. Display Fish Report")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice in ["1", "2", "3", "4", "5"]:

            # Factory creates the correct fish object
            fish = fish_factory.create_fish(choice)

            
            count = get_valid_count()

            # Singleton manager stores fish data
            aquarium1.add_or_update_fish(fish, count)

        elif choice == "6":
            aquarium2.display_fish_report()

        elif choice == "7":
            print("Thank you for using the Auckland Aquarium Management System.")
            aquarium1.close_connection()
            break

        else:
            print("Invalid choice. Please select 1 to 7.")


main()