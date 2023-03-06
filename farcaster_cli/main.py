import typer
from farcaster import Warpcast
from farcaster.models import ApiCast, ApiUser
from typing import Optional, Set
from rich import print
from rich.panel import Panel
from rich.padding import Padding
from rich.progress import Progress, SpinnerColumn, TextColumn

cast_link_prefix = "farcaster://casts/"
user_link_prefix = "farcaster://profiles/"


def main(mnemonic: str, watch_all: bool = False, skip_existing: bool = False):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Logging in...", total=None)
        progress.add_task(description="Reticulating splines...", total=None)

        client = Warpcast(mnemonic=mnemonic)

        following: Set[int] = set()
        if not watch_all:
            following_users = client.get_all_following().users
            following = set([user.fid for user in following_users])
    print("Ready!")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Listening for new casts...", total=None)
        for cast in client.stream_casts(skip_existing=skip_existing):
            if cast:
                if not watch_all:
                    if cast.author.fid not in following:
                        continue
                if cast.text.startswith("recast:farcaster://casts/"):
                    recaster = cast.author
                    cast_hash = cast.text.lstrip("recast:farcaster://casts/")
                    cast = client.get_cast(cast_hash).cast
                else:
                    recaster = None
                print_cast(cast, recaster)


def print_cast(cast: ApiCast, recaster: Optional[ApiUser] = None) -> None:
    if recaster:
        print(
            f"🔁 [red bold link={user_link_prefix + str(recaster.fid)}]{recaster.username}[/red bold link] recasted:"
        )
    parent = ""
    if cast.parent_hash:
        parent = f" replying to [purple link={cast_link_prefix + str(cast.parent_hash)}](parent)[/purple link]"

    print(
        Padding(
            f"[green bold link={user_link_prefix + str(cast.author.fid)}]{cast.author.username}[/green bold link]{parent} | [purple link={cast_link_prefix + str(cast.hash)}](cast)[/purple link]",
            (0, 1),
        )
    )
    print(Panel(cast.text))
    print()


def start():
    typer.run(main)
