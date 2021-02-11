from geocoder import get_ll
from mapapi import show_map


def main():
    # toponym_to_find = ' '.join(sys.argv[1:])
    toponym_to_find = input()
    if toponym_to_find:
        ll = get_ll(toponym_to_find)
        show_map(ll, 12, add_param='pt')
    else:
        print('NO')


if __name__ == '__main__':
    main()
