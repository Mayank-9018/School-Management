import base64

def validate(username,password):
    """Recieve Password and validate it with the stored password.

    Args:
        username (string): The Username entered by the user
        password (string): The Password entered by the user

    Returns:
        boolean: Returns True if Credentials are correct else returns False
    """
    with open('setting.management','r') as fhand:
        user = base64.b64decode(bytes(fhand.readline(),'utf-8')).decode()
        passw = base64.b64decode(bytes(fhand.readline(),'utf-8')).decode()
    if user==username.strip() and passw==password:
        return True
    else:
        return False