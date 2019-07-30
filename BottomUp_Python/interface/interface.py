
def repeat_print(num_menu):
    print()
    if num_menu==1:
        return query_main_menu()
    elif num_menu==2:
        return query_accept_menu()
    elif num_menu==3:
        return query_check_condition_menu()

def query_main_menu():
    while True:
        __print_main_menu()
        num_in = __input_number()
        if num_in == -255:
            continue
        if num_in == -1:
            return -1, 'exit'
        if num_in == 1:
            return 1, 'get DB'
        if num_in == 2:
            return 1, 'print status'
        if num_in == 3:
            return 2, 'start accept'

def query_accept_menu():
    while True:
        __print_accept_menu()
        num_in = __input_number()
        if num_in == -255:
            continue
        if num_in == -1:
            return -1, 'exit'
        if num_in == 1:
            return 1, 'stop accept'
        if num_in == 2:
            return 3, 'start check'

def query_check_condition_menu():
    while True:
        __print_check_condition_menu()
        num_in = __input_number()
        if num_in == -255:
            continue
        if num_in == -1:
            return -1, 'exit'
        if num_in == 1:
            return 1, 'stop check'

def __input_number():
    try:
        return int(input("번호를 입력하세요 :"))
    except ValueError:
        return -255


# number 1
def __print_main_menu():
    print("< 초기 메뉴 >")
    print("1. DB 정보 가져오기")
    print("2. 현재 상태 출력")
    print("3. < 기기 연결 >")
    print("-1 : 프로그램 종료")

# number 2
def __print_accept_menu():
    print("< 기기 연결 >")
    print("1. 연결 중단. < 초기 메뉴 >")
    print("2. < 상황 점검 >")
    print("-1 : 프로그램 종료")

# number 3
def __print_check_condition_menu():
    print("< 상황 점검 >")
    print("1. 점검 중단. 연결된 클라이언트 초기화 < 초기 메뉴 >")
    print("-1 : 프로그램 종료")
