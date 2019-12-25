from sys import stdin
import bisect

N = int(stdin.readline().rstrip())
L = [int(x) for x in stdin.readline().rstrip().split()]
ans = 0
L.sort()
for i in range(1, N):
    for j in range(i):
        ans += max(bisect.bisect_left(L, L[i] + L[j]) - i - 1, 0)

print(ans)
