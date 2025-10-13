import numpy as np
import math

# vcol = np.zeros((1,2))
# pxy = np.vstack([vcol]*3)
# pdq = np.zeros((3,2))

# pxy = np.array([[1000, 2000],[399.3908, 2265.0578],[-582.3429, 2173.3331]])
# pdq = np.array([[1866.0254, 1232.0508],[1470.4669, 1761.9022],[582.3429, 2173.3331]])

def konwersja_ukladow(pxy, pdq):
    (n, m) = pxy.shape

    sinusy = np.zeros(n)
    cosinusy = np.zeros(n)
    translacje = np.zeros((n,m))

    # wyznaczenie przesunięcia między poszczególnymi parami punktów
    # p21, p32, p13
    for i in range(0, n):
        nast_i = i+1
        if nast_i == n:
            nast_i = 0

        dxy = np.zeros(m)
        ddq = np.zeros(m)

        for j in range(0,m):
            # print(pxy[nast_i,j])
            # print(pxy[i,j])
            dxy[j] = pxy[nast_i,j] - pxy[i,j]
            ddq[j] = pdq[nast_i,j] - pdq[i,j]
        
        # print('dxy')
        # print(dxy)
        # print(ddq)

        # Rotacja
        sin_a = (ddq[0]*dxy[1] - dxy[0]*ddq[1]) / (ddq[0]**2 + ddq[1]**2)
        cos_a = (ddq[0]*dxy[0] + dxy[1]*ddq[1]) / (ddq[0]**2 + ddq[1]**2)

        sinusy[i] = sin_a
        cosinusy[i] = cos_a

        # print('from sine')
        # print(math.degrees(math.asin(sin_a)))
        # print('from cosine')
        # print(math.degrees(math.acos(cos_a)))

        R = np.array([[cos_a, -sin_a], [sin_a, cos_a]])

        # Translacja
        t = pxy[i].reshape((-1, 1)) - R@pdq[i].reshape((-1, 1))
        translacje[i] = t.reshape((1,-1))
        print('i = {}'.format(i))
        print(translacje)

    # print('sinusy: ')
    # print(sinusy)
    # print('cosinusy: ')
    # print(cosinusy)
    print('translacje: ')
    print(translacje)
    print(translacje)
    print(translacje[1])

    avg_sine = np.average(sinusy)
    avg_cos = np.average(cosinusy)
    avg_t = np.zeros(m)

    for i in range(0,n):
        for j in range(0,m):
            avg_t[j] += translacje[i,j]
            # print('t[{},{}] = {}'.format(i,j,translacje[i,j]))
            # print('avg_t[,{}] = {}'.format(j,avg_t[j]))
    for i in range(0,m):
        avg_t[i] /= n
        # print('avg_t[{}] = {}'.format(i,avg_t[i]))

    return avg_sine, avg_cos, avg_t

# avg_sine, avg_cos, avg_t = konwersja_wspolrzednych(pxy,pdq)

# print('sin: ' , avg_sine , ' -> ' , math.degrees(math.asin(avg_sine)))
# print('cos: ' , avg_cos , ' -> ' , math.degrees(math.acos(avg_cos)))
# print('t: ' , avg_t )

def konwertuj_wspolrzedne(sina, cosa, t, p1):
    (n,m) = p1.shape
    p2 = np.zeros((n,m))

    for i in range(0,n):
        p2[i,0] = p1[i,0]*cosa - p1[i,1]*sina + t[0]
        p2[i,1] = p1[i,0]*sina + p1[i,1]*cosa + t[1]
    
    return p2