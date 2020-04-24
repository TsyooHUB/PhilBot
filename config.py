token = ''

try:
    token = [line.rstrip('\n') for line in open('data/.token.txt')][0]
except FileNotFoundError:
    print("Token file not found")