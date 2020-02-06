# Inspirobot API

A Python3 api wrapper for [InspiroBot](https://inspirobot.me/)

### Requirements
* Python3.5 +
* Requests

### Install
Using PyPi (Pip)
```shell script
python3 -m pip install inspiro
```
Using Git
```shell script
python3 -m pip install git+<GIT_URL>
```
Manual
```shell script
git clone <GIT_URL> inspiro_python
cd inspiro_python
python3 -m pip -r requirements.txt
python3 -m pip install .
```

## Usage
#### Generating a classic Quote Image
```python
import inspirobot  # Import the libary
quote = inspirobot.generate()  # Generate Image
print(quote.url)  # Print the url
```
#### Using the mindfullness (flow) API
```python
import inspirobot  # Import the libary
flow = inspirobot.flow()  # Generate a flow object
for quote in flow:
    print(quote.text)
```
#### Spamming the mindfullness (flow) API
```python
import inspirobot  # Import the libary
flow = inspirobot.flow()  # Generate a flow object
for i in range(0, 100):
    for quote in flow:
        print(quote.text, quote.image.url)
    flow.new()
    print("-"*50)
```

##### HTTP Mode
Does your work/school network use https interception? Mine sure does!
```python
import inspirobot
inspirobot.HTTPS = False
```
That should fix it

