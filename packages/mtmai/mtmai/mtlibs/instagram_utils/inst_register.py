# -*- coding: utf-8 -*-
import csv
import hashlib
import logging
import os
import random
import string
import sys
import threading
import time
import uuid
import warnings
from datetime import datetime
from queue import Queue

import names
import requests
from faker import Faker
from mtmai.mtlibs.instagrapi import Client
from mtmai.mtlibs.instagrapi.mixins.challenge import ChallengeChoice
from pydantic import PydanticDeprecatedSince20
from requests.exceptions import SSLError

warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)

# Load proxies from environment variable
API_KEY = os.getenv("api-key")
# Y = "20699d0b4e114c3A999c209028121398"
# Set up logging configuration

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

image_folder = "img"


def select_random_image():
  images = [img for img in os.listdir(image_folder) if img.lower().endswith((".png", ".jpg", ".jpeg"))]
  if not images:
    raise Exception("No images found in the img folder.")
  return os.path.join(image_folder, random.choice(images))


def load_names():
  names_file_path = "names.txt"
  try:
    with open(names_file_path, "r", encoding="utf-8") as names_file:
      names = [name.strip() for name in names_file.readlines() if name.strip()]
    return names
  except Exception as e:
    print(f"Error loading names from {names_file_path}: {str(e)}")
    return []


def select_random_image1(image_folder):
  images = [img for img in os.listdir(image_folder) if img.lower().endswith((".png", ".jpg", ".jpeg"))]
  if not images:
    raise Exception("No images found in the img folder.")
  return os.path.join(image_folder, random.choice(images))


