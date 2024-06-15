# WebEye

WebEye is a monitoring system that tracks changes on specified websites

## Overview

This project is a notification system that allows users to subscribe to notifications for specified websites. The system periodically takes screenshots of the websites, compares them using Mean Squared Error (MSE) to detect changes, and compares it to cached data stored in Redis. If any changes occur, users are notified via email. The system uses FastAPI for the backend, React for the frontend, Celery to manage background tasks, and RedisQueue for messaging.


## Features

- User authentication (registration, login, token refresh)
- Monitoring of specified websites
- Periodic website screenshot capturing and comparison using MSE
- User profile management

## Technologies Used

- **Backend**: FastAPI
- **Frontend**: React, Redux, MUI
- **Database**: PostgreSQL, Redis (for caching and messaging)
- **Task Management**: Celery
- **Email Notifications**: SMTP

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/MarkHmnv/WebEye.git
    cd WebEye
    ```

2. **Modify the environment variables**:

   Based on the .env.sample in both the api and client packages enter your data

3. **Run the application**:

     ```bash
     docker-compose up --build
     ```

## API Endpoints

### Authentication API

- **Register**: `POST /auth/register`
- **Login**: `POST /auth/login`
- **Refresh Token**: `POST /auth/refresh`

### Monitoring API

- **Create Monitoring**: `POST /monitoring`
- **Get All Monitors**: `GET /monitoring`
- **Delete Monitoring**: `DELETE /monitoring/{monitoring_id}`

### Users API

- **Get User Profile**: `GET /users/profile`
- **Update User Profile**: `PATCH /users/profile`
- **Delete User**: `DELETE /users/profile`
