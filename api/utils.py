import os
import errno

def decode_values(redis_values):
    return {k.decode('utf-8'): v.decode('utf-8') for k, v in redis_values.items()}

def makedirs_ignore(path, mode):
    """
    Creates the given directory (and any parents), but succeeds if it already
    exists.
    """
    try:
        os.makedirs(path, mode)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def extract_arg(arg, kernel_options):
    """
    Returns a tuple of (<arg> value, rest of kernel options). If there was
    no <arg>, the result will be (None, untouched kernel options).
    """
    value = None
    tokens = []
    for token in kernel_options.split():
        if token.startswith(arg):
            value = token[len(arg):]
        else:
            tokens.append(token)
    if value:
        return (value, ' '.join(tokens))
    else:
        return (None, kernel_options)

def ip_to_hex(ipaddr):
    return '%02X%02X%02X%02X' % tuple(int(octet) for octet in ipaddr.split('.'))
