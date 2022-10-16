
# Bardi Led Automation

Automation for BARDI Bluetooth Light Bulb 9W RGBWW. use ADB automation need to use android smartphone :D

## Result 

https://user-images.githubusercontent.com/59155826/196045133-6918f7fb-30ea-4539-8260-ebe6d2fb4da1.mp4

## Feature

| Name             | Status              |
| ----------------- | ------------------------- |
| Change Color  | ✅ |
| On / Off Device | ✅ |
| Change Brightness | ✅ |
| Connection via Wifi / USB | ✅ |
| Change Theme | ✅ |

## Run Locally

Clone the project

```bash
  git clone https://github.com/sandrocods/Bardi-Led-Automation
```

Go to the project directory

```bash
  cd Bardi-Led-Automation
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Start the example

```bash
  cd example
  python3 connection.py
```


## Enable Connection ADB via Wifi

- Connect usb cable to your phone
- Open cmd
- Type: adb tcpip 5555
- Get your phone ip address

How to connect multiple android devices with ADB over wifi : 

- [Tutorial Stackoverflow](https://stackoverflow.com/a/43973839)

## API Reference

#### Connect Device
```python3

# Via Wifi
connector_bardi = BardiConnector(
    timeout=10.0,
    connection_type="wifi",
    address="192.168.0.161:5555"
)

# Via USB
connector_bardi = BardiConnector(
    timeout=10.0,
    connection_type="usb"
)
```

Output :
```python3
    {
        "status": True,
        "message": "Device connected"
    }
```

#### Get all color 

```python3
   print(connector_bardi.location_color)
```
Output :
```python3
  {'green': (0.693, 0.598), 'pink': (0.144, 0.447), 'blue': (0.769, 0.396), 'lime': (0.258, 0.595), 'cyan': (0.802, 0.545)}
```

#### Get all brightness
```python3
   print(connector_bardi.brightness)
```
Output :
```python3
  {'50': (0.529, 0.727), '100': (0.815, 0.672), '1': (0.182, 0.671), '25': (0.331, 0.715), '75': (0.655, 0.717)}
```

#### Get Theme by Music
```python3
  connector_bardi.get_theme_by_music()
  print(connector_bardi.theme_data)
```
Output :
```python3
  [{'theme_name': 'Music rhythm', 'theme_location': (887, 608)}, {'theme_name': 'Game', 'theme_location': (887, 608)}, {'theme_name': 'Romantic', 'theme_location': (887, 608)}]
```

#### Get Default Theme
```python3
    connector_bardi.get_theme()
    print(connector_bardi.theme_data)
```
Output :
```python3
  [{'theme_name': 'Good Night', 'theme_location': (397, 448)}, {'theme_name': 'Leisure', 'theme_location': (864, 448)}, {'theme_name': 'Gorgeous', 'theme_location': (383, 725)}, {'theme_name': 'Dream', 'theme_location': (860, 725)}, {'theme_name': 'Sunflower', 'theme_location': (386, 1003)}, {'theme_name': 'Grassland', 'theme_location': (889, 1003)}]
```

#### unlist color
```
  [
      'white',
      'half white',
      'sepia'
  ]
```
