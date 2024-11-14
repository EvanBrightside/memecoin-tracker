
# Memecoin Tracker

## Project Description

**Memecoin Tracker** is an API and web application that allows users to track data on popular memecoins, such as Dogecoin and Shiba Inu. The project provides information on the current price, market capitalization, and price changes over the last week. In the future, it will be expanded to include an investment recommendation system based on market data analysis and predictive models.

The project consists of three main components:

- **Backend (web)**: A FastAPI server, built with Python, which collects and processes data on memecoins.
- **Database (db)**: PostgreSQL, used for data storage and interaction with the backend.
- **Frontend**: A Next.js interface that visualizes the data and displays price trend charts.

## How to Run the Project Locally

To run this project, you’ll need [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/).

### Steps to Start:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/memecoin-tracker.git
    cd memecoin-tracker
    ```

2. Create a `.env` files in the root directory of the project, at the same level as `docker-compose.yml`, in the frontend directory and in the app directory. Add the following environment variables:

    `.env`

    ```env
    POSTGRES_USER=memcoadmin
    POSTGRES_PASSWORD=memcopassword
    POSTGRES_DB=memcodatabase
    ```

    `frontend/.env`

    ```env
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```

    `app/.env`

    ```env
    DATABASE_URL=postgresql://memcoadmin:memcopassword@db/memcodatabase
    FRONTEND_URL=http://localhost:3000
    ```

3. Start the project using Docker Compose:

    ```bash
    docker-compose up --build
    ```

   Docker Compose will start all three services:
   - **db** (PostgreSQL): Database for storing memecoin data.
   - **web** (FastAPI): Backend server built with Python, interacting with the CoinGecko API and the database.
   - **frontend** (Next.js): Client-side application, displaying information to the user.

4. After successful startup:
   - The backend will be available at: [http://localhost:8000](http://localhost:8000)
   - The frontend will be available at: [http://localhost:3000](http://localhost:3000)

### Stopping the Services

To stop all containers, use the following command:

```bash
docker-compose down
```

## Roadmap

**Current Features:**

- Display of the current price and market capitalization of popular memecoins.
- Price trend charts showing changes over the last week.

**Future Plans:**

1. **Predictive Modeling**: Use machine learning to predict memecoin prices.
2. **Recommendation System**: Based on forecasts and market data, the application will offer investment recommendations.
3. **Expand Memecoin Database**: Add more memecoins for analysis.
4. **Integrate with Other APIs**: Support for additional data sources to improve market insights.

In the future, this project will evolve into a recommendation system that assists users in evaluating investment opportunities in memecoins through comprehensive market data analysis.
