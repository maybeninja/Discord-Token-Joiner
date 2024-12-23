import threading
from colorama import init, Fore
init(autoreset=True)


class Logger: 
    def Success(text,obj=None):
    
        lock = threading.Lock()
        lock.acquire()
        print(f'{Fore.LIGHTGREEN_EX}Success >  {Fore.LIGHTMAGENTA_EX}{text} -> {Fore.LIGHTCYAN_EX}{obj}')
        lock.release()

    def Error(text,obj=None):
       
        lock = threading.Lock()
        lock.acquire()
        print(f'{Fore.LIGHTRED_EX}Error >  {Fore.LIGHTMAGENTA_EX}{text} -> {Fore.LIGHTCYAN_EX}{obj}')
        lock.release()

    def Info(text,obj=None):
        
        lock = threading.Lock()
        lock.acquire()
        print(f'{Fore.LIGHTYELLOW_EX}Warn >  {Fore.LIGHTMAGENTA_EX}{text} -> {Fore.LIGHTCYAN_EX}{obj}')
        lock.release()