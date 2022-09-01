import random
import math
from stringprep import in_table_c11
def HL_TF(u):
    return 1/(1+math.exp(-u))

def OL_TF(u):
    return 1/(1+math.exp(-u))

def templist(l1, l2):
    l = len(l1)
    k = []
    for item1, item2 in zip(l1, l2):
        value = item1+item2
        k.append(k)
    return k

if __name__ == '__main__':
    I = 4
    O = 1
    H = int(input("enter the number of hidden layer neurons  >> "))
    print(H)
    learning_rate = 0.7
    data_I = []
    with open("inputfile.txt") as myfile:
        for line in myfile:
            row_data = [float(item.strip()) for item in line.split()]
            data_I.append(row_data)
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    for item in data_I:
        for i in range(len(item)):
            if i == 0:
                l1.append(item[i])
            elif i == 1:
                l2.append(item[i])
            elif i == 3:
                l3.append(item[i])
            else:
                l4.append(item[i])
# -----------------------Target values ---------------------
    Target_output = []
    with open("Target_values.txt") as file1:
        for line in file1:
            Target_output.append(float(line))
    maxi = max(Target_output)
    mini = min(Target_output)
    for i in range(len(Target_output)):
        Target_output[i] = 0.1+0.8*((Target_output[i]-mini)/(maxi-mini))
    max_value = max(l1)
    min_value = min(l1)
    for i in range(len(l1)):
        l1[i] = 0.1+0.8*((l1[i]-min_value)/(max_value-min_value))
    max_value = max(l2)
    min_value = min(l2)
    for i in range(len(l2)):
        l2[i] = 0.1+0.8*((l2[i]-min_value)/(max_value-min_value))
    max_value = max(l3)
    min_value = min(l3)
    for i in range(len(l3)):
        l3[i] = 0.1+0.8*((l3[i]-min_value)/(max_value-min_value))
    max_value = max(l4)
    min_value = min(l4)
    for i in range(len(l4)):
        l4[i] = 0.1+0.8*((l4[i]-min_value)/(max_value-min_value))

    dat = []
    for i1, i2, i3, i4 in zip(l1, l2, l3, l4):
        temp = []
        temp.append(i1)
        temp.append(i2)
        temp.append(i3)
        temp.append(i4)
        dat.append(temp)
# ----------------------Final normalized data is -------------------------
    for item in dat:
        item.insert(0, 1)
    p = len(dat)
    min = -1
    max = 1
    # --------------------------Random V is ------------------------------
    print("\nv is -->")
    v = []
    for i in range(H):
        v1 = []
        for j in range(5):
            v1.append(min + (max-min)*random.random())
        v.append(v1)

    print(v)