# Function to read emails from the CSV file
def read_emails_from_csv(filename):
  emails = []
  with open(filename, mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
      emails.append(row[0])  # Read the email from the first column
  return emails


# Function to write remaining emails back to the CSV
def write_remaining_emails_to_csv(emails, filename):
  with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Email"])  # Re-add the header row
    for email in emails:
      writer.writerow([email])


def load_non_verified_accounts(csv_file="non-verify.csv"):
  accounts = []
  try:
    with open(csv_file, mode="r", newline="") as file:
      reader = csv.reader(file)
      for row in reader:
        # Assuming the CSV structure is: username, password, phone_number
        if len(row) == 3:  # Make sure there are 3 columns
          username, password, phone_number = row
          accounts.append((username, password, phone_number))
        else:
          print(f"Skipping invalid row: {row}")
  except FileNotFoundError:
    print(f"ERROR: File {csv_file} not found.")
    return accounts  # Return an empty list
  except Exception as e:
    print(f"ERROR: An error occurred while reading the CSV file: {e}")
    return accounts  # Return an empty list

  if not accounts:
    print("No accounts found in the CSV file.")
  return accounts


def remove_verified_account(accounts, username, csv_file="non-verify.csv"):
  # Remove the account from the list
  accounts = [account for account in accounts if account[0] != username]

  # Rewrite the CSV file with the updated list of accounts
  try:
    with open(csv_file, mode="w", newline="") as file:
      writer = csv.writer(file)
      writer.writerows(accounts)
    print(f"Account {username} removed from the CSV file.")
  except Exception as e:
    print(f"ERROR: An error occurred while updating the CSV file: {e}")

  return accounts


names = load_names()
if not names:
  print("No names found in names.txt. Please add some names to the file.")
new_full_name = random.choice(names)


def generate_random_username(new_full_name, existing_usernames):
  """Generate a unique, shuffled username using the full name and random digits."""
  name_base = new_full_name.replace(" ", "").lower()
  name_shuffled = "".join(random.sample(name_base, len(name_base)))
  random_digits = "".join(random.choices(string.digits, k=random.randint(3, 5)))
  username = f"{name_shuffled}{random_digits}"
  while username in existing_usernames:
    name_shuffled = "".join(random.sample(name_base, len(name_base)))
    random_digits = "".join(random.choices(string.digits, k=random.randint(3, 5)))
    username = f"{name_shuffled}{random_digits}"
  existing_usernames.add(username)
  return username


def write_account_to_csv(accounts, output_csv):
  # Read existing accounts from the CSV file
  existing_accounts = set()
  try:
    with open(output_csv, mode="r", newline="") as file:
      reader = csv.DictReader(file)
      for row in reader:
        # Use a tuple of the account details as a unique key
        existing_accounts.add(tuple(row.items()))
  except FileNotFoundError:
    # If the file doesn't exist, just proceed (no existing accounts)
    pass

  # Write the new account to CSV if it's not a duplicate
  with open(output_csv, mode="a", newline="") as file:
    fieldnames = ["username", "password", "authfa"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # If file is empty, write the header
    if file.tell() == 0:
      writer.writeheader()

    for account in accounts:
      account_tuple = tuple(account.items())
      if account_tuple not in existing_accounts:
        writer.writerow(account)
        existing_accounts.add(account_tuple)
      else:
        print(f"Duplicate found: {account['username']} not added.")


proxy_file_path = "proxies.txt"


def load_proxies(file_path):
  """Loads proxies from a text file."""
  if not os.path.exists(file_path):
    print(f"Proxy file '{file_path}' does not exist.")
    return []

  with open(file_path, "r") as file:
    proxies = [line.strip() for line in file if line.strip()]
  return proxies


def select_proxy(proxies):
  """Displays a list of proxies and allows the user to select one."""
  if not proxies:
    print("No proxies available.")
    sys.exit("Exiting the application.")  # Exit the program with a message

  print("Available Proxies:")
  for idx, proxy in enumerate(proxies, start=1):
    print(f"{idx}: {proxy}")

  while True:
    try:
      choice = int(input("Select a proxy by number: "))
      if 1 <= choice <= len(proxies):
        return proxies[choice - 1]
      else:
        print("Invalid selection. Try again.")
    except ValueError:
      print("Please enter a valid number.")


proxies = load_proxies(proxy_file_path)
selected_proxy = select_proxy(proxies)

if selected_proxy:
  print(f"Selected Proxy: {selected_proxy}")

  # Set up the proxy configuration for your application
  proxy = selected_proxy
  proxies = {"http": proxy, "https": proxy}

  # Example of how to use the proxy configuration
  print("Proxy configuration is ready to be used:")
  print(proxies)


# Function to check IP address
def check_ip():
  try:
    response = requests.get("https://ifconfig.me", proxies=proxies, timeout=10)
    ip_address = response.text.strip()
    # print("Your IP:", ip_address)
    return ip_address
  except requests.RequestException:
    # print("Error checking IP:", e)
    return None


def Username():
  fake = Faker()
  name = fake.name()
  return str(name)


# Functions
def generate_uuid(prefix: str = "", suffix: str = "") -> str:
  return f"{prefix}{uuid.uuid4()}{suffix}"


def generate_android_device_id() -> str:
  return "android-%s" % hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]


def generate_useragent():
  with open("UserAgent.txt", "r") as file:
    agents = file.read().splitlines()
    a = random.choice(agents)
    user = a.split(",")
  return f"Instagram 261.0.0.21.111 Android ({user[7]}/{user[6]}; {user[5]}dpi; {user[4]}; {user[0]}; {user[1]}; {user[2]}; {user[3]}; en_US; {user[9]})"


def get_mid():
  params = None
  api_url = "https://i.instagram.com/api/v1/accounts/login"
  response = requests.get(api_url, params=params, proxies=proxies)
  mid = response.cookies.get("mid")
  if mid != None:
    return mid
  else:
    u01 = "QWERTYUIOPASDFGHJKLZXCVBNM"
    us1 = str("".join(random.choice(u01) for k in range(int(8))))
    return f"Y4nS4g{us1}zwIrWdeYLcD9Shxj"


random_first_name = new_full_name


def generate_jazoest(symbols: str) -> str:
  amount = sum(ord(s) for s in symbols)
  return f"2{amount}"


def Birthday():
  day = str(random.randint(1, 28))
  month = str(random.randint(1, 12))
  year = str(random.randint(1988, 2003))
  birth = [day, year, month]
  return birth


def request_country():
  """Request the country selection from the user."""
  # Country ID mapping for selection
  country_mapping = {
    1: 187,  # USA -> 187
    2: 73,  # Brazil -> 73
    3: 19,  # Nigeria -> 19
    4: 117,  # Portugal -> 117
  }

  print("Please select a country by number:")
  print("1: USA (ID: 187)")
  print("2: Brazil (ID: 73)")
  print("3: Nigeria (ID: 19)")
  print("4: Portugal (ID: 117)")
  print("5: Enter custom country ID manually.")

  try:
    user_input = input("Enter your choice (1-5): ").strip()

    if user_input == "5":
      # Allow the user to enter a custom country ID
      country = int(input("Enter custom country ID: ").strip())
    elif user_input in ["1", "2", "3", "4"]:
      # Map the choice to the corresponding country ID
      country = country_mapping[int(user_input)]
    else:
      print("Invalid selection. Exiting.")
      exit()  # Exit if the user makes an invalid selection

    return country
  except ValueError:
    print("Invalid input. Exiting.")
    exit()  # Exit if invalid input


country = request_country()

API_URL = "https://api.sms-activate.guru/stubs/handler_api.php"


def request_activation(service="ig", country=country, max_price=5.31):
  """Request a phone number for activation using the new API, and return the activation ID and phone number."""
  try:
    # Set up the parameters for the API request
    params = {"api_key": API_KEY, "action": "getNumber", "service": service, "country": country, "maxPrice": max_price}

    # Make the API call to get the phone number
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
      response_text = response.text
      if response_text.startswith("ACCESS_NUMBER:"):
        # Extract the phone number and activation ID
        phone_number = response_text.split(":")[2]
        activation_id = response_text.split(":")[1]  # Assuming activation ID follows the phone number in the response
        # print(f"Phone number for activation: {phone_number}")
        # print(f"Activation ID: {activation_id}")
        return activation_id, phone_number
      else:
        # print(f"Failed to get phone number: {response_text}")
        return None, None
    else:
      # print(f"Failed to request phone number, HTTP Status: {response.status_code}")
      return None, None
  except Exception as e:
    print(f"Error in request_activation: {e}")
    return None, None


def wait_for_sms(activation_id, timeout=300, interval=10):
  """Wait for the SMS code with a 5-minute timeout."""
  try:
    elapsed = 0
    while elapsed < timeout:
      # Get the current status of the activation using the new API
      status_url = f"{API_URL}?api_key={API_KEY}&action=getStatus&id={activation_id}"
      response = requests.get(status_url)

      if response.status_code == 200:
        status = response.text
        if status.startswith("STATUS_OK"):
          return status.split(":")[1]  # Return the SMS code
        elif status == "STATUS_WAIT_CODE":
          time.sleep(interval)
          elapsed += interval
          sys.stdout.write(f"\rWaiting for SMS... {elapsed // 60}m {elapsed % 60}s")
          sys.stdout.flush()
        else:
          print(f"\nUnexpected status: {status}")
          return None
      else:
        print("Failed to check status.")
        return None

    # Timeout reached, no SMS code received
    print("\nTimeout reached. No SMS code received.")
    return None
  except Exception as e:
    print(f"Error during SMS waiting: {e}")
    return None


def request_new_sms_code_and_wait(activation_id, forward=None, timeout=1200, interval=10):
  try:
    print(f"Requesting a new SMS code for activation ID {activation_id}...")
    url = "https://api.sms-activate.ae/stubs/handler_api.php"
    params = {
      "api_key": API_KEY,
      "action": "setStatus",
      "status": 3,  # Request a new SMS
      "id": activation_id,
    }

    if forward:
      params["forward"] = forward

    # Step 1: Request a new SMS code
    response = requests.get(url, params=params)
    if response.status_code != 200:
      print(f"Failed to request a new SMS code. HTTP status: {response.status_code}")
      print("Response:", response.text)
      return None

    print("New SMS code requested. Waiting for the code...")

    # Step 2: Wait for the new code
    elapsed = 0
    while elapsed < timeout:
      # Check the status
      status_response = requests.get(
        url,
        params={
          "api_key": API_KEY,
          "action": "getStatus",
          "id": activation_id,
          "timestamp": int(time.time()),  # Avoid cached responses
        },
      )

      if status_response.status_code != 200:
        print("Failed to retrieve status.")
        return None

      status = status_response.text.strip()
      print(f"API Status Response: {status}")

      if status.startswith("STATUS_OK"):
        code = status.split(":")[1]
        print(f"New SMS code received: {code}")
        return code

      elif status == "STATUS_WAIT_CODE":
        time.sleep(interval)
        elapsed += interval
        sys.stdout.write(f"\rWaiting for new SMS... {elapsed // 60}m {elapsed % 60}s")
        sys.stdout.flush()

      elif status == "STATUS_WAIT_RESEND":
        print("\nAPI indicates to resend the request. Retrying...")
        response = requests.get(url, params=params)  # Re-request the code
        time.sleep(interval)
        elapsed += interval

      else:
        print(f"\nUnexpected API status: {status}")
        return None

    print("\nTimeout reached. No new SMS code received.")
    return None

  except Exception as e:
    print(f"An error occurred: {e}")
    return None


def send_signup_sms_code(
  headers, family_id, device_id, android_id, phone_number, water, proxies=proxies, retries=5, wait_time=300
):
  data = {
    "signed_body": f'SIGNATURE.{{"phone_id":"{family_id}","phone_number":"{phone_number}","guid":"{device_id}","device_id":"{android_id}","android_build_type":"release","waterfall_id":"{water}"}}'
  }

  for attempt in range(retries):
    try:
      response = requests.post(
        "https://i.instagram.com/api/v1/accounts/send_signup_sms_code/", headers=headers, data=data, proxies=proxies
      )

      # If request is successful, print the response and return it
      print(response.text)
      return response
    except SSLError as e:
      # If SSLError occurs, print the error and wait for some time before retrying
      print(f"SSLError occurred: {e}. Retrying in {wait_time} seconds...")
      time.sleep(wait_time)  # Wait for 2 minutes (120 seconds) before retrying
    except requests.exceptions.RequestException as e:
      # Handle other request-related exceptions
      print(f"Request exception occurred: {e}. Retrying in {wait_time} seconds...")
      time.sleep(wait_time)

  print("Max retries exceeded. Could not complete the request.")
  return None


def validate_signup_sms_code(
  headers, phone_number, device_id, android_id, code, water, proxies=proxies, retries=5, wait_time=300
):
  data = {
    "signed_body": f'SIGNATURE.{{"verification_code":"{code}","phone_number":"{phone_number}","guid":"{device_id}","device_id":"{android_id}","waterfall_id":"{water}"}}'
  }

  for attempt in range(retries):
    try:
      response = requests.post(
        "https://i.instagram.com/api/v1/accounts/validate_signup_sms_code/", headers=headers, data=data, proxies=proxies
      )

      # If request is successful, print the response and return it
      print(response.text)
      return response
    except SSLError as e:
      # If SSLError occurs, print the error and wait for some time before retrying
      print(f"SSLError occurred: {e}. Retrying in {wait_time} seconds...")
      time.sleep(wait_time)  # Wait for 2 minutes (120 seconds) before retrying
    except requests.exceptions.RequestException as e:
      # Handle other request-related exceptions
      print(f"Request exception occurred: {e}. Retrying in {wait_time} seconds...")
      time.sleep(wait_time)

  print("Max retries exceeded. Could not complete the request.")
  return None


def suggest_username(
  headers, family_id, device_id, android_id, username, water, proxies=proxies, retries=5, wait_time=300
):
  data = {
    "signed_body": f'SIGNATURE.{{"phone_id":"{family_id}","guid":"{device_id}","name":"{username}","device_id":"{android_id}","email":"","waterfall_id":"{water}"}}'
  }

  for attempt in range(retries):
    try:
      response = requests.post(
        "https://i.instagram.com/api/v1/accounts/username_suggestions/", headers=headers, data=data, proxies=proxies
      )

      # If the request is successful, parse the response for suggestions
      suggestions = response.json().get("suggestions_with_metadata", {}).get("suggestions", [])
      if suggestions:
        usernam = suggestions[0]["username"]
        print(f"Suggested Username: {usernam}")
        return usernam
      else:
        print("No suggestions available.")
        return None

    except SSLError as e:
      # If SSLError occurs, print the error and wait for some time before retrying
      print(f"SSLError occurred: {e}. Retrying in {wait_time} seconds...")
      time.sleep(wait_time)  # Wait for 2 minutes (120 seconds) before retrying
    except requests.exceptions.RequestException as e:
      # Handle other request-related exceptions
      print(f"Request exception occurred: {e}. Retrying in {wait_time} seconds...")
      time.sleep(wait_time)

  print("Max retries exceeded. Could not complete the request.")
  return None


def create_account(
  headers,
  family_id,
  device_id,
  android_id,
  password,
  birth,
  phone_number,
  code,
  jazoest,
  adid,
  water,
  usernam,
  activation_id,
  proxies=proxies,
):
  timpp = int(datetime.now().timestamp())
  data = {
    "signed_body": 'SIGNATURE.{"is_secondary_account_creation":"false","jazoest":"'
    + jazoest
    + '","tos_version":"row","suggestedUsername":"","verification_code":"'
    + str(code)
    + '","sn_result":"API_ERROR: class X.2mY:7: ","do_not_auto_login_if_credentials_match":"false","phone_id":"'
    + family_id
    + '","enc_password":"#PWD_INSTAGRAM:0:'
    + str(timpp)
    + ":"
    + password
    + '","phone_number":"'
    + str(phone_number)
    + '","username":"'
    + str(usernam)
    + '","first_name":"'
    + random_first_name
    + '","day":"'
    + birth[0]
    + '","adid":"'
    + adid
    + '","guid":"'
    + device_id
    + '","year":"'
    + birth[1]
    + '","device_id":"'
    + android_id
    + '","_uuid":"'
    + device_id
    + '","month":"'
    + birth[2]
    + '","sn_nonce":"","force_sign_up_code":"","waterfall_id":"'
    + water
    + '","qs_stamp":"","has_sms_consent":"true","one_tap_opt_in":"true"}',
  }
  try:
    response = requests.post(
      "https://i.instagram.com/api/v1/accounts/create_validated/", headers=headers, data=data, proxies=proxies
    )
    # print("DEBUG: Response from Instagram API:", response.text)

    if response.status_code == 200:
      response_json = response.json()
      if response_json.get("account_created", False):
        created_user = response_json.get("created_user", {})
        created_username = created_user.get("username", "").lower()
        if created_username == "instagram user":
          print(
            f"INFO: Username '{usernam}' is locked or invalid. Waiting for 2 minute before processing next account."
          )
          for remaining in range(0, 0, -1):
            print(f"Waiting... {remaining} seconds remaining", end="\r")
            time.sleep(1)

          print("\nINFO: Proceeding to the next account.")

          time.sleep(60)  # Wait for 1 minute before processing another account
          return False
        if usernam.lower() != "instagram user":
          print(f"DEBUG: Account successfully created for {usernam}. Details saved.")
          editacc(activation_id, usernam, password, phone_number)
          return True
        else:
          print(f"INFO: Username '{usernam}' is locked or invalid. Skipping save.")
      elif "error_type" in response_json:
        error_type = response_json["error_type"]
        error_message = response_json.get("message", "Unknown error")
        print(f"ERROR: Account creation failed for {usernam}. Reason: {error_message}")
      else:
        print(f"ERROR: Unexpected response for {usernam}. Response: {response_json}")
    else:
      print(f"ERROR: Account creation failed. Status code: {response.status_code}, Message: {response.text}")

  except requests.exceptions.RequestException as e:
    print(f"ERROR: Request failed. Details: {e}")

  return False  # Indicates failure


def editacc(activation_id, usernam, password, phone_number):
  try:
    username = usernam
    password = password
    phone = phone_number

    output_csv = "newacc.csv"
    new_picture_path = select_random_image()

    names = load_names()
    if not names:
      print("No names found in names.txt. Please add some names to the file.")
    new_full_name = random.choice(names)

    # Set the proxy for the session
    cl = Client()

    # Define the custom challenge resolve logic
    def custom_challenge_resolve_simple(self, challenge_url: str) -> bool:
      step_name = self.last_json.get("step_name", "")
      if step_name in ("verify_email", "verify_email_code", "select_verify_method"):
        if step_name == "select_verify_method":
          steps = self.last_json["step_data"].keys()
          phone_number = self.last_json["step_data"].get("phone_number", "N/A")
          email = self.last_json["step_data"].get("email", "N/A")
          print("Challenged Code Required")
          print(f"0: {phone_number}")
          print(f"1: {email}")
          while True:
            choice = "0"
            if choice in ["0", "1"]:
              break

          if choice == "0":
            self._send_private_request(challenge_url[1:], {"choice": ChallengeChoice.SMS})
          else:
            self._send_private_request(challenge_url[1:], {"choice": ChallengeChoice.EMAIL})

        wait_seconds = 5
        for attempt in range(24):
          # Prompt the user to enter the code
          code = self.custom_manual_input_code(self.username, "SMS" if choice == "0" else "EMAIL")
          if code:
            break
          time.sleep(wait_seconds)

        challenge_url = challenge_url[1:]
        self._send_private_request(challenge_url, {"security_code": code})
        self._send_private_request(challenge_url, {"security_code": code})

        assert self.last_json.get("action", "") == "close"
        assert self.last_json.get("status", "") == "ok"
        return True

      elif step_name == "delta_login_review" or step_name == "scraping_warning":
        self._send_private_request(challenge_url, {"choice": "0"})
        return True

      return False

    def custom_manual_input_code(self, username: str, choice=None):
      code = request_new_sms_code_and_wait(activation_id)
      return code

    cl.challenge_resolve_simple = custom_challenge_resolve_simple.__get__(cl, Client)
    cl.custom_manual_input_code = custom_manual_input_code.__get__(cl, Client)
    cl.set_proxy(selected_proxy)
    print(selected_proxy)
    try:
      # Log in with provided credentials
      cl.login(username, password)
      session_filename = f"sessions/{username}_session.json"
      cl.dump_settings(session_filename)
      logging.info(f"Login successful for {username}.")
      cl.account_edit(full_name=new_full_name)
      logging.info(f"Updated name for {username} to {new_full_name}.")
      cl.account_change_picture(new_picture_path)
      logging.info(f"Updated profile picture for {username}.")
      logging.info(f"Generating TOTP seed for {username}")
      seed = cl.totp_generate_seed() if cl.totp_generate_seed() else None

      if seed:
        print(f"\nTOTP Seed (Save this securely!): {seed}")
        # Generate the TOTP code using the generated seed
        code = cl.totp_generate_code(seed)
        print(f"TOTP Code: {code}")
      # Generate the TOTP code using the generated seed
      code = cl.totp_generate_code(seed)
      print(f"TOTP Code: {code}")
      # Enable 2FA using the generated code
      backup_keys = cl.totp_enable(code)
      print("\nBackup Keys (Save these safely):")
      for key in backup_keys:
        print(key)

      # Log out after processing the account
      try:
        cl.logout()
        logging.info(f"Logged out successfully for {username}.")
      except Exception as e:
        logging.error(f"Error logging out for {username}: {e}")

    except Exception as e:
      logging.error(f"Unexpected error during processing for {username}: {e}")

    processed_account = {
      "username": username,
      "password": password,
      "authfa": seed if seed else None,
    }

    # Write processed account to the output CSV
    write_account_to_csv([processed_account], output_csv)

  except Exception as e:
    logging.error(f"Failed to process the account: {e}")
    exit()


def worker(queue, num_accounts):
  while not queue.empty():
    try:
      i = queue.get()
      ip = check_ip()
      print(f"\nCreating account {i + 1} of {num_accounts} using IP {ip}")

      # Generate necessary identifiers
      Device_ID = generate_uuid()
      Family_ID = generate_uuid()
      Android_ID = generate_android_device_id()
      UserAgent = generate_useragent()
      adid = generate_uuid()
      water = generate_uuid()
      birth = Birthday()
      password = "Test@9988"
      username = Username()
      jazoest = generate_jazoest(Family_ID)

      headers = {
        "User-Agent": UserAgent,
        "X-Mid": "dummy_mid_value",
        "Family-ID": Family_ID,
        "Device-ID": Device_ID,
        "Android-ID": Android_ID,
      }

      activation_id, phone_number = request_activation(service="ig", country=country, max_price=0.2)
      if not activation_id:
        print("Failed to acquire a phone number. Skipping account creation.")
        queue.task_done()
        continue

      send_signup_sms_code(headers, Family_ID, Device_ID, Android_ID, phone_number, water)
      code = wait_for_sms(activation_id)
      if not code:
        print("Failed to receive SMS code. Skipping account creation.")
        queue.task_done()
        continue

      if not validate_signup_sms_code(headers, phone_number, Device_ID, Android_ID, code, water):
        print("Failed to validate SMS code. Skipping account creation.")
        queue.task_done()
        continue

      usernam = suggest_username(headers, Family_ID, Device_ID, Android_ID, username, water)
      if not usernam:
        print("Failed to get a valid username. Skipping account creation.")
        queue.task_done()
        continue

      if create_account(
        headers,
        Family_ID,
        Device_ID,
        Android_ID,
        password,
        birth,
        phone_number,
        code,
        jazoest,
        adid,
        water,
        usernam,
        activation_id,
      ):
        print(f"Account {i + 1} created successfully!")
      else:
        print(f"Failed to create the account for username {usernam}. Skipping to the next.")
    except Exception as e:
      print(f"Unexpected error during account creation: {e}")
    finally:
      queue.task_done()  # Mark the task as done


def main():
  try:
    with open("names.txt", "r") as file:
      names = [line.strip() for line in file if line.strip()]
  except FileNotFoundError:
    print("Error: 'names.txt' file not found.")
    return

  if not names:
    print("Error: 'names.txt' file is empty.")
    return

  try:
    num_accounts = int(input("How many accounts do you want to create? "))
    num_threads = int(input("How many threads do you want to use? "))
  except ValueError:
    print("Invalid number entered. Please enter a valid integer.")
    return

  queue = Queue()
  for i in range(num_accounts):
    queue.put(i)

  threads = []
  for _ in range(num_threads):
    thread = threading.Thread(target=worker, args=(queue, num_accounts))
    threads.append(thread)
    thread.start()

  for thread in threads:
    thread.join()

  print("\nAll account creation tasks completed.")


if __name__ == "__main__":
  main()
