#import
import numpy as np
import math
import random
#---------------------------------------------Funkje dla danych------------------------------------------------------#
def GetData(File_name):
    # Funkcja pobiera dane
    File = open(File_name,"r")
    Raw_Data = File.readlines()
    File.close()
    Data_To_Return = []
    for i in Raw_Data:
        Data_To_Return.append(i[:-1].split(",")[1:])
    Raw_Data.clear()
    # Zwracamy dane bez id
    return Data_To_Return[1:]

def ConvertData(Raw_Data,LE_P):
    # Funkcja rozdziela dane na część uczącą oraz część sprawdzającą
    #   Raw_Data -> Surowe Dane
    #   LE_P -> procent danych, które mają zostać wykorzystane podczas uczenia
    # Pozyskanie etykiet oraz liczby przykładów dla każdej z nich
    Lable_list = []
    for i in range(len(Raw_Data)):
        if Raw_Data[i][-1] not in Lable_list:
            Lable_list.append(Raw_Data[i][-1])

    EFE_Lable = int((LE_P*len(Raw_Data))/len(Lable_list))



    # Stworzenie zbioru uczącego wraz z odpowiedziami
    Example_list = []
    Example_Solution_list = []
    for i in range(len(Lable_list)):
        for j in range(EFE_Lable):
            help = [0, 0, 0]
            help_int = i*(int(len(Raw_Data)/len(Lable_list)))+j
            Example_list.append(Raw_Data[help_int][:-1])
            if Raw_Data[help_int][-1] == Lable_list[i]:
                help[i] = 1
                Example_Solution_list.append(help)
    Example_list = np.array(Example_list)
    Example_list = Example_list.astype(float)

    # Stworzenie zbioru sprawdzającego
    Check = []
    Check_Solution_List = []
    for i in range(len(Lable_list)):
        help = [0, 0, 0]
        help_int = EFE_Lable + i * (int(len(Raw_Data) / len(Lable_list)))
        help_int2 = (i + 1) * (int(len(Raw_Data) / len(Lable_list)))
        for j in range(help_int,help_int2):
            Check.append(Raw_Data[j][:-1])
            if Raw_Data[help_int][-1] == Lable_list[i]:
                help[i] = 1
                Check_Solution_List.append(help)
    Check = np.array(Check)
    Check = Check.astype(float)

    #Zwracamy:
    #       - Liste etykiet
    #       - Liste przykładów oraz odpowiedzi
    #       - Liste Sprawdzającą oraz odpowiedzi

    return Lable_list,Example_list.T,Example_Solution_list,Check.T, Check_Solution_List

#-----------------------------------------Funkcje dla sieci neuronowej-----------------------------------------------#
def Init(S,K1,K2):
    # Funkcja tworzy sieć dwuwarstwową i wypełnia macierze wag losowymi wartościami
    W1 = []
    W2 = []

    for i in range(S+1):
        wagi_dla_x = []
        for j in range(K1):
            waga = random.uniform(-0.1, 0.1) * 0.2 - 0.1
            wagi_dla_x.append(waga)

        W1.append(wagi_dla_x)
    W1 = np.array(W1)

    for i in range(K1+1):
        wagi_dla_x2 = []
        for j in range(K2):
            waga2 = random.uniform(-0.1, 0.1) * 0.2 - 0.1
            wagi_dla_x2.append(waga2)
        W2.append(wagi_dla_x2)

    W2= np.array(W2)

    return W1, W2


def SimulateNN(W1,W2,Example):
    # Funkcja symulująca działanie sieci dwuwarstwowej
    Beta = 3
    X1 = [-1]

    for i in Example:
        X1.append(i)
    X1 = np.array(X1)


    U1 = np.matmul(W1.T, X1)


    Y1 = []
    for i in range(len(W1.T)):
        Y1.append(1. / (1 + math.exp(-Beta * U1[i])))
    Y1 = np.array(Y1)

    X2 = [-1]
    for i in Y1:
        X2.append(i)
    X2 = np.array(X2)
    U2 = np.matmul(W2.T, X2)

    Y2 = []
    for i in range(len(W2.T)):
        Y2.append(1. / (1 + math.exp(-Beta * U2[i])))
    Y2 = np.array(Y2)

    return Y1,Y2

def Learn(W1_before,W2_before,Examples,Solutions,n):
    # Funkcja ucząca (wybieranie przykładów, liczenie błędów oraz obliczanie poprawek do wag)
    Number_of_Examples = len(Examples[0])

    Learning_rate = 0.15
    W1 = W1_before
    W2 = W2_before
    Beta = 3

    Numbers_of_examples = []
    for k in range(n):
        if len(Numbers_of_examples) == Number_of_Examples:
            Numbers_of_examples = []

        else:
            Finish = False
            while not Finish:
                NumO_Example = random.randint(0, Number_of_Examples - 1)
                if NumO_Example not in Numbers_of_examples:
                    Finish = True
                    Numbers_of_examples.append(NumO_Example)


        X = Examples[:,NumO_Example]
        X1 = [-1]

        for i in X:
            X1.append(i)
        X1 = np.array(X1)

        Y1, Y2 = SimulateNN(W1,W2,X)

        X2 = [-1]
        for i in Y1:
            X2.append(i)
        X2 = np.array(X2)

        D2 = Solutions[NumO_Example]-Y2

        D1 = W2[1:,:]* D2

        E1 = []

        for i in range(len(Y1)):
            E1_1 = D1[i] * Beta * Y1[i] * (1-Y1[i])
            E1.append(E1_1[0])
        E1 = np.array(E1)

        E2 = []
        for i in range(len(Y2)):
            E2_1 = D2[i] * Beta * Y2[i] * (1-Y2[i])
            E2.append(E2_1)
        E2 = np.array(E2)

        dW1 = []
        for i in range(len(X1)):
            help1 = []
            for j in range(len(E1)):
                help1.append(Learning_rate*X1[i]*E1[j])
            dW1.append(help1)

        dW2 = []
        for i in range(len(X2)):
            help2 = []
            for j in range(len(E2)):
                help2.append(Learning_rate*X2[i]*E2[j])
            dW2.append(help2)

        dW1 = np.array(dW1)
        dW2 = np.array(dW2)

        W1 = np.add(dW1,W1)
        W2 = np.add(dW2,W2)

    return W1,W2


#------------------------------------------------Ciało programu------------------------------------------------------#
if __name__ == "__main__":

    Data = GetData("IRIS.txt")

    Labels,Examples,Solution_E,Check,Solution_C = ConvertData(Data,0.3)

    W1_Before,W2_Before = Init(len(Examples.T[0]),len(Examples.T[0])*5,len(Labels))

    W1_After, W2_After = Learn(W1_Before, W2_Before, Examples, Solution_E, 7000)

    correct_worng = []
    for i in range(len(Check.T)):

        Y1, Y2 = SimulateNN(W1_After, W2_After, Check[:, i])
        Help_I = Y2[0]
        Help_II = 0
        for j in range(len(Y2)):
            if Y2[j] > Help_I:
                Help_I = Y2[j]
                Help_II = j
        if Solution_C[i][Help_II] == 1:
            correct_worng.append("correct")
        else:
            correct_worng.append("wrong")

    print(f"Correct:{correct_worng.count('correct')} ({round((correct_worng.count('correct')/len(Check.T)) * 100,2)}%)")
    print(f"Wrong: {correct_worng.count('wrong')} ({round((correct_worng.count('wrong') / len(Check.T)) * 100,2)}%)")

