[![CodeFactor](https://www.codefactor.io/repository/github/wacrex/py-rpi_pwm_controller/badge)](https://www.codefactor.io/repository/github/wacrex/py-rpi_pwm_controller) [![DeepSource](https://deepsource.io/gh/WaCrex/Py-RPi_PWM_Controller.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/WaCrex/Py-RPi_PWM_Controller/?ref=repository-badge)

# Py-RPi_PWM Controller

![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) __WARNING!__ This is an early development release, any use of this script is at your own risk! ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+)

---

The project originally started off as a custom script for the [NESPi-4 Fan Control](https://mini-mods.com/product/nespi-4-fan-control/) PCB,
but was later changed to be used with the official [Raspberry Pi 4 Case Fan](https://www.raspberrypi.org/products/raspberry-pi-4-case-fan/) instead.

The script will not only turn the fan on/off, but also adjust the fan speed according to the temperature using a fan profile.

## Installation

1. Go to the [Getting started](https://www.raspberrypi.org/products/raspberry-pi-4-case-fan/) section on the official website and follow the first 5 steps except for the 4:th step where you should instead connect the cables like this:

   ![Fan Pinout](pinout.png)

2. Next install the fan controller python script:

   ```bash
   wget -qO- https://raw.githubusercontent.com/WaCrex/Py-RPi_PWM_Controller/master/install.sh | sudo bash -
   ```

## Fan Profiles

The script comes with 3 fan profiles: `silent`, `linear` & `cool`. With `linear` being the default preset.

![Fan Profiles](fan_profiles.png)

## Configuration

The python script is by default looking for a json-file with the same name as the python script, by default this should be fan_ctrl.json.

/opt/fan_ctrl/fan_ctrl.json:

```json
{
    "profile": "linear",
    "gpio_pin": 18,
    "pwm_freq": 100,
    "profiles": {
        "silent": [
            40, 40, 41, 41, 42, 42, 43, 44,
            45, 46, 47, 49, 51, 53, 55, 57,
            59, 61, 63, 65, 67, 70, 73, 76,
            79, 82, 86, 89, 93, 96, 100],
        "linear": [
            40, 42, 44, 46, 48, 50, 52, 54,
            56, 58, 60, 62, 64, 66, 68, 70,
            72, 74, 76, 78, 80, 82, 84, 86,
            88, 90, 92, 94, 96, 98, 100],
        "cool": [
            40, 44, 47, 51, 54, 58, 61, 64,
            67, 70, 73, 75, 77, 79, 81, 83,
            85, 87, 89, 91, 93, 94, 95, 96,
            97, 98, 98, 99, 99, 100, 100]
    }
}
```

|Option|Default|Description|
|:-|:-|:-|
|`profile`|`linear`|*The name of the profile currently in use (must be listed under profiles).*|
|`gpio_pin`|`18`|*The GPIO Pin that the fan's PWM cable is connected to.*|
|`pwm_freq`|`100`|*The frequency of the PWM signal.*|
|`profiles`||*A dictionary of fan profiles, with Duty Cycle values (%) for the temperatures 50-80°C. The values must be between 0-100% and decimals aren't allowed.*|
