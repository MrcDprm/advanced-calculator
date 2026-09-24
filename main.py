from evaluator import evaluate
from history import History
from formatter import format_result


def print_help():
    print("Komutlar: gecmis, temizle, derece, radyan, yardim, cikis")
    print("Örnekler: (3 + 4) * 2   2 ^ 3   sqrt(16)   sin(30)   5!   200+10%")


def show_history(history):
    if history.is_empty():
        print("Geçmiş boş.")
        return
    for number, (expression, result) in enumerate(history.get_all(), start = 1):
        print(f"{number}. {expression} = {result}")

def main():
    history = History("history.json")
    print("Gelişmiş Hesap Makinesi")
    degrees = True
    print_help

    while True:
        try:
            user_input = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGörüşmek üzere!")
            break

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
        elif command == "derece":
            degrees = True
            print("Açı birimi: derece")
        elif command == "radyan":
            degrees = False
            print("Açı birimi: radyan")        
        elif command == "yardim":
            print_help()
        else:
            try:
                result = format_result(evaluate(user_input, degrees))
                history.add(user_input, result)
                print(f"= {result}")
            except (ValueError, ZeroDivisionError, OverflowError) as error:
                print(f"Hata: {error}")


if __name__ == "__main__":
    main()