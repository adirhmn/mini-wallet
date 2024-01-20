<a name="readme-top"></a>

[![GitHub contributors](https://img.shields.io/github/contributors/adirhmn/mini-wallet)](https://github.com/adirhmn/mini-wallet/graphs/contributors)
[![GitHub forks](https://img.shields.io/github/forks/adirhmn/mini-wallet)](https://github.com/adirhmn/mini-wallet/network)
[![GitHub stars](https://img.shields.io/github/stars/adirhmn/mini-wallet)](https://github.com/adirhmn/mini-wallet/stargazers)

<br />
<div align="center">
  <h3 align="center">Mini Wallet</h3>

  <p align="center">
    "Mini Wallet" application is a REST API designed to provide digital wallet services to users. Through this API, users can easily perform deposit (adding funds) and withdrawal (withdrawal of funds) operations from their digital wallets.
    <br />
    <a href="https://github.com/adirhmn/mini-wallet"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/adirhmn/mini-wallet/issues">Report Bug</a>
    ·
    <a href="https://github.com/adirhmn/mini-wallet/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
      <li><a href="#key-features">Key Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#how-to-running-project">How to Running Project</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

"Mini Wallet" application is a REST API designed to provide digital wallet services to users. Through this API, users can easily perform deposit (adding funds) and withdrawal (withdrawal of funds) operations from their digital wallets.


### Key Features
<b>1. Initial Account</b>

Customer can create or sign to account by providing customer id.

<b>2. Authentication and Authorization</b>

The application provides authentication mechanisms to protect customer data.
Each request to the API needs to be authorized using an authentication token provided during init account.

<b>3. Deposit Funds</b>

Customer can deposit funds into their digital wallets by specifying the amount they want to deposit.After a successful deposit, the customer's wallet balance will be updated accordingly.

<b>4. Withdrawal of Funds</b>

Customer can withdraw funds from their digital wallets by specifying the amount they want to withdraw.The system will check the availability of funds and process the withdrawal if sufficient funds are present.

<b>5. Check Balance</b>

Customer can check their wallet balance at any time.

<b>6. Transaction History</b>

The application provides an endpoint to view the customer's transaction history, including deposits and withdrawals.

<b>7. Wallet Status</b>

Customer can enable or disable their wallets based on their preference.
When a wallet is disabled, no deposit or withdrawal transactions can be initiated.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]
* [![FastAPI][FastAPI]][FastAPI-url]
* [![SQLAlchemy][SQLAlchemy]][SQLAlchemy-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![Docker][Docker]][Docker-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Welcome to "Mini Wallet" API! This section will guide you through the process of getting started with wallet services.

Get a local copy up and running follow these simple example steps.

### Prerequisites

1. Git Installation:

Make sure Git is installed on your computer. If not, you can download and install it from [here](https://git-scm.com/).

2. Docker Installation:

Install Docker by following the instructions for your operating system from [here](https://docs.docker.com/desktop/install/windows-install/).

### How To Running Project

#### Clone Repository to Local

1. Copy Repository URL

    On the repository page, look for the `Code` or `Clone` button located at the top right. Click on the button and copy the displayed URL (usually in HTTPS or SSH format).

2. Open Terminal

   Open the terminal or command prompt on your computer.

3. Navigate to Destination Directory

   Use the `cd` command to navigate to the directory where you want to store the project. For example:

   ```bash
   cd path/to/destination/directory
   ```

4. Clone Repository

   Type the following command to clone the repository:

   ```bash
   git clone [Repository URL]
   ```

   Replace `[Repository URL]` with the URL

   ```bash
   git clone https://github.com/adirhmn/mini-wallet
   ```

5. Done!

   The project has now been successfully cloned to your computer. You can start working or exploring the code of the project.

#### Running Project with Docker Compose
1. Navigate to Project Directory

   After cloning the repository, navigate to the project directory:

   ```bash
   cd repository-directory
   ```
2. Create an .env file

    You can create it by changing the `.env-example` file to `.env`

3. Start Docker Compose

   Make sure Docker is installed and running on your system.
     Run the following command to start the application using Docker Compose:

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker images and start the containers in detached mode.
   Congratulations your app has been running at `http://localhost:8000` and you can checking status app by access `http://localhost:8000` and you will get response

   ```
   {
       "status": "success",
       "message": "App running well"
   }
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Running Unit Testing with Docker
1.  Open a New Terminal

    * Launch a new terminal window or tab on your computer.
    * Make sure Docker is running on your system.

2. List Running Containers

   - In the terminal, execute the command:
     ```
     docker container ls
     ```
   - You will see a response similar to the following example:
     ```
     CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                    NAMES
     5217500e60b1   mini_wallet-web        "sh -c 'uvicorn main…"   About an hour ago   Up About a minute   0.0.0.0:8000->8000/tcp   mini_wallet-web-1
     30d0a6339feb   postgres:12.0-alpine   "docker-entrypoint.s…"   2 hours ago         Up About a minute   5432/tcp                 mini_wallet-db-1
     ```
   - Note down `IMAGE` name from the list. In this example, the `IMAGE` is `mini_wallet-web`.

3. **Run Testing Command**

   - Replace `{IMAGE_NAME}` with the actual image name (from step 2) in the following command:
     ```
     docker run {IMAGE_NAME} sh -c "pytest"
     ```
   - For example, if your image name is `mini_wallet-web`, the command will be:
     ```
     docker run mini_wallet-web sh -c "pytest"
     ```
   - Execute the command in the terminal to run the API tests inside the Docker container.

4. **Observe Test Results**
   - The terminal will display the output of the tests. Ensure all tests pass and check for any error messages or failures.




<!-- USAGE EXAMPLES -->
## Usage

#### API Endpoints

Explore and interact with the Mini Wallet API using the following endpoints. You can use tools like [Postman](https://www.postman.com/) for a convenient API testing experience.

#### API Documentation

Access the detailed API documentation using Swagger at [http://localhost:8000/docs](http://localhost:8000/docs).

#### Postman Collection

To simplify API testing, you can use the provided Postman collection.

1. **Download Postman:**
   If you don't have Postman installed, you can download it [here](https://www.postman.com/downloads/).

2. **Import Collection:**
   Download Mini Wallet API Postman collection [here](https://github.com/adirhmn/mini-wallet/blob/main/Mini-Wallet.postman_collection.json), and import it into Postman.

3. **Set Environment Variables:**
   - Create a new environment in Postman.
   - Set the following variables:
     - `host`: `http://localhost:8000/api/v1/`
     - `token`: `[YOUR_TOKEN]`

4. **Explore and Test:**
   - Browse the available requests in the Mini Wallet API collection.
   - Update variables like `YOUR_TOKEN` with a valid token obtained from the Init API.

5. **Execute Requests:**
   - Execute requests to register a user, deposit funds, check balance, and more.



_For screenshot usage, please refer to the [Documentation](https://github.com/adirhmn/mini-wallet/tree/main/documentation)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[FastAPI]: https://img.shields.io/badge/FastAPI-000000?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-20232A?style=for-the-badge&logo=postgresql&logoColor=61DAFB
[PostgreSQL-url]: https://www.postgresql.org/
[SQLAlchemy]: https://img.shields.io/badge/SQLAlchemy-35495E?style=for-the-badge&logo=sqlalchemy&logoColor=4FC08D
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[Python]: https://img.shields.io/badge/Python-4A4A55?style=for-the-badge&logo=python&logoColor=61DAFB
[Python-url]: https://www.python.org/
[Docker]: https://img.shields.io/badge/Docker-0769AD?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
