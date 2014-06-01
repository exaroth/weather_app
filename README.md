##Weather app

Weather app is a simple script for getting basic weather information based on your location. It has been written mainly to work along with conky or other desktop notifiers.

### Basic usage

```shell
./weather.py
```

Will try to guess your location based on host ip address. This might not be reliable in some regions so it's better to define location manually

```shell
./weather.py -l "New York"
```
or 

```shell
./weather.py --location="New York"
```

will get weather information for New York city.

#### Additional options


* Get forecast for few days ahead (maximum of 15 days)

``` shell
./weather.py --forecast=10
```

or

``` shell
./weather.py -f 10
```
* Change system from metric to imperial

```shell
./weather.py -s imperial
```
or 
```shell
./weather.py --system=imperial
```

