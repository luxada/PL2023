import sys
import re

def sum_digits(text):
    digits = re.findall(r'\d+', text)
    return sum(int(d) for d in digits)

def main():
    # Inicializa o comportamento
    active = True
    result = 0

    # Loop principal
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            break

        if 'off' in line.lower():
            active = False
        elif 'on' in line.lower():
            active = True

        if active:
            result += sum_digits(line)

        if '=' in line:
            print(result)

if __name__ == '__main__':
    main()
