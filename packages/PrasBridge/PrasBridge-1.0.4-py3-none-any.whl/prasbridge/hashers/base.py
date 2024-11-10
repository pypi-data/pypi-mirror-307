import secrets
import uuid
import hashlib
import time
import string
from datetime import datetime
import random
import re

def make_token(length=32, numb=True, lower=True, upper=True):
    """
    Generate a customizable token with options for characters.

    Parameters:
    - length (int): Desired length of the token (default: 32).
    - numb (bool): Whether to include numbers (default: True).
    - lower (bool): Whether to include lowercase letters (default: True).
    - upper (bool): Whether to include uppercase letters (default: True).

    Returns:
    - str: A secure token.
    """
    
    # Initialize the character pool based on user preferences
    characters = ''
    if lower:
        characters += string.ascii_lowercase 
    if upper:
        characters += string.ascii_uppercase 
    if numb:
        characters += string.digits           
 
    if not characters:
        raise ValueError("At least one character type must be enabled")

    # Generate a random hex string using secrets
    token_part = secrets.token_hex(length // 2)

    # Generate a random UUID
    uuid_part = str(uuid.uuid4()).replace('-', '')

    # Add a custom mix with a timestamp hash for uniqueness
    timestamp = str(time.time()).encode('utf-8')
    hash_part = hashlib.sha256(timestamp).hexdigest()[:16]

    # Combine all parts to create the initial code
    code = f"{token_part}{uuid_part}{hash_part}"

    # generate a new token with character preferences
    if characters:
        code = ''.join(secrets.choice(characters) for _ in range(length))
    
    return code[:length]



def __generate_random_string(length=10, separator='-', spchar=False):
    """Generate a random string with a defined length, separated every 5 characters."""
    random_string = ''
    if spchar:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    else:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return separator.join([random_string[i:i+5] for i in range(0, len(random_string), 5)])

def __get_datetime(fmt="%Y%m%d-%H%M%S"):
    """Get the current datetime in a specified format."""
    return datetime.now().strftime(fmt)

def __get_timestamp_ms():
    """Get the current timestamp in milliseconds."""
    return str(int(datetime.now().timestamp() * 1000))

def slugify(title, rand=False, rand_len=10, dt=False, ms=False, structure='title-rand', sep='-', case=False, spchar=False):
    """
    Generate a customizable slug.
    
    Parameters:
    - title (str): The base string to convert to a slug.
    - rand (bool): Append a random string to the slug (default False).
    - rand_len (int): Length of the random string to add (default 10 characters).
    - dt (bool): Include current date-time in the slug (default False).
    - ms (bool): Include current timestamp with milliseconds (default False).
    - structure (str): Define the slug structure using 'title', 'rand', 'dt', and 'ms' (default 'title-rand').
    - sep (str): Separator to use between different slug parts (default '-').
    - case (bool): If True, preserve the original case, otherwise convert to lowercase (default False).
    - spchar (bool): If True, include special characters in the random string and don't remove them from the title (default False).
    Returns:
    - str: The generated slug based on the specified structure.
    """
    if not title:
        raise ValueError("Title must be provided to generate a slug.")
    
    if not spchar:
        title = re.sub(r'[^\w\s]', '', title)
    
    slug_parts = {}
    slug_parts['title'] = title.replace(' ', sep) if case else title.lower().replace(' ', sep)

    if rand:
        structure = structure+'-rand' if not 'rand' in structure else structure
        slug_parts['rand'] = __generate_random_string(length=rand_len, separator=sep, spchar=spchar)
    
    if dt:
        structure = structure+'-dt' if not 'dt' in structure else structure
        slug_parts['dt'] = __get_datetime().replace('-', sep)
    
    if ms:
        structure = structure+'-ms' if not 'ms' in structure else structure 
        slug_parts['ms'] = __get_timestamp_ms()

    # Build the slug according to the provided structure
    slug_structure = structure.split('-')
    slug = sep.join([slug_parts[part] for part in slug_structure if part in slug_parts])
    if len(slug) <= 0:
        slug = slug_parts['title']
    return slug
