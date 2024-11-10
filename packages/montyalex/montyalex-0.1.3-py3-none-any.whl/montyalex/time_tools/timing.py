import concurrent.futures
import time
import sys

from montyalex.us_tools import SETTINGS

TIMEOUT = '1min'
if SETTINGS.get_value('default.opt.timeout'):
    TIMEOUT = SETTINGS.get_value('default.opt.timeout')
MINUTE = False
SECONDS = False

if isinstance(TIMEOUT, str):
    if 'min' in TIMEOUT:
        MINUTE = True
        TIMEOUT = int(TIMEOUT.removesuffix('min')) * 60
if isinstance(TIMEOUT, str):
    if 'sec' in TIMEOUT:
        SECONDS = True
        TIMEOUT = int(TIMEOUT.removesuffix('sec'))

def func_time(message: str = None):
    def decorator(func):
        func_name = f'"{func.__name__}({func.__type_params__})"'
        def wrapper(*args, **kwargs):
            local_message = message if message is not None else 'completed in approximately'

            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    result = future.result(timeout=TIMEOUT)
                    elapsed_time = time.time() - start_time

                    if local_message and '+' in local_message:
                        func_msg_1, func_msg_2 = [
                            part.strip()
                            for part in local_message.split('+', maxsplit=1)]
                        print(f'{func_name}: {func_msg_1} {elapsed_time:.3f} seconds {func_msg_2}')
                    elif local_message and ';' in local_message:
                        func_msg_1, func_msg_2 = [
                            part.strip()
                            for part in local_message.split(';', maxsplit=1)]
                        print(f'{func_name}: {func_msg_1} {elapsed_time:.3f} seconds {func_msg_2}')
                    else:
                        print(f'{func_name}: {local_message} {elapsed_time:.3f} seconds')

                    return result

                except concurrent.futures.TimeoutError:
                    print(f"Function {func_name} exceeded {TIMEOUT} seconds. Cancelling...")
                    sys.exit("Cancelled due to timeout")
        return wrapper
    return decorator

# ---------------------------------------------------------------------------
# | Example Usage
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    @func_time(message='completed in')
    def short_running_action():
        time.sleep(2)
        print("SHORT Action completed")

    @func_time(message='took + to complete')
    def long_running_action():
        time.sleep(4)
        print("LONG Action completed")

    @func_time(message='took; to complete!')
    def longer_running_action():
        time.sleep(8)
        print("LONGER Action completed")

    @func_time()
    def longest_running_action():
        time.sleep(16)
        print("LONGEST Action completed")

    short_running_action()
    long_running_action()
    longer_running_action()
    longest_running_action()
