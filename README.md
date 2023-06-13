# Taiko Client Dashboard

This application is a real-time dashboard for the Taiko Node Client.

![Node](app/doc/screenshots/node.png "Node")

![Proposer](app/doc/screenshots/proposer.png "Proposer")

![Prover](app/doc/screenshots/prover.png "Prover")

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
   git clone https://github.com/mehdibouzit/taiko-client-dashboard.git
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Build the Docker image (ensure Docker is installed):

   ```bash
   docker build -t dashboard .
   ```

## Usage with Docker

To run the application with Docker, execute the following command:

```bash
docker run -p 5006:5006 dashboard
```

After running the above command, you can access the application by navigating to `http://localhost:5006/dashboard` in your web browser.

## Usage without Docker

To run the application, follow these steps:

1. Make sure you have installed all the necessary dependencies listed in the `requirements.txt` file.

2. From the command line, execute the following command to launch the application:

   ```bash
   panel serve dashboard.py
   ```

   Make sure you are in the root directory of the application when running this command.

3. Once the application is launched, open a web browser and navigate to the following URL:

   ```
   http://localhost:5006/dashboard
   ```

   This will display the user interface of the application.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
