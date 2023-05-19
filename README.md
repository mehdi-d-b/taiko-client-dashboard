# Real-time IoT Dashboard

This application is a real-time IoT dashboard that uses Panel, HoloViews, and Params to display and interact with the data. It fetches data periodically and updates the curves dynamically.

## Dependencies

- Python 3.7+
- Panel 0.12.1
- HoloViews 1.14.4
- Param 1.11.1
- Pandas
- NumPy
- Tornado

## Installation

To run the application, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/mehdibouzit/realtime-iot-dashboard-holoviz.git
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Build the Docker image (ensure Docker is installed):

   ```bash
   docker build -t hmi .
   ```

## Usage

To run the application with Docker, execute the following command:

```bash
docker run -p 5006:5006 hmi
```

After running the above command, you can access the application by navigating to `http://localhost:5006/hmi` in your web browser.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```

