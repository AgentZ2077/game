
import argparse
from planner.planner import dispatch

parser = argparse.ArgumentParser()
parser.add_argument("--agent", type=str, required=True)
parser.add_argument("--player", type=str, default="guest")
args = parser.parse_args()

result = dispatch(args.agent, args.player)
print("Agent Output:", result)
