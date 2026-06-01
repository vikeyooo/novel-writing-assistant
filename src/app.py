"""
小说创意助手 - 交互式 CLI 应用
基于 DeepSeek V4 的完整功能子辅助工具
"""

import os
import sys
from typing import Optional
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from dotenv import load_dotenv

from .deepseek_api import DeepSeekAPI
from .deepseek_advanced import DeepSeekAdvanced
from .web_searcher import WebSearcher
from .data_manager import DataManager
from .writing_assistant import WritingAssistant
from .consistency_checker import ConsistencyChecker
from .logger_config import setup_logger
from loguru import logger

load_dotenv()
setup_logger()

console = Console()


class NovelAssistant:
    """\u4e92动式小说创意助手"""

    def __init__(self):
        """初始化所有组件"""
        try:
            self.api = DeepSeekAPI()
            self.advanced = DeepSeekAdvanced(api=self.api)
            self.data = DataManager()
            self.assistant = WritingAssistant()
            self.checker = ConsistencyChecker()
            self.searcher = WebSearcher()
            console.print("[green]\u2705 小说创意助手已启动[/green]")
        except Exception as e:
            console.print(f"[red]\u274c 初始化失败: {e}[/red]")
            sys.exit(1)

    def show_menu(self):
        """\u6848示主菜单"""
        console.clear()
        console.print(
            "[bold cyan]\n\u2728 小说创意助手 v2.0.0 - DeepSeek V4 \u4e1c方\u7248[/bold cyan]"
        )
        console.print("[yellow]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500[/yellow]")
        console.print("""
[bold]\u4e3b\u83dc\u5355[/bold]
1. \ud83d\udcdd \u5199\u4f5c\u5efa\u8bae      - \u83b7\u5f97\u4e0b\u4e00\u7ae0\u7684\u6545\u4e8b\u5efa\u8bae
2. \ud83e\udde0 \u4eba\u7269\u5206\u6790      - \u6df1\u5ea6\u5206\u6790\u4eba\u7269\u4e0a\u8bbe
3. \ud83d\udd0d \u8054\u7f51\u641c\u7d22      - \u641c\u7d22\u76f8\u5173\u80cc\u666f\u8d44\u6599
4. \ud83d\udca1 \u5934\u8111\u98ce\u66b4      - \u591a\u89d2\u5ea6\u751f\u6210\u521b\u610f
5. \u270d\ufe0f \u7eed\u5199\u6545\u4e8b      - AI \u5e2e\u6助\u7ee7\u7eed章\u8282
6. \ud83d\udd27 \u6539\u8fdb\u6587\u5b57      - \u4f18\u5316\u6587\u672c\u8d28\u91cf
7. \u2705 \u4e00\u81f4\u6027\u68c0\u67e5    - \u68c0\u67e5\u903b\u8f91\u77db\u76fe
8. \ud83d\udcca \u7edf\u8ba1\u4fe1\u606f      - \u67e5\u770b\u5c0f\u8bf4\u8fdb\u5ea6
9. \ud83d\udcbe \u4fdd\u5b58\u7ae0\u8282      - \u4fdd\u5b58\u7ae0\u8282\u5185\u5bb9
10. \ud83d\udcd6 \u67e5\u770b\u7ae0\u8282     - \u9605\u8bfb\u5df2\u4fdd\u5b58\u7ae0\u8282
11. \ud83d\udce4 \u5bfc\u51fa\u5c0f\u8bf4     - \u5bfc\u51fa\u4e3a TXT \u6587\u4ef6
12. \ud83d\udc1b \u6d4b\u8bd5 API        - \u6d4b\u8bd5 DeepSeek \u8fde\u63a5
13. \u274c \u9000\u51fa
        """)
        console.print("[yellow]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500[/yellow]")

    def write_suggestion(self):
        """\u83b7\u5f97\u5199\u4f5c\u5efa\u8bae"""
        try:
            chapter = click.prompt("\u8bf7\u8f93\u5165\u7ae0\u8282\u53f7", type=int)
            search = click.confirm("\u662f\u5426\u641c\u7d22\u76f8\u5173\u4fe1\u606f?", default=True)

            console.print("\n[cyan]\u6b63\u5728\u751f\u6210\u5efa\u8bae...[/cyan]")

            keywords = None
            if search:
                keyword_input = click.prompt("\u8f93\u5165\u641c\u7d22\u5173\u952e\u8bcd\uff08\u903b\u8f91\u9017\u53f7\u5206\u9694\uff09", default="")
                if keyword_input:
                    keywords = [k.strip() for k in keyword_input.split(",")]

            suggestion = self.assistant.suggest_plot(chapter, search_keywords=keywords)
            console.print("\n" + "="*50)
            console.print(Markdown(suggestion))
            console.print("="*50)

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def analyze_character(self):
        """\u5206\u6790\u4eba\u7269"""
        try:
            char_name = click.prompt("\u8bf7\u8f93\u5165\u4eba\u7269\u540d\u79f0")
            search = click.confirm("\u662f\u5426\u641c\u7d22\u53c2\u8003\u8d44\u6599?", default=True)

            console.print(f"\n[cyan]\u6b63\u5728\u5206\u6790 {char_name}...[/cyan]")
            analysis = self.assistant.analyze_character(char_name, search_references=search)
            console.print("\n" + "="*50)
            console.print(Markdown(analysis))
            console.print("="*50)

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def web_search(self):
        """\u8054\u7f51\u641c\u7d22"""
        try:
            query = click.prompt("\u8bf7\u8f93\u5165\u641c\u7d22\u5185\u5bb9")
            console.print(f"\n[cyan]\u6b63\u5728\u641c\u7d22: {query}...[/cyan]")

            results = self.searcher.search(query, num_results=5)

            if results:
                console.print(f"\n[yellow]\u627e\u5230 {len(results)} \u4e2a\u7ed3\u679c[/yellow]\n")
                for i, result in enumerate(results, 1):
                    console.print(f"[bold]{i}. {result['title']}[/bold]")
                    console.print(f"   {result['snippet']}")
                    console.print(f"   [blue]{result['url']}[/blue]\n")
            else:
                console.print("[yellow]\u627e\u4e0d\u5230\u7ecf\u5408\u7684\u7ed3\u679c[/yellow]")

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def brainstorm(self):
        """\u5934\u8111\u98ce\u66b4"""
        try:
            theme = click.prompt("\u8bf7\u8f93\u5165\u521b\u610f\u4e3b\u9898")
            console.print(f"\n[cyan]\u6b63\u5728\u4ece\u591a\u4e2a\u89d2\u5ea6\u8fdb\u884c\u5934\u8111\u98ce\u66b4...[/cyan]")

            ideas = self.assistant.brainstorm_ideas(theme)
            console.print("\n" + "="*50)
            console.print(Markdown(ideas))
            console.print("="*50)

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def write_continuation(self):
        """\u7eed\u5199\u6545\u4e8b"""
        try:
            chapter = click.prompt("\u8bf7\u8f93\u5165\u5f53\u524d\u7ae0\u8282\u53f7", type=int)
            length = click.prompt(
                "\u9009\u62e9\u957f\u5ea6 (short/medium/long)",
                type=click.Choice(["short", "medium", "long"]),
                default="medium"
            )
            tone = click.prompt("\u8f93\u5165\u8bed\u8c04\u63d0\u793a \uff08\u53ef\u9009\uff09", default="")

            console.print("\n[cyan]\u6b63\u5728\u7eed\u5199\u6545\u4e8b...[/cyan]")
            continuation = self.assistant.write_continuation(
                chapter,
                length=length,
                tone=tone if tone else None
            )

            console.print("\n" + "="*50)
            console.print(Markdown(continuation))
            console.print("="*50)

            save = click.confirm("\u662f\u5426\u4fdd\u5b58\u8fd9\u4e2a\u7ae0\u8282?")
            if save:
                title = click.prompt("\u8bf7\u8f93\u5165\u7ae0\u8282\u6807\u9898")
                self.data.save_chapter(chapter + 1, title, continuation)
                console.print("[green]\u2705 \u7ae0\u8282\u5df2\u4fdd\u5b58[/green]")

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def improve_writing(self):
        """\u6539\u8fdb\u6587\u5b57"""
        try:
            console.print("\u8bf7\u8f93\u5165\u6216\u7c98\u8d34\u8981\u6539\u8fdb\u7684\u6587\u672c (\u8f93\u5165 'END' \u7ed3\u675f):")
            lines = []
            while True:
                line = click.prompt("", default="", show_default=False)
                if line.strip() == "END":
                    break
                lines.append(line)

            text = "\n".join(lines)
            if not text.strip():
                console.print("[yellow]\u672a\u8f93\u5165\u4efb\u4f55\u5185\u5bb9[/yellow]")
                return

            aspect = click.prompt(
                "\u9009\u62e9\u6539\u8fdb\u65b9\u9762 (general/dialogue/description/pacing/grammar/style)",
                default="general"
            )

            console.print(f"\n[cyan]\u6b63\u5728\u6539\u8fdb\u6587\u5b57 ({aspect})...[/cyan]")
            improved = self.assistant.improve_writing(text, aspect=aspect)
            console.print("\n" + "="*50)
            console.print(Markdown(improved))
            console.print("="*50)

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def check_consistency(self):
        """\u4e00\u81f4\u6027\u68c0\u67e5"""
        try:
            console.print("\n[cyan]\u6b63\u5728\u8fdb\u884c\u5168\u9762\u4e00\u81f4\u6027\u68c0\u67e5...[/cyan]")
            report = self.checker.full_consistency_check()

            console.print("\n[bold cyan]\u2705 \u4e00\u81f4\u6027\u68c0\u67e5\u5b8c\u6210[/bold cyan]")
            console.print("\n" + "="*50)
            for key, value in report.get("checks", {}).items():
                console.print(f"\n[yellow]\u3010{key.upper()}\u3011[/yellow]")
                if isinstance(value, dict) and "analysis" in value:
                    console.print(Markdown(value["analysis"]))
                else:
                    console.print(str(value)[:500])
            console.print("="*50)

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def show_statistics(self):
        """\u67e5\u770b\u7edf\u8ba1\u4fe1\u606f"""
        try:
            stats = self.data.get_statistics()
            table = Table(title="\ud83d\udcca \u5c0f\u8bf4\u7edf\u8ba1")
            table.add_column("\u9879\u76ee", style="cyan")
            table.add_column("\u6570\u503c", style="magenta")
            table.add_row("\u603b\u7ae0\u6570", str(stats['total_chapters']))
            table.add_row("\u603b\u5b57\u6570", str(stats['total_words']))
            table.add_row("\u4eba\u7269\u603b\u6570", str(stats['total_characters']))
            table.add_row("\u5e73\u5747\u7ae0\u8282\u957f\u5ea6", str(stats['average_chapter_length']))
            console.print(table)

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def save_chapter(self):
        """\u4fdd\u5b58\u7ae0\u8282"""
        try:
            chapter_num = click.prompt("\u7ae0\u8282\u53f7", type=int)
            title = click.prompt("\u7ae0\u8282\u6807\u9898")
            console.print("\u8bf7\u8f93\u5165\u7ae0\u8282\u5185\u5bb9 (\u8f93\u5165 'END' \u7ed3\u675f):")

            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)

            content = "\n".join(lines)
            self.data.save_chapter(chapter_num, title, content)
            console.print("[green]\u2705 \u7ae0\u8282\u5df2\u4fdd\u5b58[/green]")

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def view_chapter(self):
        """\u67e5\u770b\u7ae0\u8282"""
        try:
            chapters = self.data.list_chapters()
            if not chapters:
                console.print("[yellow]\u6ca1\u6709\u4fdd\u5b58\u7684\u7ae0\u8282[/yellow]")
                return

            console.print("\n[bold]\u53ef\u7528\u7684\u7ae0\u8282\uff1a[/bold]")
            for ch in chapters:
                console.print(f"  {ch['chapter_num']:3d}. {ch['title']} ({ch['word_count']} \u5b57)")

            chapter_num = click.prompt("\u8bf7\u8f93\u5165\u7ae0\u8282\u53f7", type=int)
            chapter = self.data.load_chapter(chapter_num)

            if chapter:
                console.print(f"\n[bold cyan]\u7b2c {chapter_num} \u7ae0: {chapter['title']}[/bold cyan]")
                console.print("\n" + "="*60)
                console.print(chapter['content'])
                console.print("="*60)
                console.print(f"\n[yellow]\u5b57\u6570: {chapter['word_count']}[/yellow]")
            else:
                console.print("[red]\u7ae0\u8282\u672a\u627e\u5230[/red]")

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def export_novel(self):
        """\u5bfc\u51fa\u5c0f\u8bf4"""
        try:
            output_path = click.prompt("\u8f93\u51fa\u6587\u4ef6\u8def\u5f84", default="./novel_export.txt")
            console.print(f"\n[cyan]\u6b63\u5728\u5bfc\u51fa\u5230 {output_path}...[/cyan]")

            success = self.data.export_to_txt(output_path)
            if success:
                console.print(f"[green]\u2705 \u6210\u529f\u5bfc\u51fa\u5230 {output_path}[/green]")
            else:
                console.print("[red]\u274c \u5bfc\u51fa\u5931\u8d25[/red]")

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def test_api(self):
        """\u6d4b\u8bd5 API \u8fde\u63a5"""
        try:
            console.print("\n[cyan]\u6b63\u5728\u6d4b\u8bd5 DeepSeek API \u8fde\u63a5...[/cyan]")
            if self.api.test_connection():
                console.print("[green]\u2705 DeepSeek API \u8fde\u63a5\u6210\u529f[/green]")
            else:
                console.print("[red]\u274c DeepSeek API \u8fde\u63a5\u5931\u8d25[/red]")

        except Exception as e:
            console.print(f"[red]\u274c \u9519\u8bef: {e}[/red]")

    def run(self):
        """\u4e3b\u4ea4\u4e92\u5faa\u73af"""
        while True:
            self.show_menu()
            choice = click.prompt("\u8bf7\u9009\u62e9\u64cd\u4f5c (1-13)")

            if choice == "1":
                self.write_suggestion()
            elif choice == "2":
                self.analyze_character()
            elif choice == "3":
                self.web_search()
            elif choice == "4":
                self.brainstorm()
            elif choice == "5":
                self.write_continuation()
            elif choice == "6":
                self.improve_writing()
            elif choice == "7":
                self.check_consistency()
            elif choice == "8":
                self.show_statistics()
            elif choice == "9":
                self.save_chapter()
            elif choice == "10":
                self.view_chapter()
            elif choice == "11":
                self.export_novel()
            elif choice == "12":
                self.test_api()
            elif choice == "13":
                console.print("[cyan]\u611f\u8c22\u4f7f\u7528\uff01\u518d\u89c1 \ud83d\udc4b[/cyan]")
                break
            else:
                console.print("[red]\u65e0\u6548\u9009\u62e9[/red]")

            click.prompt("\u6309 Enter \u7ee7\u7eed...")


@click.group()
def cli():
    """\u5c0f\u8bf4\u521b\u610f\u52a9\u624b CLI"""
    pass


@cli.command()
def interactive():
    """\u4ea4\u4e92\u5f0f\u6a21\u5f0f"""
    assistant = NovelAssistant()
    assistant.run()


@cli.command()
@cli.option('--text', prompt='\u8f93\u5165\u8981\u6539\u8fdb\u7684\u6587\u672c', help='\u6587\u672c')
@cli.option('--aspect', default='general', help='\u6539\u8fdb\u65b9\u9762')
def improve(text, aspect):
    """\u6539\u8fdb\u6587\u5b57"""
    from .writing_assistant import WritingAssistant
    assistant = WritingAssistant()
    improved = assistant.improve_writing(text, aspect=aspect)
    console.print(Markdown(improved))


if __name__ == '__main__':
    cli()
