from ratelimit import limits, sleep_and_retry
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import re
import os
import time
from collections import defaultdict

PEPPER = "jdafhpoahsofdashjp"
ONE_MINUTE = 60 * 10
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_TIME = 10 * 60  # Time for lockout if the max number of attemot is exceeded (in seconds)

# in memory storage for number of failed attempts
failed_attempts = defaultdict(list)  # Login Tracks failed attempts for email, token, and IP
bisHash_attempts = defaultdict(list)

# Custom Password Hasher
ph = PasswordHasher(
    time_cost=8,  # Number of iterations
    memory_cost=2**16,  # Memory cost
    parallelism=1,  # Number of parallel threads
    hash_len=64,  # Length of the resulting hash
    salt_len=16 # length of salt
)

def is_strong_password(password):
    """Check if password is Strong."""
    if len(password) < 12:
        return False, "Password must be at least 12 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."
    return True, "Password is strong."



def bis_hash(ip, identifier, password):
    current_time = time.time()
    
    # Clear out outdated attempts
    bisHash_attempts[ip] = [timestamp for timestamp in bisHash_attempts[identifier] if current_time - timestamp < ONE_MINUTE]

    if len(bisHash_attempts[ip]) >= 5:  # Maximum 5 attempts per identifier per minute
        raise Exception("Too many sign-up attempts. Please try again later.")
    
    # Log this attempt
    bisHash_attempts[ip].append(current_time)
    
    # Perform the hash
    combined_input = identifier + password + PEPPER
    return ph.hash(combined_input)


def track_failed_attempt(identifier):
    """Track failed login attempts for rate limiting and lockout"""
    current_time = time.time()
    failed_attempts[identifier].append(current_time)
    # Remove old failed attempts (outside the lockout period)
    failed_attempts[identifier] = [timestamp for timestamp in failed_attempts[identifier] if current_time - timestamp < LOCKOUT_TIME]

def check_account_lock(identifier):
    """Check if the account should be locked"""
    if len(failed_attempts[identifier]) >= MAX_FAILED_ATTEMPTS:
        return True  # Account is locked
    return False

def verify_password(stored_hash, identifier, entered_password):
    """Verify if the entered password matches the stored hashed password"""
    if check_account_lock(identifier):
        return False  # Account is locked, reject the login attempt

    combined_input = identifier + entered_password + PEPPER
    try:
        ph.verify(stored_hash, combined_input)
        return True
    except VerifyMismatchError:
        track_failed_attempt(identifier)
        return False