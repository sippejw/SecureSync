from api import WormholeAPI

w = WormholeAPI()

res = w.receive("3-test-test-test")
print(res)
