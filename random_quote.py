import inspirobot

print("-"*50)
flow = inspirobot.flow()
for quote in flow:
    print(quote.text, quote.image.url)
print("-"*50)
