from sys import stdin

N, M = [int(x) for x in stdin.readline().rstrip().split()]
D = [[int(x) for x in stdin.readline().rstrip().split()] for _ in range(M)]
for d in D:
    if d[0] > d[1]:
        d[0], d[1] = d[1], d[0]

D.sort(key=lambda x: (x[0], x[1]))
left = -1
right = N
ans = 0

for d in D:
    left = max(d[0], left)
    right = min(d[1], right)
    if left >= right:
        ans += 1
        left = d[0]
        right = d[1]

print(ans + 1)
