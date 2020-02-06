import inspirobot
import random

print("-"*50)
flow = inspirobot.flow()
for quote in flow:
    print(quote.text)
print("-"*50)