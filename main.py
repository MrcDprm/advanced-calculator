from evaluator import evaluate
from history import History


def format_result(value):
    if value == int(value):
        return str(int(value))
    return str(round(value, 10))



def print_help():
    print("Komutlar: gecmis, temizle, yardim, cikis")
    print("Örnekler: (3 + 4) * 2  2 ^ 3  sqrt(16)")


def show_history(history):
    if history.is_empty():
        print("Geçmiş boş.")
        return
    for number, (expression, result) in enumerate(history.get_all(), start = 1):
        print(f"{number}. {expression} = {result}")

def main():
    history = History()
    print("Gelişmiş Hesap Makinesi")
    print_help

    while True:
        user_input = input("> ").strip()
        command = user_input.lower()

        if not user_input:
            continue
        elif command == "cikis":
            print("Görüşmek üzere!")
            break
        elif command == "gecmis":
            show_history(history)
        elif command == "temizle":
            history.clear()
            print("Geçmiş temizlendi.")
        elif command == "yardim":
            print_help()
        else:
            try:
                result = format_result(evaluate(user_input))
                history.add(user_input, result)
                print(f"= {result}")
            except (ValueError, ZeroDivisionError, OverflowError) as error:
                print(f"Hata: {error}")


if __name__ == "__main__":
    main()