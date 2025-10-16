"""Quick action utilities for Prometheus terminal assistant."""

import hashlib
import base64
import pyqrcode
import io
from datetime import datetime
import pytz
from typing import Optional
from rich.console import Console
from rich.panel import Panel

console = Console()


def shorten_url(url: str) -> str:
    """
    Shorten a URL using a simple hash-based approach.
    For production, integrate with a URL shortening service.
    """
    # Create a simple hash-based short code
    hash_obj = hashlib.md5(url.encode())
    short_code = hash_obj.hexdigest()[:8]
    
    # In a real implementation, this would save to a database
    console.print(Panel(
        f"[bright_white]Original URL:[/bright_white]\n{url}\n\n"
        f"[bright_white]Short code:[/bright_white] {short_code}\n\n"
        f"[dim]Note: In production, this would generate a full short URL[/dim]",
        border_style="bright_cyan",
        title="[bold bright_cyan]🔗 URL Shortener[/bold bright_cyan]",
        title_align="left"
    ))
    return short_code


def generate_qr_code(text: str, output_file: Optional[str] = None) -> None:
    """Generate QR code for given text."""
    try:
        qr = pyqrcode.create(text)
        
        if output_file:
            qr.png(output_file, scale=8)
            console.print(f"[green]✓ QR code saved to {output_file}[/green]")
        else:
            # Display as ASCII art in terminal
            console.print(Panel(
                qr.terminal(quiet_zone=1),
                border_style="bright_cyan",
                title="[bold bright_cyan]📱 QR Code[/bold bright_cyan]",
                title_align="left"
            ))
            console.print(f"[dim]Text: {text}[/dim]")
    except Exception as e:
        console.print(f"[red]Error generating QR code: {e}[/red]")


def generate_hash(text: str, algorithm: str = "all") -> None:
    """Generate cryptographic hash of text."""
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    
    output = []
    
    if algorithm == "all":
        for name, func in algorithms.items():
            hash_value = func(text.encode()).hexdigest()
            output.append(f"[cyan]{name.upper()}:[/cyan] {hash_value}")
    elif algorithm in algorithms:
        hash_value = algorithms[algorithm](text.encode()).hexdigest()
        output.append(f"[cyan]{algorithm.upper()}:[/cyan] {hash_value}")
    else:
        console.print(f"[red]Unknown algorithm: {algorithm}[/red]")
        return
    
    console.print(Panel(
        "\n".join(output),
        border_style="bright_cyan",
        title="[bold bright_cyan]🔐 Hash Generator[/bold bright_cyan]",
        title_align="left"
    ))


def encode_text(text: str, encoding: str = "base64") -> None:
    """Encode text using various encoding schemes."""
    encodings = {
        'base64': lambda t: base64.b64encode(t.encode()).decode(),
        'base32': lambda t: base64.b32encode(t.encode()).decode(),
        'base16': lambda t: base64.b16encode(t.encode()).decode(),
        'hex': lambda t: t.encode().hex(),
        'url': lambda t: __import__('urllib.parse').quote(t),
    }
    
    if encoding in encodings:
        try:
            encoded = encodings[encoding](text)
            console.print(Panel(
                f"[bright_white]Original:[/bright_white]\n{text}\n\n"
                f"[bright_white]Encoded ({encoding}):[/bright_white]\n{encoded}",
                border_style="bright_cyan",
                title="[bold bright_cyan]🔤 Text Encoder[/bold bright_cyan]",
                title_align="left"
            ))
        except Exception as e:
            console.print(f"[red]Encoding error: {e}[/red]")
    else:
        console.print(f"[red]Unknown encoding: {encoding}[/red]")
        console.print(f"[dim]Available: {', '.join(encodings.keys())}[/dim]")


