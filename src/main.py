import time


def maxCharacter(operands, result):
    result = len(result[0])
    for x in operands:
        if (result < len(x)):
            result = len(x)
    return result


def printEquation(operands, result):
    maxChar = maxCharacter(operands, result)
    for i in range(len(operands)):
        spaceCount = maxChar - len(operands[i])
        if (i == len(operands) - 1):
            print((' ' * spaceCount) + operands[i] + '+')
        else:
            print((' ' * spaceCount) + operands[i])
    print("-" * maxChar)
    spaceCount = maxChar - len(result[0])
    print((' ' * spaceCount) + result[0])
    print('')


def isValidData(operands, result, data):
    startChar = []
    for x in operands:
        startChar.append(x[0])
    startChar.append(result[0][0])
    # convert to set to remove duplicate
    startChar = set(startChar)
    for c in startChar:
        if (int(data[c]) == 0):
            return False
    return True


def check(operands, result, data):
    intOperands = []
    intResult = []

    if (not(isValidData(operands, result, data))):
        return False

    for x in operands:
        operand = ''
        for c in x:
            operand += str(data[c])
        intOperands.append(int(operand))

    res = ''
    for c in result[0]:
        res += str(data[c])
    intResult.append(int(res))

    res = 0
    for x in intOperands:
        res += x

    return res == intResult[0]


def generateOperandsAndResult(operands, result, data):
    intOperands = []
    intResult = []

    for x in operands:
        operand = ''
        for c in x:
            operand += str(data[c])
        intOperands.append(operand)

    res = ''
    for c in result[0]:
        res += str(data[c])
    intResult.append(res)

    return [intOperands, intResult]


def nextNumbers(arr, i):
    if (int(arr[i]) + 1 <= 9 - (len(arr) - 1) + i):
        arr[i] = str(int(arr[i]) + 1)
        return True
    else:
        while (int(arr[i]) + 1 > 9 - (len(arr) - 1) + i and i > 0):
            i -= 1

        if (i != 0 or int(arr[i]) + 1 <= 9 - (len(arr) - 1) + i):
            arr[i] = str(int(arr[i]) + 1)
            while (i < len(arr) - 1 and int(arr[i]) + 1 <= 9 - (len(arr) - 1) + i + 1):
                arr[i + 1] = str(int(arr[i]) + 1)
                i += 1
            return True
        else:
            return False


def nextPermutation(arr):
    # find pivot
    pivotIndex = -1

    for i in range(len(arr), 1, -1):
        if (int(arr[i - 1]) > int(arr[i - 2])):
            pivotIndex = i - 2
            break

    if (pivotIndex == -1):
        # arr is the last permutation
        return False

    swapIndex = -1
    # find the rightmost sucessor to pivot in suffix
    for i in range(len(arr), pivotIndex + 1, -1):
        if (int(arr[i - 1]) > int(arr[pivotIndex])):
            swapIndex = i - 1
            break

    arr[pivotIndex], arr[swapIndex] = arr[swapIndex], arr[pivotIndex]

    suffix = []
    for i in range(len(arr), pivotIndex + 1, -1):
        suffix.append(arr[i - 1])

    for i in range(len(arr)):
        if (i > pivotIndex):
            arr[i] = suffix[i - pivotIndex - 1]

    return True


def generateData(arr, characters):
    data = {}
    for c in characters:
        data[c] = arr[0]
        arr = arr[1:]
    return data


def solver(operands, result):
    joinedString = ''
    for i in operands:
        joinedString += i
    joinedString += result[0]
    # get unique alphabet in operands and result
    characters = list(set(joinedString))
    if (len(characters) > 10):
        print("Tidak punya solusi")
        return

    startNumber = [i for i in range(len(characters))]
    cursor = len(startNumber) - 1
    startPermutation = list(startNumber)

    count = 1
    data = generateData(startPermutation, characters)
    if (check(operands, result, data)):
        correct = generateOperandsAndResult(operands, result, data)
        printEquation(correct[0], correct[1])
        return count
    else:
        while (nextPermutation(startPermutation)):
            count += 1
            data = generateData(startPermutation, characters)
            if (check(operands, result, data)):
                correct = generateOperandsAndResult(operands, result, data)
                printEquation(correct[0], correct[1])
                return count

        while (nextNumbers(startNumber, cursor)):
            count += 1
            startPermutation = list(startNumber)
            data = generateData(startPermutation, characters)
            if (check(operands, result, data)):
                correct = generateOperandsAndResult(operands, result, data)
                printEquation(correct[0], correct[1])
                return count
            else:
                while (nextPermutation(startPermutation)):
                    count += 1
                    data = generateData(startPermutation, characters)
                    if (check(operands, result, data)):
                        correct = generateOperandsAndResult(
                            operands, result, data)
                        printEquation(correct[0], correct[1])
                        return count

    return count


# main program
fname = str(input("Masukkan nama file: "))
f = open(fname)
print("")
f1 = f.readlines()

operands = []
result = []

failure = False

operandFinished = False
for i in f1:
    isDelimiter = '-' in i
    isLastOperand = '+' in i

    # remove space
    i = i.replace(" ", "")
    # remove enter
    i = i.rstrip("\n")

    isEmptyString = len(i) == 0

    if (isLastOperand):
        i = i.replace("+", "")

    if (not(isDelimiter) and not(isEmptyString)):
        # add to array
        if (operandFinished):
            result.append(i)

            # check for failure
            if (len(f1) < 4 or len(result) != 1 or len(operands) == 0):
                failure = True

            if (failure):
                print ("Input format wrong")
                break
            else:
                # timer start
                startTime = time.time()
                printEquation(operands, result)
                count = solver(operands, result)
                # timer end
                endTime = time.time()
                print("Total waktu: {:.3f} detik".format(endTime-startTime))
                print("Total tes: {:d}".format(count))
                print("")

                operandFinished = False
                operands = []
                result = []

        else:
            operands.append(i)

    # check if last operand
    if (isLastOperand):
        operandFinished = True
