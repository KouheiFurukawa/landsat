from sys import stdin

N = int(stdin.readline().rstrip())
A = [int(x) for x in stdin.readline().rstrip().split()]
ans = 0

for i in range(N - 1):
    for j in range(i + 1, N):
        ans += A[i] * A[j]

print(ans)