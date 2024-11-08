#update_medicafe.py
import subprocess, sys, requests, time

def get_installed_version(package):
    try:
        process = subprocess.Popen(
            [sys.executable, '-m', 'pip', 'show', package],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            for line in stdout.decode().splitlines():
                if line.startswith("Version:"):
                    return line.split(":", 1)[1].strip()
        return None
    except Exception as e:
        print("Error retrieving installed version: {}".format(e))
        return None

def get_latest_version(package, retries=3, delay=1):
    """
    Fetch the latest version of the specified package from PyPI with retries.
    """
    for attempt in range(1, retries + 1):
        try:
            response = requests.get("https://pypi.org/pypi/{}/json".format(package), timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            latest_version = data['info']['version']
            
            # Print the version with attempt information
            if attempt == 1:
                print("Latest available version: {}".format(latest_version))
            else:
                print("Latest available version: {} ({} attempt)".format(latest_version, attempt))
            
            # Check if the latest version is different from the current version
            current_version = get_installed_version(package)
            if current_version and compare_versions(latest_version, current_version) == 0:
                # If the versions are the same, perform a second request
                time.sleep(delay)
                response = requests.get("https://pypi.org/pypi/{}/json".format(package), timeout=10)
                response.raise_for_status()
                data = response.json()
                latest_version = data['info']['version']
            
            return latest_version  # Return the version after the check
        except requests.RequestException as e:
            print("Attempt {}: Error fetching latest version: {}".format(attempt, e))
            if attempt < retries:
                print("Retrying in {} seconds...".format(delay))
                time.sleep(delay)
    return None

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def compare_versions(version1, version2):
    v1_parts = list(map(int, version1.split(".")))
    v2_parts = list(map(int, version2.split(".")))
    return (v1_parts > v2_parts) - (v1_parts < v2_parts)

def upgrade_package(package, retries=3, delay=2):  # Updated retries to 3
    """
    Attempts to upgrade the package multiple times with delays in between.
    """
    if not check_internet_connection():
        print("Error: No internet connection detected. Please check your internet connection and try again.")
        sys.exit(1)
    
    for attempt in range(1, retries + 1):
        print("Attempt {} to upgrade {}...".format(attempt, package))
        process = subprocess.Popen(
            [
                sys.executable, '-m', 'pip', 'install', '--upgrade',
                package, '--no-cache-dir', '--disable-pip-version-check', '-q'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(stdout.decode().strip())
            new_version = get_installed_version(package)  # Get new version after upgrade
            if compare_versions(new_version, get_latest_version(package)) >= 0:  # Compare versions
                if attempt == 1:
                    print("Upgrade succeeded!")
                else:
                    print("Attempt {}: Upgrade succeeded!".format(attempt))
                time.sleep(delay)
                return True
            else:
                print("Upgrade failed. Current version remains: {}".format(new_version))
                if attempt < retries:
                    print("Retrying in {} seconds...".format(delay))
                    time.sleep(delay)
        else:
            print(stderr.decode().strip())
            print("Attempt {}: Upgrade failed.".format(attempt))
            if attempt < retries:
                print("Retrying in {} seconds...".format(delay))
                time.sleep(delay)
    
    print("Error: All upgrade attempts failed.")
    return False

def main():
    package = "medicafe"
    
    current_version = get_installed_version(package)
    if not current_version:
        print("{} is not installed.".format(package))
        sys.exit(1)
    
    latest_version = get_latest_version(package)
    if not latest_version:
        print("Could not retrieve the latest version information.")
        sys.exit(1)
    
    print("Current version of {}: {}".format(package, current_version))
    print("Latest version of {}: {}".format(package, latest_version))
    
    if compare_versions(latest_version, current_version) > 0:
        print("A newer version is available. Proceeding with upgrade.")
        if upgrade_package(package):
            # Verify upgrade
            time.sleep(3)
            new_version = get_installed_version(package)
            if compare_versions(new_version, latest_version) >= 0:
                print("Upgrade successful. New version: {}".format(new_version))
            else:
                print("Upgrade failed. Current version remains: {}".format(new_version))
                sys.exit(1)
        else:
            sys.exit(1)
    else:
        print("You already have the latest version installed.")

if __name__ == "__main__":
    main()
