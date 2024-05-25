import requests


def process_page(url):
    response = requests.get(url)
    data = response.json()
    rows = data["data"]["rows"]

    non_zero_rows = []
    zero_rows = []
    for row in rows:
        rank = row["rank"]
        points = row["points"]
        if points > 0:
            print(f"Rank {rank} points: {points}")
            non_zero_rows.append(row)
        else:
            print(f"Rank {rank} points: {points}")
            zero_rows.append(row)

    return non_zero_rows, zero_rows


def count_tiers(rows):
    tier_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    tier_points = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    tier_min_points = {1: float('inf'), 2: float('inf'), 3: float('inf'), 4: float('inf'), 5: float('inf'),
                       6: float('inf')}
    for row in rows:
        tier = row["tier"]
        points = row["points"]
        tier_counts[tier] += 1
        tier_points[tier] += points
        if points < tier_min_points[tier]:
            tier_min_points[tier] = points
    return tier_counts, tier_points, tier_min_points


def get_user_input():
    while True:
        try:
            epoch_id = int(input("Введите номер эпохи (epoch_id): "))
            if epoch_id > 0:
                return epoch_id
            else:
                print("Пожалуйста, введите положительное число.")
        except ValueError:
            print("Пожалуйста, введите корректное число.")


def show_epoch_info():
    epoch_id = get_user_input()

    all_rows = []
    unique_addresses = set()
    zero_points_count = 0

    url = f"https://api-evm.orderly.org/v1/public/points/leaderboard?page=1&size=100&epoch_id={epoch_id}"
    response = requests.get(url)
    data = response.json()
    total_participants = data["data"]["meta"]["total"]

    hz = total_participants // 100 + 1

    for page in range(1, hz + 1):
        url = f"https://api-evm.orderly.org/v1/public/points/leaderboard?page={page}&size=100&epoch_id={epoch_id}"
        non_zero_rows, zero_rows = process_page(url)
        all_rows.extend(non_zero_rows)
        all_rows.extend(zero_rows)
        unique_addresses.update(row["address"] for row in non_zero_rows)
        unique_addresses.update(row["address"] for row in zero_rows)
        zero_points_count += len(zero_rows)

    total_user_points = sum(row["points"] for row in all_rows)
    tier_counts, tier_points, tier_min_points = count_tiers(all_rows)

    print()
    print(f"Epoch: {epoch_id}")
    print(f"Unique addresses: {len(unique_addresses)}")
    print(f"Total points: {total_user_points}")
    for tier in range(6, 0, -1):
        if tier == 1:
            print(f"Tier {tier} addresses: {tier_counts[tier]}, points: {tier_points[tier]}")
        else:
            print(
                f"Tier {tier} addresses: {tier_counts[tier]}, points: {tier_points[tier]} ({tier_min_points[tier]}+ points)")
    print(f"Addresses with 0 points: {zero_points_count}")


def find_address_info():
    while True:
        address = input("Введите адрес для поиска: ")

        if not address:
            print("Адрес не может быть пустым. Пожалуйста, введите корректный адрес.")
            continue

        url = f"https://api-evm.orderly.org/v1/client/points?address={address}"
        response = requests.get(url)
        data = response.json()

        if not data["success"]:
            print("Адрес не найден. Пожалуйста, введите корректный адрес.")
            continue

        current_epoch_points = data["data"]["current_epoch_points"]
        current_epoch_rank = data["data"]["current_epoch_rank"]
        total_points = data["data"]["total_points"]
        global_rank = data["data"]["global_rank"]
        tier = data["data"]["tier"]

        url = f"https://api-evm.orderly.org/v1/public/campaign/user?address={address}&campaign_id=20"
        response = requests.get(url)
        data = response.json()

        if not data["success"]:
            print("Информация о кампании не найдена для данного адреса.")
            volume = 0
            pnl = 0
            filled_orders_count = 0
            end_account_value = 0
        else:
            volume = data["data"]["volume"]
            pnl = data["data"]["pnl"]
            filled_orders_count = data["data"]["filled_orders_count"]
            end_account_value = data["data"]["end_account_value"]

        print()
        print(f"Current epoch points: {current_epoch_points}")
        print(f"Current epoch rank: {current_epoch_rank}")
        print(f"Total points: {total_points}")
        print(f"Total rank: {global_rank}")
        print(f"Tier: {tier}")
        print(f"Volume: {volume}")
        print(f"PnL: {pnl}")
        print(f"Filled orders count: {filled_orders_count}")
        print(f"End account value: {end_account_value}")

        break


def create_participants_file():
    epoch_id = get_user_input()

    filename = input(
        "Введите название файла, в который нужно записать информацию об участниках (без расширения .txt): ")
    filename += ".txt"

    with open(filename, "w") as file:
        url = f"https://api-evm.orderly.org/v1/public/points/leaderboard?page=1&size=100&epoch_id={epoch_id}"
        response = requests.get(url)
        data = response.json()
        total_participants = data["data"]["meta"]["total"]

        hz = total_participants // 100 + 1

        for page in range(1, hz + 1):
            url = f"https://api-evm.orderly.org/v1/public/points/leaderboard?page={page}&size=100&epoch_id={epoch_id}"
            response = requests.get(url)
            data = response.json()
            rows = data["data"]["rows"]

            for row in rows:
                address = row["address"]
                points = row["points"]
                rank = row["rank"]
                tier = row["tier"]
                file.write(f"{address}, {points} points, rank {rank}, tier {tier}\n")

    print(f"Информация об участниках успешно записана в файл {filename}")


# Дружочек, ты зачем эту хуйню читаешь? Понятно же, что этот код сделан, чтобы я тебя сдрейнил


def display_menu():
    print("Выберите действие:")
    print("1. Показать информацию об определенной эпохе")
    print("2. Найти информацию об искомом адресе")
    print("3. Создать текстовый файл с данными об участниках")
    print("0. Выход")


def main():
    while True:
        display_menu()
        choice = input("Введите номер действия: ")

        if choice == "1":
            show_epoch_info()
        elif choice == "2":
            find_address_info()
        elif choice == "3":
            create_participants_file()
        elif choice == "0":
            print("Программа завершена.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")

        print()


if __name__ == "__main__":
    main()
