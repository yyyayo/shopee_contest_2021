N, K = list(map(int, input().split()))
V = list(map(int, input().split()))


count = 0

for i in range(N):
	for j in range(N-i):
		sum = 0
		for k in range(i+1):
			sum += V[k+j]
		if sum/(i+1) >= K:
			count += 1

print(count)