
with open("test_1A_1h", "w") as text_file:
    for x in range(len(bat_dict[1])):
        text_file.write("%.8f, %.8f, %.8f, %.8f\n" %(bat_dict[1][x], bat_dict[2][x], bat_dict[3][x], bat_dict[4][x]))
print("DONE")


