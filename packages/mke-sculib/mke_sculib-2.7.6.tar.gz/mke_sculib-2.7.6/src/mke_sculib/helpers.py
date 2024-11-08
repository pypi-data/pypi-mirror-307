import dateutil.parser, datetime, time, re



class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BLACK = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

colors_dc = {
    'header': colors.HEADER,
    'blue': colors.OKBLUE,
    'green': colors.OKGREEN,
    'warn': colors.WARNING,
    'red': colors.FAIL,
    'black': colors.BLACK,
    'bold': colors.BOLD,
    'underline': colors.UNDERLINE
}
    
def print_color(msg, color='red'):
    if isinstance(color, str):
        color = colors_dc[color]
    print(f"{color}{msg}{colors.BLACK}")


def get_utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

def make_zulustr(dtobj, remove_ms = True):
    utc = dtobj.replace(tzinfo=datetime.timezone.utc)
    if remove_ms:
        utc = utc.replace(microsecond=0)
    return utc.isoformat().replace('+00:00','') + 'Z'

def mk_dtz(dtobj=None, remove_ms = True):
    if dtobj is None:
        dtobj = get_utcnow()
    return make_zulustr(dtobj, remove_ms).replace('T',' ').replace('Z',' ')

def match_zulutime(s):
    if s is None: return None

    s = s.strip()
    if '.' in s and re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{1,6}Z', s) is not None:
        return s
    elif 'T' in s and re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', s) is not None:
        return s
    elif re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}Z', s) is not None:
        return s
    else:
        return None


def parse_zulutime(s):
    try:
        if re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}Z', s) is not None:
            s = s[:-1] + 'T00:00:00Z'
        return dateutil.parser.isoparse(s).replace(tzinfo=datetime.timezone.utc)
    except Exception:
        return None
    
def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter



def get_ntp_time_with_socket(ntp_server_address):
    """Retrieves the current time from an NTP server using socket programming.

    Args:
        ntp_server_address: The IP address of the NTP server.

    Returns:
        A tuple containing the current time as a Unix timestamp and a human-readable string.
    """
    
    import socket
    import struct
    import time

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(b'\x1b' + 47 * b'\0', (ntp_server_address, 123))
    message, address = client.recvfrom(1024)
    
    # Unpack the received message
    t = struct.unpack('!12I', message)[10]
    t -= 2208988800  # Convert NTP time to Unix time

    # Convert Unix timestamp to datetime object in UTC
    dt_utc = datetime.datetime.utcfromtimestamp(t)

    # Format the datetime object in ISO 8601 format
    human_time_iso = make_zulustr(dt_utc, remove_ms=False)

    return human_time_iso
