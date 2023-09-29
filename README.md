# Stock Trading Platform

## Overview

Stock Trading Platform is a simulated, user-friendly web application built with Flask, allowing users to interact with real-time stock trading functionalities. Users can register an account, manage portfolios, execute buy/sell orders, and view transaction histories, providing an engaging and educative platform to understand stock trading.

## 🌟 Features

- **User Registration and Authentication:** Secure creation and access to user accounts.
- **Real-Time Stock Price Lookup:** Provides real-time stock price information.
- **Portfolio Management:** Enables users to view and manage their stock portfolios.
- **Buying and Selling Stocks:** Facilitates the buying and selling of stocks.
- **Transaction History View:** Allows users to view their transaction histories.
- **[Additional Feature(s)]:** [Any Additional Features]

## 🛠️ Installation and Setup

```sh
# Clone the repository
git clone https://github.com/evaristomat/finance-app.git
cd finance-app

# Install dependencies
pip install -r requirements.txt

# Run the application
flask run 
```

## 📖 Usage

### Registration/Login
- **Register:**
  - Navigate to `/register` to create a new account.
- **Login:**
  - Once registered, navigate to `/login` and input your credentials to access your account.
![Example Image](https://github.com/evaristomat/finance-app/blob/b070480de1466f25e6cc2bbcc688fbb71a77e375/png/1.png)

### Index/Portfolio
- **View Portfolio:**
  - After logging in, you will be redirected to `/` where you can view owned stocks, their current prices, and your remaining cash balance.
![Example Image](https://github.com/evaristomat/finance-app/blob/7a62fdca2812b4b3ebbc670a60a872dd4b25399b/png/3.png)


### Buy/Sell Stocks
- **Buy Stocks:**
  - Navigate to `/buy`, input the stock's symbol and the desired number of shares, and submit the form.
- **Sell Stocks:**
  - Navigate to `/sell`, select the stock from your portfolio, input the number of shares, and submit the form.

### Transaction History
- **View History:**
  - Navigate to `/history` to view details of all your transactions including stock symbols, share numbers, prices, and transaction times.
![Example Image](https://github.com/evaristomat/finance-app/blob/7a62fdca2812b4b3ebbc670a60a872dd4b25399b/png/2.png)

### Adding Cash
- **Add Cash:**
  - Navigate to `/addcash`, input the amount to be added to your cash balance, and submit the form.

## 📜 License

This project is open-source and is licensed under the MIT License. For more details, see [LICENSE](<Link to your LICENSE file>).

## 🌐 Contact

For any additional information or inquiries, please feel free to contact:
- **[Linkedin](https://www.linkedin.com/in/matheus-alves-evaristo/)**
  or
- **[GitHub](https://github.com/evaristomat)**