def decode_text(text: str, encoding: str = "base64") -> None:
    """Decode text using various encoding schemes."""
    decodings = {
        'base64': lambda t: base64.b64decode(t).decode(),
        'base32': lambda t: base64.b32decode(t).decode(),
        'base16': lambda t: base64.b16decode(t).decode(),
        'hex': lambda t: bytes.fromhex(t).decode(),
        'url': lambda t: __import__('urllib.parse').unquote(t),
    }
    
    if encoding in decodings:
        try:
            decoded = decodings[encoding](text)
            console.print(Panel(
                f"[bright_white]Encoded ({encoding}):[/bright_white]\n{text}\n\n"
                f"[bright_white]Decoded:[/bright_white]\n{decoded}",
                border_style="bright_cyan",
                title="[bold bright_cyan]🔓 Text Decoder[/bold bright_cyan]",
                title_align="left"
            ))
        except Exception as e:
            console.print(f"[red]Decoding error: {e}[/red]")
    else:
        console.print(f"[red]Unknown encoding: {encoding}[/red]")
        console.print(f"[dim]Available: {', '.join(decodings.keys())}[/dim]")


def world_time(location: str = "UTC") -> None:
    """Show current time in different timezones."""
    # Common timezone mappings
    timezone_map = {
        'utc': 'UTC',
        'new york': 'America/New_York',
        'los angeles': 'America/Los_Angeles',
        'london': 'Europe/London',
        'paris': 'Europe/Paris',
        'tokyo': 'Asia/Tokyo',
        'sydney': 'Australia/Sydney',
        'dubai': 'Asia/Dubai',
        'mumbai': 'Asia/Kolkata',
        'beijing': 'Asia/Shanghai',
    }
    
    location_lower = location.lower()
    timezone_str = timezone_map.get(location_lower, location)
    
    try:
        tz = pytz.timezone(timezone_str)
        current_time = datetime.now(tz)
        
        console.print(Panel(
            f"[bright_white]Location:[/bright_white] {location}\n"
            f"[bright_white]Timezone:[/bright_white] {timezone_str}\n\n"
            f"[bold bright_cyan]{current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}[/bold bright_cyan]",
            border_style="bright_cyan",
            title="[bold bright_cyan]🌍 World Clock[/bold bright_cyan]",
            title_align="left"
        ))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print(f"[dim]Available locations: {', '.join(timezone_map.keys())}[/dim]")


def show_multiple_times() -> None:
    """Show time in multiple major cities."""
    cities = [
        ('UTC', 'UTC'),
        ('New York', 'America/New_York'),
        ('Los Angeles', 'America/Los_Angeles'),
        ('London', 'Europe/London'),
        ('Paris', 'Europe/Paris'),
        ('Tokyo', 'Asia/Tokyo'),
        ('Sydney', 'Australia/Sydney'),
    ]
    
    output = []
    for city, tz_str in cities:
        try:
            tz = pytz.timezone(tz_str)
            current_time = datetime.now(tz)
            output.append(f"[cyan]{city:15}[/cyan] {current_time.strftime('%H:%M:%S')}")
        except:
            pass
    
    console.print(Panel(
        "\n".join(output),
        border_style="bright_cyan",
        title="[bold bright_cyan]🌍 World Clocks[/bold bright_cyan]",
        title_align="left"
    ))


def calculate(expression: str) -> None:
    """Safe calculator for mathematical expressions."""
    import ast
    import operator
    
    # Allowed operations
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
    }
    
    def eval_expr(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](eval_expr(node.operand))
        else:
            raise ValueError(f"Unsupported operation: {type(node)}")
    
    try:
        tree = ast.parse(expression, mode='eval')
        result = eval_expr(tree.body)
        
        console.print(Panel(
            f"[bright_white]Expression:[/bright_white]\n{expression}\n\n"
            f"[bright_white]Result:[/bright_white]\n[bold bright_cyan]{result}[/bold bright_cyan]",
            border_style="bright_cyan",
            title="[bold bright_cyan]🔢 Calculator[/bold bright_cyan]",
            title_align="left"
        ))
    except Exception as e:
        console.print(f"[red]Calculation error: {e}[/red]")
