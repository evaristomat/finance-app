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
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository

# Install dependencies
pip install -r requirements.txt

# Run the application
flask run

## 📖 Usage

### **Registration/Login**
- **Register:**
   - Navigate to `/register` to create a new account.
- **Login:**
   - Once registered, navigate to `/login` and input your credentials to access your account.

### **Index/Portfolio**
- **View Portfolio:**
   - After logging in, you will be redirected to `/` where you can view owned stocks, their current prices, and your remaining cash balance.

### **Buy/Sell Stocks**
- **Buy Stocks:**
   - Navigate to `/buy`, input the stock's symbol and the desired number of shares, and submit the form.
- **Sell Stocks:**
   - Navigate to `/sell`, select the stock from your portfolio, input the number of shares, and submit the form.

### **Transaction History**
- **View History:**
   - Navigate to `/history` to view details of all your transactions including stock symbols, share numbers, prices, and transaction times.

### **Adding Cash**
- **Add Cash:**
   - Navigate to `/addcash`, input the amount to be added to your cash balance, and submit the form.

## 📜 License

This project is open-source and is licensed under the MIT License. For more details, see [LICENSE](<Link to your LICENSE file>).

## 🌐 Contact

For any additional information or inquiries, please feel free to contact:

- **[Your Name]**: <your.email@example.com>

   or

- **[GitHub](<Your GitHub Profile Link>)**
