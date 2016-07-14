import os;
size = int(input("Tamanho do array: "))                
arr = []

for i in range (size):
    arr.append(int(input("Numero: ")))


file = open("Isort.smv", "w")
file.write("MODULE main\n\n")
file.write("VAR\n\t")
file.write("arr : array 0 .. " + str(size -1) + " of {")
x = list(set(arr))
for i in range (len(x)):
    file.write(str(x[i]))
    if(i < len(x) - 1): 
        file.write(",")
    else: 
        file.write("};\n")

file.write("\ti : 0 .. "+str(size)+";\n")
file.write("\tj : 0 .. "+str(size-1)+";\n")

        
file.write("\taux : {")
for i in range (len(x)):
    file.write(str(x[i]))
    if(i < len(x) - 1): 
        file.write(",")
    else: 
        file.write("};\n")

file.write("\tstate : {b1,b2,b3,b4,b5,b6};\n")
file.write("DEFINE\n\tord := ")
for i in range (size - 1):
    file.write("arr["+str(i)+"] <= arr["+str(i+1)+"]")
    if(i < size - 2): file.write(" & ")
    else: file.write(";\n")

file.write("\nASSIGN\n")
file.write("\tinit(state) := b1;\n\tinit(i) := 0;\n\tinit(j) := 0;\n")
file.write("\tinit(aux) := arr[0];\n")
for i in range(size):
    file.write("\tinit(arr["+str(i)+"]) := "+str(arr[i])+";\n")

file.write("\tnext(state) := case\n\t\t\t\t\tstate = b1 & i < "+str(size)+" : b2;\n\t\t\t\t\tstate = b1 & i = "+str(size)+" : b6;\n\t\t\t\t\tstate = b2 & (j < 1 | arr[j] >= arr[j - 1]) : b5;\n")
file.write("\t\t\t\t\tstate = b2 & j >= 1 & arr[j] < arr[j - 1] : b3;\n")
file.write("\t\t\t\t\tstate = b3 : b4;\n")
file.write("\t\t\t\t\tstate = b4 : b2;\n")
file.write("\t\t\t\t\tstate = b5 & i = "+str(size)+" : b6;\n")
file.write("\t\t\t\t\tstate = b5 : b1;\n")
file.write("\t\t\t\t\tTRUE : state;\n")
file.write("\t\t\t\tesac;\n")
file.write("\tnext(aux) :=\n\t\t\t\tcase\n\t\t\t\t\tj > 0 : arr[j - 1];\n\t\t\t\t\tTRUE : aux;\n\t\t\t\tesac;\n")
file.write("\tnext(i) :=\n\t\t\t\tcase\n\t\t\t\t\tstate = b5 & i <= "+str(size-1)+": i + 1;\n\t\t\t\t\tTRUE : i;\n\t\t\t\tesac;\n")
file.write("\tnext(j) :=\n\t\t\t\tcase\n\t\t\t\t\tstate = b1 & i < "+str(size)+" : i;\n\t\t\t\t\tstate = b4 & j > 1 : j - 1;\n\t\t\t\t\tTRUE : j;\n\t\t\t\tesac;\n")
for i in range (size):
    file.write("\tnext(arr["+str(i)+"]) :=\n\t\t\t\tcase\n")
    if(i == size - 1):
        file.write("\t\t\t\t\tstate = b3 & j = "+str(i)+"  : aux;\n")
    elif(i == 0):
        file.write("\t\t\t\t\tstate = b3 & j = "+str(i + 1)+" : arr["+str(i + 1)+"];\n")
    else:
	file.write("\t\t\t\t\tstate = b3 & j = "+str(i + 1)+" : arr["+str(i + 1)+"];\n")
	file.write("\t\t\t\t\tstate = b3 & j = "+str(i)+" : aux;\n")
    file.write("\t\t\t\t\tTRUE : arr["+str(i)+"];\n\t\t\t\tesac;\n")  
    
  
file.write("LTLSPEC\n\tF state = b6\n")
file.write("LTLSPEC\n\tG (ord -> F state = b6)\n")
file.write("LTLSPEC\n\tF ord\n")
file.write("LTLSPEC\n\tord = FALSE U state != b6\n")

file.close()

os.system("./NuSMV Isort.smv")
