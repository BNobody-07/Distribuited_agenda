# import os
# from datetime import date, time, datetime
# from pathlib import Path

# x = date.today()
# y = time(12)
# y = y.strftime("%X")
# z = datetime.now()
# print(f"{z}")


# SCHEDULES_FILE = Path("schedules.txt")
# f = open(SCHEDULES_FILE, "x")

# with open(SCHEDULES_FILE, 'a') as f:
#     for x in range(8, 21):
#         f.write(f">> {time(x)}\n")

# with open(rf'{SCHEDULES_FILE}', 'r') as file:
#         content = file.read()
#         if y in content:
#             print('string exist')
#         else:
#             print('string does not exist')

# with open(SCHEDULES_FILE, "r+") as f:
#     lines = [line for line in f if line.strip() != f">> {y}"]
#     f.seek(0)
#     f.writelines(lines)
#     f.truncate()

# print("Removed")
# with open(SCHEDULES_FILE) as f:
#      print(f.read())

    
# os.remove(SCHEDULES_FILE)
# s = print(type(y))


x = int(input("opcao: "))
