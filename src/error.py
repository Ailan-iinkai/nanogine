from pathlib import Path
import sys
from datetime import datetime
from urllib.parse import urlparse
from dataclasses import dataclass
from bs4.element import Tag

def err(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("error.log", "a") as f:
                sys.stderr = f
                print(f"{now}", file=sys.stderr)

    return wrapper

def domain_exists(func):
    def wrapper(*args, **kwargs):
        url = args[0]  
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        try:
            import socket
            socket.gethostbyname(domain)
            print(f"{domain} は存在します。")
            return func(*args, **kwargs)
        except socket.gaierror:
            print(f"{domain} は存在しません。")
            return None 

    return wrapper

@dataclass
class ErrLog():
    message: str
    file: Path
    detail: dict
    
    def save(self):
        detail = ''.join(f"\n\t{k}: {v}" for k,v in self.detail.items())
        err_msg = f"""[Error]: {self.message} {detail}\n\n"""
        print(err_msg, file=sys.stderr)
        with open(self.file/"error.log", "a") as f:
            f.write(f"{datetime.now()}=================================================\n\n")
            f.write(err_msg)
            f.write("\n\n")
            
    

def log(message:str,detail:dict={}):
    cache_dir = Path(__file__).parent.parent / "cache/"
    ErrLog(message,cache_dir,detail).save()

def can_findall(content) -> bool:
    """find()が"NavigableString | None"で帰ってきたときfind_all()がメソッドにないため、Tag以外の型が帰ってきたらfalse
    """
    if isinstance(content,Tag):
        return True
    else: 
        return False