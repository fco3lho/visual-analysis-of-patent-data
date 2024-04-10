conjunto = ["A", "B", "C", "D"]

cont = 0

for i in range(len(conjunto)):
  for j in range(i+1, len(conjunto)):
    print(conjunto[i], conjunto[j])
    cont+=1

print("Contador:", cont)