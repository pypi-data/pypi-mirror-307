#!/usr/bin/env python3
# Author: Arturo 'Buanzo' Busleiman - October 2020
import argparse
import os
import subprocess
from pathlib import Path

from pythonping import ping
from sshconf import read_ssh_config

__version__ = '0.1.4'
SSH_PING_PATH = '/usr/local/bin/sshping'


class SSHPing:
    def __init__(self, target=None, count=4, verbose=False, timeout=10):
        self.target = target
        config_path = Path('~/.ssh/config').expanduser()
        if config_path.exists() and target:
            config = read_ssh_config(config_path)
            try:
                self.target = config.host(target)['hostname']
            except KeyError:
                pass
        self.count = count
        self.verbose = verbose
        self.timeout = timeout

    def ping(self):
        try:
            # Attempt pythonping first
            return ping(self.target, timeout=self.timeout, verbose=self.verbose, count=self.count)
        except PermissionError:
            print("RAW socket access denied. Attempting system ping command as fallback...")
            return self.system_ping()

    def system_ping(self):
        try:
            # Use system's ping command and print output in real-time
            command = ['ping', '-c', str(self.count), '-W', str(self.timeout), self.target]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
            for line in process.stdout:
                print(line, end='')  # Print each line as it comes in
            process.wait()  # Wait for the process to complete
            if process.returncode != 0:
                return f"System ping failed with exit code {process.returncode}"
            return ""  # Return empty string on success as output is already printed
        except subprocess.CalledProcessError as e:
            return f"System ping failed: {e}"

    @staticmethod
    def test_permissions():
        issues = []

        # Check setuid bit
        if os.geteuid() != 0:
            issues.append(f"Setuid bit is not enabled. To enable it, run:\n"
                          f"sudo chmod u+s {SSH_PING_PATH}")

        # Check cap_net_raw capability
        try:
            cap_check = subprocess.run(['getcap', SSH_PING_PATH], capture_output=True, text=True)
            if 'cap_net_raw+ep' not in cap_check.stdout:
                issues.append(f"cap_net_raw capability is not set. To set it, run:\n"
                              f"sudo setcap cap_net_raw+ep {SSH_PING_PATH}")
        except FileNotFoundError:
            issues.append("Capability check failed: 'getcap' command not found. Install 'libcap2-bin' package.")

        # Explain fallback mechanism if any issues exist
        if issues:
            print("\n".join(issues))
            print("\nFallback mechanism explanation: If raw socket permissions are unavailable, sshping will attempt "
                  "to use the system ping command as a fallback. This avoids the need for elevated privileges but "
                  "requires the system ping command to be installed and accessible.")
        else:
            print("All necessary permissions and capabilities are set. You are ready to use sshping.")


def run():
    parser = argparse.ArgumentParser(description="""Simple command line tool that lets you ping hosts that are only defined in your ssh config""")
    parser.add_argument('target', metavar="HOST", nargs='?', help="Name of host to ping")
    parser.add_argument('-c', '--count', default=4, type=int, help="How many times to attempt the ping, 4 by default")
    parser.add_argument('-t', '--timeout', default=10, type=int, help="Time in seconds before considering each non-arrived reply permanently lost")
    parser.add_argument('-v', '--verbose', action='store_true', help="Be verbose")
    parser.add_argument('--test', action='store_true', help="Check for setuid and raw socket capabilities required for sshping")

    parsed = parser.parse_args()

    if parsed.test:
        SSHPing.test_permissions()
    elif parsed.target:
        sshping = SSHPing(target=parsed.target, count=parsed.count, verbose=parsed.verbose, timeout=parsed.timeout)
        print(sshping.ping())
    else:
        print("Error: Please provide a target to ping or use the --test option to check permissions.")


if __name__ == '__main__':
    run()
