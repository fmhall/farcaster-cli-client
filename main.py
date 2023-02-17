import typer
from farcaster import Warpcast
from farcaster.models import ApiCast, ApiUser
from typing import Optional
from rich import print

cast_link_prefix = "farcaster://casts/"
user_link_prefix = "farcaster://profiles/"
def main(mnemonic: str, watch_all: bool = False):

    client = Warpcast(mnemonic=mnemonic)

    #print(f"Hello {client.get_me()}")
    following = set()
    if not watch_all:
        following_users = client.get_all_following().users
        following = set([user.fid for user in following_users])
    for cast in client.stream_casts():
        if cast:
            if not watch_all:
                if cast.author.fid not in following:
                    continue
            if "recast" in cast.text:
                recaster = cast.author
                cast_hash = cast.text.lstrip("recast:farcaster://casts/")
                cast = client.get_cast(cast_hash).cast
            else:
                recaster = None
            print_cast(cast, recaster)

def print_cast(cast: ApiCast, recaster: Optional[ApiUser] = None) -> None:
    
    if recaster:
        print(f"🔁 [red bold link={user_link_prefix + str(recaster.fid)}]{recaster.username}[/red bold link] recasted:")
    
    print(
        f"[green bold link={user_link_prefix + str(cast.author.fid)}]{cast.author.username}[/green bold link] [purple link={cast_link_prefix+ str(cast.hash)}](cast)[/purple link]"
    )
    print(cast.text)
    print()

if __name__ == "__main__":
    typer.run(main)