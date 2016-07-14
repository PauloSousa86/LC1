import os;
tamanho = int(input("Tamanho do array: "))                
arr = []

for i in range (tamanho):
    arr.append(int(input("Numero: ")))

print(arr)

file = open("bsort.smv", "w")
file.write("MODULE main\n\n")
file.write("VAR\n\t")
file.write("arr : array 0 .. " + str(tamanho -1) + " of {")
x = list(set(arr))
for i in range (len(x)):
    file.write(str(x[i]))
    if(i < len(x) - 1): 
        file.write(",")
    else: 
        file.write("};\n")

file.write("\ti : 0 .. "+str(tamanho-1)+";\n")
file.write("\tj : 0 .. "+str(tamanho-2)+";\n")

        
file.write("\taux : {")
for i in range (len(x)):
    file.write(str(x[i]))
    if(i < len(x) - 1): 
        file.write(",")
    else: 
        file.write("};\n")

file.write("\tstate : {b1,b3,b4,b5,b6,b7};\n")
file.write("DEFINE\n\tord := ")
for i in range (tamanho - 1):
    file.write("arr["+str(i)+"] <= arr["+str(i+1)+"]")
    if(i < tamanho - 2): file.write(" & ")
    else: file.write(";\n")

file.write("\nASSIGN\n")
file.write("\tinit(state) := b1;\n\tinit(i) := 0;\n\tinit(j) := 0;\n")
file.write("\tinit(aux) := arr[0];\n")
for i in range(tamanho):
    file.write("\tinit(arr["+str(i)+"]) := "+str(arr[i])+";\n")

file.write("\tnext(state) :=\n\t\t\t\tcase\n\t\t\t\t\tstate = b1 & i < "+str(tamanho)+" : b3;\n")
file.write("\t\t\t\t\tstate = b3 & arr[j] > arr[j + 1] : b4;\n")
file.write("\t\t\t\t\tstate = b3 & arr[j] <= arr[j + 1] : b5;\n")
file.write("\t\t\t\t\tstate = b3 & j >= "+str(tamanho)+" - i - 1: b6;\n")
file.write("\t\t\t\t\tstate = b4 : b5;\n")
file.write("\t\t\t\t\tstate = b5 & j + 1 < "+str(tamanho)+" - i - 1: b3;\n")
file.write("\t\t\t\t\tstate = b5 & j + 1 >= "+str(tamanho)+" - i - 1: b6;\n")
file.write("\t\t\t\t\tstate = b6 & i + 1 < "+str(tamanho)+" : b1;\n")
file.write("\t\t\t\t\tstate = b6 & i + 1 >= "+str(tamanho)+" : b7;\n")
file.write("\t\t\t\t\tTRUE : state;\n")
file.write("\t\t\t\tesac;\n")
file.write("\tnext(aux) :=\n\t\t\t\tcase\n\t\t\t\t\tstate = b3 : arr[j];\n\t\t\t\t\tTRUE : aux;\n\t\t\t\tesac;\n")
file.write("\tnext(i) :=\n\t\t\t\tcase\n\t\t\t\t\tstate = b6 & i < "+str(tamanho-1)+": i + 1;\n\t\t\t\t\tTRUE : i;\n\t\t\t\tesac;\n")
file.write("\tnext(j) :=\n\t\t\t\tcase\n\t\t\t\t\tstate = b1 : 0;\n\t\t\t\t\tstate = b5 & j < "+str(tamanho-2)+": j + 1;\n\t\t\t\t\tTRUE : j;\n\t\t\t\tesac;\n")
for i in range (tamanho):
    file.write("\tnext(arr["+str(i)+"]) :=\n\t\t\t\tcase\n")
    if(i < tamanho - 1):
        file.write("\t\t\t\t\tstate = b4 & j = "+str(i)+" : arr[j+1];\n")
    if(i > 0):
        file.write("\t\t\t\t\tstate = b4 & j = "+str(i-1)+"  : aux;\n")
    file.write("\t\t\t\t\tTRUE : arr["+str(i)+"];\n\t\t\t\tesac;\n")  
    
  
file.write("LTLSPEC\n\tF state = b7\n")
file.write("LTLSPEC\n\tG (ord -> F state = b7)\n")
file.write("LTLSPEC\n\tF ord\n")
file.write("LTLSPEC\n\tord = FALSE U state != b7\n")

file.close()

os.system("./NuSMV bsort.smv")
