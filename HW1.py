import gzip
import simplejson
from matplotlib import pyplot as plt

userInfo={}
productInfo={}
quantity = {}
userId = "b'review/userId"
productId = "b'product/productId"

def parse(filename):
  f = gzip.open(filename, 'r')
  entry = {}
  for l in f:
    l = str(l.strip())
    colonPos = l.find(':')
    if colonPos == -1:
      yield entry
      entry = {}
      continue
    eName = l[:colonPos]
    rest = l[colonPos+2:].replace("'","")
    entry[eName] = rest
  yield entry

'''def countingSort(inputArray,maximum):
    arr = list(inputArray.values())
    maxElement= maximum
    countArrayLength = maxElement+1
    countArray = [0] * countArrayLength
    for el in arr: 
        countArray[el] += 1
    for i in range(1, countArrayLength):
        countArray[i] += countArray[i-1] 
    outputArray = [0] * len(arr)
    i = len(arr) - 1
    while i >= 0:
        currentEl = arr[i]
        countArray[currentEl] -= 1
        newPosition = countArray[currentEl]
        outputArray[newPosition] = currentEl
        i -= 1
    return outputArray
'''

def countingSort(inputArray,maxElement):
    countArrayLength = maxElement+1
    countArray = [0] * countArrayLength
    for el in inputArray: 
        countArray[inputArray[el]] += 1
    for i in range(1, countArrayLength):
        countArray[i] += countArray[i-1] 
    outputArray = [0] * len(inputArray)
    for el in inputArray:
        currentEl = inputArray[el]
        countArray[currentEl] -= 1
        newPosition = countArray[currentEl]
        outputArray[newPosition] = el
    return outputArray

def findMax(inputArray,keys,T):
  global quantity
  if T == 'u':
    maxNum = len(inputArray[keys])
    if keys == "unknow":
      for i in inputArray:
        quantity[i] = len(inputArray[i])
        if maxNum < len(inputArray[i]):
          maxNum = len(inputArray[i])
    else:
      for i in inputArray:
        if i == "unknown":
          continue
        quantity[i] = len(inputArray[i])
        if maxNum < len(inputArray[i]):
          maxNum = len(inputArray[i])
  #return maxNum
  elif T == 'p':
    maxNum = inputArray[keys[0]]
    for i in inputArray:
      if maxNum < inputArray[i]:
        maxNum = inputArray[i]
  return maxNum

for e in parse("C:\\Users\\user\\Desktop\\vscode\\datasincine\\Music.txt.gz"):
  if e.get(productId,0) == 0:
    continue
  if productInfo.get(e[productId],0) == 0:
    productInfo[e[productId]] = 0
  productInfo[e[productId]] += 1
  if userInfo.get(e[userId],0) == 0:
    userInfo[e[userId]] = set()
  userInfo[e[userId]].add(e[productId])

userId = list(userInfo.keys())
productId = list(productInfo.keys())
tolUser = len(userId)
tolProduct = len(productId)
print(f'Q1: {tolUser}')
print(f'Q2: {tolProduct}')

print(f"Q3 with unknown:{findMax(userInfo,userId[0],'u')}")
print(f"Q3 without unknown:{findMax(userInfo,userId[1],'u')}")

#medinum
maximum = findMax(productInfo,productId,'p')
print(maximum)
productId = countingSort(productInfo,maximum)
mid = int(len(productId)/2)
mid = int((productInfo[productId[mid]]+productInfo[productId[mid+1]])/2)
midUser = set()
for i in quantity:
  if quantity[i] == mid:
    midUser.add(i)
print(f'Q4 : midle number is {mid} \nThe first ten users Id are:{sorted(list(midUser))[:10]}')

barX=[]
numY=[]
for i in range(1,11):
  barX.append(productId[len(productId)-i])
  numY.append(productInfo[productId[len(productId)-i]])
plt.bar(range(len(barX)),numY)
plt.title("The most popular product")
plt.ylabel("the  number of products")
plt.xticks(range(len(barX)),barX)
plt.show()