# ------------------------------Random W is ---------------------------------
    print("\nw is -->")
    w = []
    for i in range(O):
        v2 = []
        for j in range(H+1):
            v2.append(min + (max-min)*random.random())
        w.append(v2)
    print(w)

    tol = 10**(-2)
    print(tol)
    filename = open("final_Result.txt", "w")
    filename.write("Normalized data : \n")
    for item in dat:
        filename.write(str(item))
        filename.write("\n")

    filename.write("\nnormalized target values : \n")
    for item in Target_output:
        filename.write(str(item))
        filename.write("\n")

    filename.write("\nInitial random w :\n ")
    for item in w:
        filename.write(str(item))
        filename.write("\n")
    filename.write("\n")

    filename.write("\nInitial random v :\n ")
    for item in v:
        filename.write(str(item))
        filename.write("\n")
    filename.write("\n")

    kiter = 0
    while True:
        HL_input = []
        for item1 in dat:
            for item2 in v:
                sum = 0
                for i in range(len(item1)):
                    sum += item1[i]*item2[i]
                HL_input.append(sum)

        HL_outputs = []
        for item in HL_input:
            HL_outputs.append(HL_TF(item))

        HL_outputs2 = []
        k = 1
        temp = []
        for i in range(len(HL_outputs)):
            temp.append(HL_outputs[i])
            k += 1
            if k > H:
                k = 1
                HL_outputs2.append(temp)
                temp = []

        for item in HL_outputs2:
            item.insert(0, 1)

        OL_inputs = []
        for item1 in HL_outputs2:
            for item2 in w:
                sum = 0
                for i in range(len(item1)):
                    sum += item1[i]*item2[i]

                OL_inputs.append(sum)

        OL_output = []
        for item in OL_inputs:
            OL_output.append(OL_TF(item))

        diff = []
        for item1, item2 in zip(Target_output, OL_output):
            diff.append(math.fabs(item1-item2))
        myerror = 0
        for item in diff:
            myerror += (item**2)/2
        myerror = myerror/p
        print("error  --->", myerror)
        filename.write("\nerror ---> ")
        filename.write(str(myerror))
        filename.write("\n")

        delw = []
        for j in range(H+1):
            value = 0
            for h in range(p):
                value = value+(Target_output[h]-OL_output[h]) * \
                    OL_output[h]*(1-OL_output[h])*HL_outputs2[h][j]
            value = (learning_rate/p)*value
            delw.append(value)

        delv = []
        for k in range(H):
            tempmat = []
            for i in range(5):
                tempvalue = 0
                for h in range(p):
                    tempvalue += (Target_output[h]-OL_output[h])*OL_output[h]*(
                        1-OL_output[h])*delw[k+1]*HL_outputs[h]*(1-HL_outputs[h])*dat[h][i]

                tempvalue = tempvalue*(learning_rate/p)
                tempmat.append(tempvalue)

            delv.append(tempmat)

        print("\n")
        finalw = []
        for i in range(len(w)):
            for j in range(len(w[0])):
                finalw.append(w[i][j]+delw[j])

        w[0] = finalw
        finalv = []
        for item1, item2 in zip(v, delv):
            templist1 = []
            for i in range(len(item1)):
                templist1.append(item1[i]+item2[i])
            finalv.append(templist1)
        v = finalv
        print("Iteration  ",kiter)
        
        kiter = kiter+1
        if(myerror < tol):
            break

    filename.write("final result is \n")
    filename.write("w :")
    for item in w:
        filename.write(str(item))
    filename.write("\n")
    filename.write("v :")
    for item in v:
        filename.write(str(item))
        filename.write("\n")
    filename.write("\n")

    data_k = []
    with open("inputfile2.txt") as rk:
        for line in rk:
            row_data1 = [float(item.strip()) for item in line.split()]
            data_k.append(row_data1)

    lk1 = []
    lk2 = []
    lk3 = []
    lk4 = []
    for item in data_k:
        for i in range(len(item)):
            if i == 0:
                lk1.append(item[i])
            elif i == 1:
                lk2.append(item[i])
            elif i == 3:
                lk3.append(item[i])
            else:
                lk4.append(item[i])

    max_v1 = lk1[0]
    min_v1 = lk1[0]
    for item in lk1:
        if item > max_v1:
            max_v1 = item
        if min_v1 > item:
            min_v1 = item

    max_v2 = lk2[0]
    min_v2 = lk2[0]
    for item in lk2:
        if item > max_v2:
            max_v2 = item
        if min_v2 > item:
            min_v2 = item

    max_v3 = lk3[0]
    min_v3 = lk3[0]
    for item in lk3:
        if item > max_v3:
            max_v3 = item
        if min_v3 > item:
            min_v3 = item

    max_v4 = lk4[0]
    min_v4 = lk4[0]
    for item in lk4:
        if item > max_v4:
            max_v4 = item
        if min_v4 > item:
            min_v4 = item

    for i in range(len(lk1)):
        lk1[i] = 0.1+0.8*((lk1[i]-min_v1)/(max_v1-min_v1))

    for i in range(len(lk2)):
        lk2[i] = 0.1+0.8*((lk2[i]-min_v2)/(max_v2-min_v2))

    for i in range(len(lk3)):
        lk3[i] = 0.1+0.8*((lk3[i]-min_v3)/(max_v3-min_v3))

    for i in range(len(lk4)):
        lk4[i] = 0.1+0.8*((lk4[i]-min_v4)/(max_v4-min_v4))

    datk = []
    for item1, item2, item3, item4 in zip(lk1, lk2, lk3, lk4):
        tempk = []
        tempk.append(item1)
        tempk.append(item2)
        tempk.append(item3)
        tempk.append(item4)
        datk.append(tempk)
# ----------------------Final normalized data is -------------------------
    for item in datk:
        item.insert(0, 1)

    HL_inputk = []
    for item1 in datk:
        for item2 in v:
            sum = 0
            for i in range(len(item1)):
                sum += item1[i]*item2[i]
            HL_inputk.append(sum)

    HL_outputsk = []
    for item in HL_inputk:
        HL_outputsk.append(HL_TF(item))

    HL_outputs2k = []
    k = 1
    temp = []
    for i in range(len(HL_outputsk)):
        temp.append(HL_outputsk[i])
        k += 1
        if k > H:
            k = 1
            HL_outputs2k.append(temp)
            temp = []

    for item in HL_outputs2k:
        item.insert(0, 1)

    OL_inputsk = []
    for item1 in HL_outputs2k:
        for item2 in w:
            sum = 0
            for i in range(len(item1)):
                sum += item1[i]*item2[i]

        OL_inputsk.append(sum)

    OL_outputk = []
    for item in OL_inputsk:
        OL_outputk.append(OL_TF(item))

    print("testing outputs are\n")
    for item in OL_outputk:
        print(item)
    
    Target_outputk = []
    with open("Target_values2.txt") as file1k:
        for line in file1k:
            Target_outputk.append(float(line))

    maxi = Target_outputk[0]
    mini = Target_outputk[0]
    for item in Target_outputk:
        if maxi<item:
            maxi=item
        if mini>item:
            mini=item

    for i in range(len(Target_outputk)):
        Target_outputk[i] = 0.1+0.8*((Target_outputk[i]-mini)/(maxi-mini))

    print("testing target value are \n")
    for item in Target_outputk:
        print(item)
    
    
    diff = []
    for item1, item2 in zip(Target_output, OL_output):
        diff.append(math.fabs(item1-item2))
    myerror = 0
    for item in diff:
        myerror += (item**2)/2
    myerror = myerror/p
    print("testing error  --->", myerror)
    print("number of iterations in training are  ", kiter)
    print("code has worked properly")
