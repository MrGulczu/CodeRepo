import math
import random
import concurrent.futures

def Start_Manual():

    NumOfPoints = int(input("Podaj liczbę punktów: "))
    XoYList = []
    PointsList = []
    for i in range(NumOfPoints):
        XoYHelpList = []
        Point = chr(65 + i)
        X = int(input(f"Podaj X dla punktu {Point}: "))
        Y = int(input((f"Podaj Y dla punktu {Point}: ")))
        PointsList.append(Point)
        XoYHelpList.append(X)
        XoYHelpList.append(Y)
        XoYList.append(XoYHelpList)


    return XoYList, PointsList
def Start_File(Filename):
    File = open(Filename,"r").read()
    XoYList = []
    PointsList = []
    Lines = File.split("\n")
    for Line in Lines:
        XoYHelpList = []
        help = Line.split("$")

        PointsList.append(help[0])

        XoYHelpList.append(int(help[1]))
        XoYHelpList.append(int(help[2]))

        XoYList.append(XoYHelpList)

    return XoYList, PointsList

def SelectStartPoint(LoP):

    print("+-------+-------+")
    print("| Punkt | Numer |")
    ok = False
    while ok != True:
        for i in range(len(LoP)):
            print("+-------+-------+")
            print(f"|   {LoP[i]}   |   {i+1}   |")
        print("+-------+-------+")
        Number = int(input("Podaj numer punktu od ktorego chcesz rozpoczac: "))
        if Number not in range(1,len(LoP)+1):
            continue
        else:
            SelP = LoP[Number-1]
            SelP_index = Number-1


            return SelP, SelP_index

def MakeAr(XYList):

    file = open("note.txt","a")
    DistanceAR = []
    for i in range(len(XYList)):
        tablica_pom = []
        for j in range(len(XYList)):
            x = math.fabs(XYList[i][0] - XYList[j][0])
            y = math.fabs(XYList[i][1] - XYList[j][1])

            odl = math.sqrt(pow(x, 2) + pow(y, 2))
            file.write(f"{x}^2 + {y}^2 = c^2 => {round(odl,2)}\\lb\n")
            odl = round(odl, 2)
            tablica_pom.append(odl)
        DistanceAR.append(tablica_pom)

    PheromonAR = []
    for i in DistanceAR:
        HelpPL = []
        for j in i:
            if j != 0:
                HelpPL.append(1.0)
            else:
                HelpPL.append(0.0)
        PheromonAR.append(HelpPL)

    return DistanceAR, PheromonAR

def Creat_Colony(DiAR,PhAR, ANTS_Num):
    ANTSList = []
    for i in range(ANTS_Num):
        ant = ANT(DiAR,PhAR)
        ANTSList.append(ant)
    return ANTSList

def Explore(ANT):
    for i in range(len(ANT.EYES)-1):
        ANT.C_Probability()
        ANT.Choice()
    ANT.C_Distances()
    return [round(ANT.Distance,3), ANT.MEM]

def Best(List):
    Distance = 9999999
    Best_index = 0
    for i in range(len(List)):
        if List[i][0] < Distance:
            Distance = List[i][0]
            Best_index = i
    return Best_index, Distance

def Ph_evaporation(p):
    for i in range(len(PheAR)):
        for j in range(len(PheAR)):
            PheAR[i][j] = PheAR[i][j] * p

def Ph_add(Distance, List_of_points):
    L = len(List_of_points)-1
    pheromone = 1/Distance
    for i in range(L):
        PheAR[List_of_points[i]][List_of_points[i+1]] += pheromone
        PheAR[List_of_points[i+1]][List_of_points[i]] += pheromone



class ANT():

    def __init__(self,DiAR, PhAR):
        self.StartP = random.randint(0,len(DiAR)-1)
        self.MEM = [self.StartP]
        self.EYES = DiAR
        self.PHSENS = PhAR
        self.alpha = 1.51
        self.beta = 1.27

    def C_Probability(self):
        self.NOTVisited = []
        self.LastVisited = self.MEM[-1]
        self.ProbabilityList = []
        for Ponit in range(len(self.EYES)):
            if Ponit not in self.MEM:
                self.NOTVisited.append(Ponit)
        self.Y = 0
        for index in self.NOTVisited:
            self.Y += (math.pow(self.PHSENS[self.LastVisited][index],self.alpha) * math.pow(1/self.EYES[self.LastVisited][index],self.beta))
        for index in self.NOTVisited:
            self.Pr_Help_List = [index]
            self.X = (math.pow(self.PHSENS[self.LastVisited][index],self.alpha) * math.pow(1/self.EYES[self.LastVisited][index],self.beta))

            self.P_ij = self.X/self.Y

            self.Pr_Help_List.append(round(self.P_ij,4))
            self.ProbabilityList.append(self.Pr_Help_List)

    def Choice(self):
        self.rulet = random.uniform(0.0,1.0)
        self.rulet = round(self.rulet,4)
        self.help_int = 0
        random.shuffle(self.ProbabilityList)
        for i in self.ProbabilityList:
            self.help_int += i[1]
            if self.rulet <= self.help_int:
                self.next_hop_index = i[0]
                break
        self.MEM.append(self.next_hop_index)

    def C_Distances(self):
        self.Distance = 0
        self.L = len(self.MEM)
        self.MEM.append(self.MEM[0])
        for i in range(self.L):
            self.Distance += self.EYES[self.MEM[i]][self.MEM[i+1]]



if __name__ == "__main__":
    ok = False
    while ok != True:
        Read = input("Odczyt z pliku (P)\nWprowadzanie reczne (R)\nWybor: ")
        match Read.upper():
            case "P":
                ok = True
                FileName = input("Podaj nazwe pliku: ")
                XYList, PName = Start_File(FileName)
            case "R":
                ok = True
                XYList, PName = Start_Manual()
            case _:
                continue

    DisAR, PheAR = MakeAr(XYList)
    StartP_name, StartP_index = SelectStartPoint(PName)
    Best_route = 99999999999999
    Best_route_count = 0
    Best_route_ind = []
    Continue = True


    if len(DisAR) >= 12:
        number_of_ants = 15
    elif len(DisAR) % 2 == 0:
        number_of_ants = (len(DisAR)//2)+7
    elif len(DisAR) % 2 != 0:
        number_of_ants = ((len(DisAR)-1) // 2) + 7


    while Continue:
        List_of_ants = Creat_Colony(DisAR,PheAR,number_of_ants)
        List_of_results = []

        with concurrent.futures.ProcessPoolExecutor() as executor:
            Results = [executor.submit(Explore,List_of_ants[i]) for i in range(len(List_of_ants))]

            for Finished in concurrent.futures.as_completed(Results):
                List_of_results.append(Finished.result())

        Ph_evaporation(0.8)

        for i in List_of_results:
            Ph_add(i[0],i[1])

        Best_index, Best_Distance = Best(List_of_results)

        if Best_route == Best_Distance:
            Best_route_count += 1
        else:
            if Best_route > Best_Distance:
                Best_route = Best_Distance
                Best_route_count = 0
                Best_route_ind = List_of_results[Best_index][1]
            elif Best_route < Best_Distance:
                Best_route_count +=1
        if Best_route_count == 20:
            Continue = False
            Names = []
            for i in Best_route_ind:
                Names.append(PName[i])
            print(f"Najlepsza trasa:")
            if Names[0] != StartP_name:
                print(*Names[Names.index(StartP_name):], *Names[1:Names.index(StartP_name) + 1])
            else:
                print(*Names)

            print(f"Odleglosc: {Best_route}")