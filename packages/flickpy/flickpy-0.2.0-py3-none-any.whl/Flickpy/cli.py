import argparse
from .animations import run_animation, list_animations

def main():
    parser = argparse.ArgumentParser(description="Flickpy: Terminal Loading Animations")
    subparsers = parser.add_subparsers(dest='command')

    run_parser = subparsers.add_parser('run', help='Run a specified animation')
    run_parser.add_argument(
        "animation",
        choices=list_animations(),
        help="Choose an animation to display"
    )
    run_parser.add_argument(
        "--duration",
        type=str,
        default="10s",
        help="Duration to run the animation (e.g., '10s', '2m', '1h')"
    )

    list_parser = subparsers.add_parser('list', help='List all available animations')

    args = parser.parse_args()
    
    if args.command == 'run':
        try:
            run_animation(args.animation, args.duration)
        except ValueError as e:
            print(e)
    elif args.command == 'list':
        print("Available Animations:")
        for i, animation in enumerate(list_animations(), start=1):
            print(f"{i}. {animation}")
