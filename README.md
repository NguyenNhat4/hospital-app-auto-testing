# Facebook Chatbot Testing Framework

This project provides an automated testing framework for a Facebook page chatbot using Python, Pytest, and Playwright. It's designed to be a learning tool for understanding automated testing principles and best practices.

## Why This Approach? (Python + Pytest + Playwright)

While there are many chatbot testing tools like Botium, this project uses a Python-native stack for a few key reasons:

- **Real User Simulation (End-to-End Testing)**: By using Playwright to control a real web browser, we are simulating user interactions exactly as they happen. This allows us to test the entire system, from the user interface to the bot's backend logic.
- **No API Access Required**: This approach doesn't require developer access to the Facebook App or the Messenger Platform API. All you need is a standard Facebook user account, making it easier to get started.
- **Python-Native**: For a Python developer, using tools like `pytest` and `playwright` is natural. It keeps the entire project in one language and leverages the rich Python ecosystem.
- **Educational Value**: This setup is a fantastic, practical example of modern web automation and testing principles that are highly valuable in the software industry.

## Project Structure

Here's an overview of the files in this project:

- `README.md`: You are reading it! This is the central guide for the project.
- `requirements.txt`: Lists the Python dependencies required to run the project.
- `test_data.json`: Contains the test cases. We keep test data separate from test logic, which is a best practice.
- `config.py`: This is where you will store your secrets, like your Facebook username, password, and the URL of the page you want to test. (You will create this file yourself by copying `config.py.example`).
- `config.py.example`: An example file for you to copy.
- `test_chatbot.py`: The heart of the project. This Python script contains the automated tests.
- `.gitignore`: A standard file that tells the Git version control system which files to ignore.

## Setup Instructions

Follow these steps to get the testing framework running.

### 1. Prerequisites

- **Python**: Make sure you have Python 3.8 or newer installed on your system.
- **Virtual Environment (Recommended)**: It's a best practice to create a virtual environment to isolate project dependencies.
  ```bash
  # Create a virtual environment
  python -m venv venv

  # Activate it
  # On Windows
  .\venv\Scripts\activate
  # On macOS/Linux
  source venv/bin/activate
  ```

### 2. Install Dependencies

Install all the necessary Python packages using pip and the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

Playwright needs to download browser binaries (for Chrome, Firefox, etc.) that it will use for automation.

```bash
playwright install
```

### 4. Configure Your Credentials

Create your own configuration file by copying the example file.

```bash
# On Windows
copy config.py.example config.py
# On macOS/Linux
cp config.py.example config.py
```

Now, open `config.py` with a text editor and fill in your Facebook account's email/phone number, your password, and the full URL of the Facebook page whose bot you want to test.

**Security Warning**: Automating a personal social media account is against the terms of service of many platforms and can be risky. It is **highly recommended** to create a dedicated, separate Facebook account solely for testing purposes.

## Running the Tests

Once everything is set up, you can run the tests using `pytest` from your terminal.

```bash
pytest
```

Pytest will automatically discover the tests in `test_chatbot.py`, launch a browser, perform the login, and run through each test case defined in `test_data.json`. You will see the results directly in your terminal.

## Understanding the Code (`test_chatbot.py`)

The test script is structured to be readable and maintainable. Here are some key concepts it uses:

- **Pytest Fixtures (`@pytest.fixture`)**: Fixtures are functions that `pytest` runs before each test. We use a fixture to set up the Playwright browser and a new page for each test, ensuring that tests are isolated from each other.
- **Data-Driven Testing (`@pytest.mark.parametrize`)**: We use this `pytest` feature to run the same test function with different data. Our test function runs once for each test case (each object) in the `test_data.json` file. This is a powerful technique that avoids code duplication.
- **Explicit Waits**: Modern web applications load content dynamically. Instead of using fixed delays (like `time.sleep()`), which are unreliable, we use Playwright's "auto-waiting" feature. It waits for elements to be ready before interacting with them, making our tests more robust.
- **Page Object Model (Concept)**: While not a strict implementation, the structure of the tests leans towards the Page Object Model idea, where we define "locators" (CSS selectors) for page elements at the top. In a larger project, you would encapsulate interactions with a specific page into its own class. 