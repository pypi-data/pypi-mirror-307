import hashlib
import requests
import sys
import os
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

# Load common passwords from a text file
def load_common_passwords(filename="common_passwords.txt") -> set:
    """
    Load common passwords from a text file.

    Args:
        filename (str): The path to the text file containing common passwords.

    Returns:
        set: A set of common passwords for quick lookup.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found. Ensure the text file is available.")

    with open(filename, "r") as file:
        return set(line.strip().lower() for line in file if line.strip())


# Load common passwords once at startup
COMMON_PASSWORDS = load_common_passwords()


class PasswordChecker:
    def __init__(self, password: str):
        """
        Initialize the PasswordChecker with a password.

        Args:
            password (str): The password to check.
        """
        self.password = password

    def check_pwned(self) -> int:
        """
        Check if the password has been pwned using the HaveIBeenPwned API.

        This method uses k-Anonymity by sending only the first 5 characters of the SHA-1 hash.

        Returns:
            int: The count of times the password has been pwned, or 0 if it hasn't.
        """
        sha1_password = hashlib.sha1(self.password.encode("utf-8")).hexdigest().upper()
        prefix, suffix = sha1_password[:5], sha1_password[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)

        if response.status_code != 200:
            raise RuntimeError("Error fetching data from PwnedPasswords API")

        hashes = (line.split(":") for line in response.text.splitlines())
        for hash_suffix, count in hashes:
            if hash_suffix == suffix:
                return int(count)  # Password has been pwned 'count' times
        return 0

    def find_common_password(self) -> str:
        """
        Check if the password contains any common password as a substring, case-insensitive.

        Returns:
            str: The common password found within the user password, or an empty string if none found.
        """
        password_lower = self.password.lower()
        for common_password in COMMON_PASSWORDS:
            if common_password in password_lower:
                return common_password
        return ""

    def check_security_recommendations(self) -> list:
        """
        Evaluate the password against security best practices.

        Returns:
            list: A list of recommendations to improve the password.
        """
        recommendations = []
        if len(self.password) < 12:
            recommendations.append("Password should be at least 12 characters long.")
        if not any(c.isupper() for c in self.password):
            recommendations.append("Password should contain at least one uppercase letter.")
        if not any(c.islower() for c in self.password):
            recommendations.append("Password should contain at least one lowercase letter.")
        if not any(c.isdigit() for c in self.password):
            recommendations.append("Password should contain at least one digit.")
        if not any(c in "!@#$%^&*()_+{}:;'<>?.,~" for c in self.password):
            recommendations.append("Password should contain at least one special character.")
        return recommendations

    def print_warning(self, message: str):
        """Prints a warning message in red with a warning symbol."""
        warning_symbol = "⚠️"
        print(f"{Fore.RED}{warning_symbol} WARNING: {message}{Style.RESET_ALL}")

    def print_pass(self, message: str):
        """Prints a pass message in green."""
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    def check_password(self):
        """
        Perform all password checks, output warnings first, then a separator, and finally passes.
        """
        warnings = []
        passes = []

        # Check if password has been pwned
        try:
            pwned_count = self.check_pwned()
            if pwned_count > 0:
                warnings.append(f"This password has been pwned {pwned_count} times!")
            else:
                passes.append("Good news: This password has not been found in any known data breaches.")
        except RuntimeError as e:
            warnings.append(f"Error checking password against pwned database: {e}")

        # Check if password contains any common passwords
        found_common = self.find_common_password()
        recommendations = self.check_security_recommendations()

        if found_common:
            warnings.append(
                f"This password contains the common password '{found_common}', possibly making it vulnerable to attacks.")

        if recommendations:
            warnings.append("This password does not meet the recommended security standards:")
            for rec in recommendations:
                warnings.append(f"- {rec}")
        else:
            passes.append("This password is secure by recommended standards.")

        # Output warnings first, followed by passes
        for warning in warnings:
            self.print_warning(warning)
        if warnings and passes:
            print("---")
        for pass_message in passes:
            self.print_pass(pass_message)


def main():
    """
    Main function to handle command-line input or prompt for password input.
    """
    if len(sys.argv) == 2:
        password = sys.argv[1]
    else:
        # Prompt user for password if no argument is provided
        password = input("Enter the password to check: ")

    checker = PasswordChecker(password)
    checker.check_password()


if __name__ == "__main__":
    main()
