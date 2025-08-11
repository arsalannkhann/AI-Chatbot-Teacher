#!/usr/bin/env python3
"""Simple CLI Interface"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from rich.console import Console
    from rich.panel import Panel
    from src.chatbot import SimpleAITeacher
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

console = Console()

def main():
    teacher = SimpleAITeacher()

    console.print(Panel.fit(
        "🤖📚 Simple AI Teacher Chatbot\n"
        "Ask questions in English, Hindi, or Telugu!\n"
        "Type 'quit' to exit, 'stats' for statistics",
        style="bold blue"
    ))

    while True:
        try:
            user_input = console.input("\n[bold green]You: [/bold green]").strip()

            if user_input.lower() in ['quit', 'exit', 'bye']:
                console.print("[yellow]Goodbye! Happy learning! 👋[/yellow]")
                break

            if user_input.lower() == 'stats':
                stats = teacher.get_stats()
                console.print(f"[cyan]Messages: {stats['total_messages']}[/cyan]")
                console.print(f"[cyan]Languages: {', '.join(stats['languages_used'])}[/cyan]")
                console.print(f"[cyan]Subjects: {', '.join(stats['subjects_discussed'])}[/cyan]")
                continue

            if not user_input:
                continue

            console.print("[dim]Thinking...[/dim]")
            response = teacher.chat(user_input)

            console.print(f"[blue]Teacher ({response['language_name']} | {response['category'].title()}):[/blue]")
            console.print(Panel(response['response'], style="green"))

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye! Happy learning! 👋[/yellow]")
            break

if __name__ == "__main__":
    main()