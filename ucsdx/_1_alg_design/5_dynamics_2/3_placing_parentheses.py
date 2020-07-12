# Uses python3
def get_maximum_value(data):
    res = {(i, i+1): (int(data[i]), int(data[i])) for i in range(0, len(data), 2)}
    def recurse(io, ie, indent=0):
        if (io, ie) not in res:
            for im in range(io+1, ie, 2):
                recurse(io, im, indent+1)
                recurse(im+1, ie, indent+1)
            maxima = []
            minima = []
            for im in range(io + 1, ie, 2):
                a, b = res[(io, im)], res[(im+1, ie)]
                if data[im] == '+':
                    maxima.append(a[0] + b[0])
                    minima.append(a[1] + b[1])
                elif data[im] == '-':
                    maxima.append(a[0] - b[1])
                    minima.append(a[1] - b[0])
                elif data[im] == '*':
                    options = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
                    maxima.append(max(options))
                    minima.append(min(options))
                else:
                    raise Exception('Invalid operator.')
            res[(io, ie)] = (max(maxima), min(minima))
    recurse(0, len(data))
    return res[(0, len(data))][0]


if __name__ == "__main__":
    print(get_maximum_value(input()))
