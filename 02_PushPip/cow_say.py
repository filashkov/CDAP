import argparse
from warnings import warn

import cowsay


def main():
    parser = argparse.ArgumentParser(description='cow_say - an analog of the cowsay program')
    parser.add_argument('-f', '--cow', default='default', help='Select cowfile (-f cowfile)')
    parser.add_argument('-e', '--eyes', default='oo', help='Select eyes (-e eye_string)')
    parser.add_argument('-T', '--tongue', default='  ', help='Select tongue (-T tongue_string)')
    parser.add_argument('-W', '--width', type=int, default=40, help='Set wrapping width (-W column)')
    parser.add_argument('-n', '--nowrap', action='store_false', dest='wrap_text', help='Disable word wrap (-n)')
    parser.add_argument('-l', '--list', action='store_true', help='List available cowfiles (-l)')
    parser.add_argument('message', nargs='?', default='', help="Cow's message")
    
    parser.add_argument('-b', '--borg', action='store_true', help='Borg mode')
    parser.add_argument('-d', '--dead', action='store_true', help='Dead mode')
    parser.add_argument('-g', '--greedy', action='store_true', help='Greedy mode')
    parser.add_argument('-p', '--paranoia', action='store_true', help='Paranoia mode')
    parser.add_argument('-s', '--stoned', action='store_true', help='Stoned mode')
    parser.add_argument('-t', '--tired', action='store_true', help='Tired mode')
    parser.add_argument('-w', '--wired', action='store_true', help='Wired mode')
    parser.add_argument('-y', '--youthful', action='store_true', help='Youthful mode')

    args = parser.parse_args()

    if args.list:
        print(cowsay.list_cows())
        return

    cowfile_content = None
    if args.cow != 'default':
        try:
            with open(args.cow, 'r') as file:
                cowfile_content = file.read()
        except FileNotFoundError:
            warn(f"Cowfile '{args.cow}' not found. Using default.")
            args.cow = 'default'

    mode = None
    if args.borg:
        mode = 'b'
    elif args.dead:
        mode = 'd'
    elif args.greedy:
        mode = 'g'
    elif args.paranoia:
        mode = 'p'
    elif args.stoned:
        mode = 's'
    elif args.tired:
        mode = 't'
    elif args.wired:
        mode = 'w'
    elif args.youthful:
        mode = 'y'

    cow_output = cowsay.cowsay(
        message=args.message,
        cow=args.cow if cowfile_content is None else None,
        preset=mode,
        eyes=args.eyes,
        tongue=args.tongue,
        width=args.width,
        wrap_text=args.wrap_text,
        cowfile=cowfile_content
    )
    print(cow_output)


if __name__ == '__main__':
    main()
