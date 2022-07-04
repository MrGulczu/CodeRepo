import math

def Open_File(filename):
    file = open(filename,"r")
    text_from_file = file.read()
    file.close()
    return text_from_file

def Make_Dictionary(text):
    ASCII_table = [0 for _ in range(256)]
    Dict_of_chr = ""
    for i in text:
        ASCII_table[ord(i)] += 1
    for i in range(len(ASCII_table)):
        if ASCII_table[i] > 0:
            Dict_of_chr += chr(i)
    return Dict_of_chr

def Decimal_To_Binary(i,n):
    help_str = ""
    help_str_2 = ""
    while i > 0:
        help_str += str(i % 2)
        i = i // 2
    for i in help_str:
        help_str_2 = i + help_str_2
    while len(help_str_2) < n:
        help_str_2 = "0" + help_str_2
    return help_str_2

def Convert_Dict_to_bit(dictionary):
    x = len(dictionary)
    n = math.ceil(math.log(x,2))
    list_of_bin = []
    for i in range(x):
        list_of_bin.append(Decimal_To_Binary(i,n))
    return list_of_bin, n

def Extra_bits(k, n):
    r = 8 - (3 + k*n)%8
    return Decimal_To_Binary(r,3), r

def Text_To_Bit(text,dict,bin_dict):
    binary_text = ""
    for i in text:
        for n in range(len(dict)):
            if i == dict[n]:
                binary_text += bin_dict[n]
    return binary_text

def Add_And_Split(prefix, binary_text, prefix_count):
    full_binary_text = prefix + binary_text + "1" * prefix_count
    byte_string = ""
    byte_list = []
    for i in full_binary_text:
        byte_string += i
        if len(byte_string) == 8:
            byte_list.append(byte_string)
            byte_string = ""
    return byte_list

def Binary_To_Decimal(byte_list):
    decimal_list = []
    for i in byte_list:
        help_num = 0
        help_num_2 = 1
        if i[-1] == "1":
            help_num = 1
        for j in range(len(i)-1):
            if i[-j-2] == "1":
               for k in range(j+1):
                   help_num_2 *= 2
               help_num += help_num_2
               help_num_2 = 1
        decimal_list.append(help_num)
    return decimal_list

def Decimal_To_Chr(decimal_list):
    text = ""
    for i in decimal_list:
        text += chr(i)
    return text

def Make_Full_Compression(dict_lenght, dict,compressed_text):
    full_Text = chr(dict_lenght) + dict + compressed_text
    return full_Text

def Compress(Filename):
    Text_in_File = Open_File(Filename)
    Dict = Make_Dictionary(Text_in_File)
    Bin_Dict, N = Convert_Dict_to_bit(Dict)
    Prefix, Prefix_Count = Extra_bits(len(Text_in_File),N)
    Binary_Text = Text_To_Bit(Text_in_File,Dict,Bin_Dict)
    Byte_List = Add_And_Split(Prefix,Binary_Text,Prefix_Count)
    Decimal_List = Binary_To_Decimal(Byte_List)
    Compressed_Text = Decimal_To_Chr(Decimal_List)
    Full_Text = Make_Full_Compression(len(Dict),Dict,Compressed_Text)

    print(f"\nNazwa pliku: {Filename}")
    print(f"Oryginalny tekst:\n{Text_in_File}\n")
    print(f"Slownik: {Dict}\n")
    print(f"Dlugosc oryginalnego tekstu: {len(Text_in_File)}")
    print(f"Unikalne litery: {len(Dict)}")
    print(f"Liczba bitow na na znak: {N}")
    print(f"Liczba nadmiarowych bitow: {Prefix_Count}\n")
    print(f"Bitowa reprezentacja (Podzielona na Bajty):")
    print(*Byte_List, sep=" ")
    print(f"\nDziesietna reprezentacja: ")
    print(*Decimal_List, sep=" ")
    print(f"\nNazwa skompresowanego pliku: Skompresowany_{Filename}")
    print(f"Skompresowany tekst: {Full_Text}")
    print(f"Dlugosc tekstu po kompresji (Dlugosc slownika + slownik + skompresowany tekst): {len(Full_Text)}")


    file = open(f"Skompresowany_{Filename}","w")
    file.write(Full_Text)
    file.close()

def Chr_To_Decimal(compressed_text):
    decimal_list = []
    for i in compressed_text:
        decimal_list.append(ord(i))
    return decimal_list

def Make_Binary_Text(decimal_list):
    binary_text = ""
    for i in decimal_list:
        binary_text+= f"{Decimal_To_Binary(i,8)}"
    end = Binary_To_Decimal([binary_text[:3]])
    original_binary_text = binary_text[3: -end[0]]
    return original_binary_text

def Binary_To_Text(original_binary_text,dict):
    n = math.ceil(math.log(len(dict),2))
    chr_in_binary = ""
    final_text = ""
    for i in original_binary_text:
        chr_in_binary += i
        if len(chr_in_binary) == n:
            bin = Binary_To_Decimal([chr_in_binary])
            final_text += dict[bin[0]]
            chr_in_binary = ""
    return final_text

def Decompress(File_Name):
    Text_in_File = Open_File(f"Skompresowany_{File_Name}")
    Dict = Text_in_File[1:ord(Text_in_File[0])+1]
    Decimal_List = Chr_To_Decimal(Text_in_File[len(Dict)+1:])
    Original_Binary_Text = Make_Binary_Text(Decimal_List)
    Final_Text = Binary_To_Text(Original_Binary_Text,Dict)

    print(f"\n\nDekompresja pliku: Skompresowany_{File_Name}")
    print(f"Tekst w pliku: {Text_in_File}")
    print(f"Nazwa zdekompresowanego pliku: Zdekompresowny_{File_Name}")
    print(f"Tekst po dekompresji:\n{Final_Text}")
    print(f"Dlugosc zdekompresowanego tekstu: {len(Final_Text)}")

    file = open(f"Zdekompresowny_{File_Name}", "w")
    file.write(Final_Text)
    file.close()

if __name__ == "__main__":
    print("Jakub Gulcz nr.75999")
    File_Name = input("Podaj nazwę pliku do kompresji (np. Plik.txt): ")
    Compress(File_Name)
    Decompress(File_Name)

