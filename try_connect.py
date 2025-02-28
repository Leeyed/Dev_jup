'''
Author: LiuSheng
Date: 2025-01-21 15:44:04
LastEditTime: 2025-02-07 09:56:27
Description: 
'''
import subprocess
import time

def run_command_until_success():
    while True:
        print("Running slookup...")
        slookup_result = subprocess.run(
            ['nslookup', 'baidu.com'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if "REFUSED" not in slookup_result.stdout and "unexpected source" not in slookup_result.stdout:
            print("slookup returned expected result:")
            print(slookup_result.stdout)
        else:
            print("slookup failed. Retrying...")
            time.sleep(0.2) # Retry delay in seconds.

            # Check for ping issues as well
            print("Running ping...")
            
if __name__ == '__main__':
    run_command_until_success()