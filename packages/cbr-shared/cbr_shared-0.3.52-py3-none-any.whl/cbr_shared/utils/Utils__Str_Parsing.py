def split__user_name_into_first_and_last_names(user_name: str):  # Split a user-name into first and last names, returning them as a tuple
    first_name = ''                                              # Initialize first_name as an empty string
    last_name  = ''                                              # Initialize last_name as an empty string
    if user_name:                                                # Proceed only if guest_name is not None or empty
        guest_name = user_name.strip('_ ').replace('_', ' ')     # Strip leading/trailing underscores and spaces, then replace remaining underscores with spaces
        parts = guest_name.split()                               # Split the cleaned name into words based on spaces
        if parts:                                                # Check if the parts list is not empty
            first_name = parts[0]                                # Assign the first part as first_name
            last_name = ' '.join(parts[1:])                      # Combine the remaining parts into last_name, separated by spaces
    return first_name, last_name                                 # Return the first_name and last_name as a tuple