import os
import sys
import logging
import argparse
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# Set vars for connection
token = os.getenv('SLACK_TOKEN') or ""

if token is None or token == "":
    eprint('SLACK_TOKEN not set')
    sys.exit(os.EX_CONFIG)


def post_blocks_to_slack(blocks, summary, channel, token):
    client = WebClient(token)
    logger = logging.getLogger(__name__)
    try:
        result = client.chat_postMessage(
            channel=channel,
            text=summary,
            blocks=blocks
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")


def cli():
    """
    Parse command line arguments and invoke get_or_create_application_version
    """
    parser = argparse.ArgumentParser(
        description="""Post stdin to slack on behalf of an app capable of doing so, leveraging the token in environment SLACK_TOKEN""")
    parser.add_argument("channel_name", help="name of channel in which to post")
    parser.add_argument("summary_text", help="brief text only message for contexts that can't render a block (e.g. push notifications)")
    args = parser.parse_args()
    try:
        blocks = sys.stdin.readlines()
        if len("".join(blocks).strip()) == 0:
            eprint("Empty message through stdin. Not sending anything to slack.")
            sys.exit(os.EX_OK)

        json_blocks = json.loads("\n".join(blocks))
        post_blocks_to_slack(json_blocks, args.summary_text, args.channel_name, token)
    except Exception as e:
        eprint(e)
        sys.exit(os.EX_CONFIG)


if __name__ == '__main__':
    cli()
