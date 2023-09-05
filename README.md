# FILDZ CYBEROS WS2812 (NeoPixel) Library

Fully asynchronous WS2812 library for CYBEROS.

## Features

* Completely asynchronous.
* 8 pre-defined colors.
* Adjustable brightness.

## Setup

1. Download and extract .zip file contents to fildz_neopixel folder.
2. Upload fildz_neopixel folder to your MicroPython powered device.

## Usage

```Python
from machine import Pin
import uasyncio as asyncio
import fildz_cyberos as cyberos
from fildz_neopixel import NeoPixel


async def main():
    await cyberos.init()
    pxl = NeoPixel(Pin(14, Pin.OUT), 1)  # One RGB LED on pin 14.
    await pxl.set_color(index=0, color=pxl.C_RED)  # Set first LED to red color.
    await cyberos.run_forever()

asyncio.run(main())
```

## Documentation

The documentation for this library is currently a work in progress. It will be available soon to provide detailed explanations of the library's API, usage examples, and best practices.

## Contributing

FILDZ CYBEROS is an open-source project that thrives on community contributions. We welcome developers to contribute to the project by following the MIT license guidelines. Feel free to submit pull requests, report issues, or suggest enhancements to help us improve the project further.

## Acknowledgment 

We are immensely thankful to the [MicroPython](https://github.com/micropython/micropython) community for developing and maintaining this incredible open-source project. Their dedication and hard work have provided us with a powerful and versatile platform to build upon.
