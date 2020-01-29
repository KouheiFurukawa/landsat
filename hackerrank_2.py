from sys import stdin

S = [int(x) for x in stdin.readline().rstrip().split(',')]
ans = ''
for i in range(len(S)):
    if S[i] == S[i - 1] or i % 2 == 1:
        if len(ans) > 0:
            ans += ','
        ans += str(S[i])

print(ans)
