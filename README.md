# RECYCLYOPS

## Overview

RECYCLYOPS is a smart waste management system that leverages AI-powered material recognition, object tracking, and interactive feedback mechanisms to optimize waste disposal and recycling. The system integrates multiple hardware components, including cameras, motion sensors, displays, and speakers, to provide an intuitive and educational user experience.

## Hardware Requirements

To set up RECYCLYOPS, you will need the following hardware components:

- **Raspberry Pi 5** (or compatible model with necessary GPIO/I2C support)
- **IMX500 Camera** (for AI-powered image capture and object recognition)
- **Ultrasonic Motion Sensor** (for detecting object placement)
- **16x2 I2C LCD Display** (for visual feedback)
- **USB Speaker** (for text-to-speech output)
- **Power Supply for Raspberry Pi**
- **Jumper Wires** (for connecting components)

## Features

- **Face Display:** Displays expressions and feedback messages using an LCD.
- **Hardware Integration:** Supports various hardware modules such as cameras, motion sensors, speakers, and displays.
- **Material Recognition:** Identifies different types of waste materials using AI.
- **Object Tracking:** Tracks objects using motion detection algorithms.
- **Text-to-Speech:** Generates verbal responses for user interaction.
- **Utility Functions:** Handles configuration, logging, and JSON parsing.

## Project Structure
```
RECYCLYOPS/
├── face_display/                # Handles display of facial expressions
│   ├── expressions.json         # Predefined face expressions
│   ├── face_display.py          # Manages LCD face display
├── hardware/                    # Contains drivers for different hardware components
│   ├── cameras/                 # Camera integration
│   │   ├── imx500_camera.py     # IMX500 AI camera integration
│   ├── displays/                # LCD display integration
│   │   ├── LCD_16x2_display.py  # 16x2 LCD Display management
│   ├── motion_sensor/           # Motion detection using ultrasonic sensors
│   │   ├── ultrasonic_motion_sensor.py # Ultrasonic motion sensor handling
│   ├── speakers/                # USB speaker support
│   │   ├── USB_speaker.py       # USB speaker sound management
│   ├── hardware_config.json     # Hardware configuration settings
├── material_recognition/        # AI-powered material classification
│   ├── client.py                # OpenAI client for material recognition
│   ├── prompt_output.py         # Parses OpenAI API responses
│   ├── utils.py                 # Utility functions for processing images
├── object_tracking/             # Motion detection and object tracking
│   ├── object_tracker.py        # Tracks objects using sensors and cameras
│   ├── motiondetection.py       # Detects motion in images for tracking
├── text_to_speech/              # Generates speech responses
│   ├── comment_generator.py     # Generates contextual feedback messages
│   ├── responses.json           # Predefined responses for correct/incorrect sorting
│   ├── speech_manager.py        # Manages speech output queue
│   ├── tts.py                   # Google TTS integration for spoken feedback
├── utils/                       # Utility scripts for configuration and logging
│   ├── configuration.py         # Loads hardware configuration settings
│   ├── custom_logger.py         # Custom logger for debugging and tracking
│   ├── json_reader.py           # Reads and parses JSON files
├── .env                         # Environment variables (API_KEY required)
├── .gitignore                   # Git ignore file
├── main.py                      # Entry point of the application
├── README.md                    # Project documentation
├── requirements.txt              # Dependencies and required packages
```
## Installation

To set up the project, follow these steps:

1. Clone the repository:
	```
	git clone https://github.com/your-repo/RECYCLYOPS.git
	cd RECYCLYOPS
	```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the environment variables:
    ```bash
    cp .env.example .env
    ```
    Edit the .env file and add your OpenAI API key:
    ```python
    API_KEY="your_key_here"
    ```

4. Configure the LCD screen:

    - Connect the LCD screen as follows:

        - GND to any GND pin

        - VDD to any 5V pin

        - SDA to the I2C pin (GPIO2)

        - SCL to the I2C pin (GPIO3)

    - Enable I2C on your Raspberry Pi:
        ```bash
        sudo raspi-config
        ```
        Navigate to `3 Interface Options > P5 I2C`, enable it, then reboot:
        ```bash
        sudo reboot
        ```
        
    - Find the I2C address:
        ```bash
        sudo i2cdetect -y 1
        ```
        Set the found address in `hardware_config.json` under `"I2C_LCD_ADDRESS"`.

5. Configure the Ultrasonic Motion Sensor:

    - Connect the motion sensor as follows:

        - GND to any GND pin

        - VCC to any 5V pin

        - TRIG to GPIO22

        - ECHO to GPIO23

    - If any of the GPIO pins for the LCD or motion sensor are changed, update the `hardware_config.json` file accordingly:
        ```json
        {
        "I2C_LCD_ADDRESS": 39,
        "TRIG_PIN": 22,
        "ECHO_PIN": 23
        }
        ```
6. Run the application:
    ```bash
    python main.py
    ```

## Contributors

| | | | |
|-|-|-|-|
| <img src="https://avatars.githubusercontent.com/u/65859589?v=4" width="100px;"/><br>[Jeffrey Bringolf](https://www.linkedin.com/in/jeffreybringolf/) | <img src="https://media.licdn.com/dms/image/v2/D4E03AQHqQuMhIE2kEA/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1713570493957?e=1744243200&v=beta&t=MZ9wC1pn6R8smZg6DbFXw0KyROGtdprbudZ1_SSneBo" width="100px;"/><br>[Olivier Demers](https://www.linkedin.com/in/olivier-dmrs/) | <img src="https://media.licdn.com/dms/image/v2/C4E03AQFjltrdwGDx8w/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1652230341532?e=1744243200&v=beta&t=9L0Dso-vuh4ROX44iFE-ycRyTk7kVJTr-MCBaBmbxDE" width="100px;"/><br>[Abdessalam Aithaqi](https://www.linkedin.com/in/abdessalamaithaqi/) | <img src="https://media.licdn.com/dms/image/v2/D4E03AQHBbkTRAfCR_w/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1682204524530?e=1744243200&v=beta&t=iCyyEfclVTgcspa3H769qYERnu2bNgCVkgefD6g7Qic" width="100px;"/><br>[Biko-Higiro Ndabwunze](https://www.linkedin.com/in/biko-higiro-ndabwunze-44ab4423b/) |
| Worked on object tracking, material recognition, AI, and API development. | Contributed to object tracking, material recognition, AI, and API development. | Developed hardware modules, text-to-speech, face display, and comment generation. | Worked on text-to-speech functionality, collaborated on hardware implementation, and developed the database backend. |
