from flask.ext.wtf import regexp


USERNAME_RE = r'^[\w.+-]+$'

is_username = regexp(USERNAME_RE, 
                     message="You can only use letters, numbers or dashes")