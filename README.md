# Car Search Web Application

The Car Search Web Application is a web-based platform that allows users to search for both used and new cars based on various criteria such as make, model. The application provides autocomplete suggestions as the user types, making it easy to find the desired cars quickly. It utilizes FastAPI as the backend framework, SQLite as the database, and HTML/CSS/JavaScript for the frontend.

# Try Now
You can try the application now. Simple go to [Oogoocars Deta App](https://oogoocars-1-w2365740.deta.app/)

Visit API Documentation on [Oogoocars Deta App API Docs](https://oogoocars-1-w2365740.deta.app/docs/)

![image](/media/sc3.png) 
![image](/media/sc4.png) 
## Purpose and Scope

The purpose of this project is to create a user-friendly and efficient car search platform that helps users find their desired cars with ease. The application provides a seamless search experience with autocomplete functionality, allowing users to type in the car's name, make, or model and receive real-time suggestions. The scope of the project includes the development of both the frontend and backend components, as well as the integration with an SQLite database to store and retrieve car data.

## Features

The Car Search Web Application offers the following features:

1. Car Search: Users can search for cars by entering the car's name, make, model, or other criteria. The search feature provides real-time autocomplete suggestions to help users find the desired cars quickly.

2. Autocomplete: As the user types in the search input, the application provides autocomplete suggestions based on the available car data in the database. This feature enhances the search experience and improves usability.

3. Responsive UI: The frontend interface is designed to be responsive, ensuring that the application can be accessed and used effectively on various devices, including desktops, tablets, and mobile phones.

4. Load More: The application includes a "Load More" functionality that allows users to fetch additional cars as they scroll through the search results. This feature enhances usability and provides a seamless browsing experience.

5. Scalability: The application is designed to be scalable to handle a large number of concurrent users without compromising performance. Techniques such as caching of requests using reddis (an in memory caching mechanism), asynchronous request handling and efficient database queries have been implemented to support scalability.

## Scalability Implementation

To achieve scalability, the following techniques and approaches have been implemented:

1. **FastAPI Framework**: FastAPI is a high-performance Python web framework that leverages asynchronous programming and utilizes the Starlette framework. It is designed to handle high-concurrency workloads, making it well-suited for scaling the backend server.

2. **SQLite Database**: SQLite is a lightweight and fast database engine. While SQLite has limitations compared to more robust databases, it can handle millions of simultaneous users when appropriately optimized. Proper indexing, query optimization, and database connection pooling techniques have been implemented to improve performance and scalability.

3. **Caching**: FastAPI Caching technique using Redis with the `fastapi-cache2[redis]` package, is implemented to cache frequently accessed data, reducing the load on the database and improving response times. Caching helps to scale the application by minimizing the need for repeated expensive database queries.

4. **Frontend Optimization**: The frontend only triggers the backend search when user is finished typing, ensuring limited, necessary requests to  the API.

## Installation and Setup

To run the Car Search Web Application locally, follow these steps:

1. Clone the repository: `git clone https://github.com/zShanCS/car-search`

2. Install dependencies: `pip install -r requirements.txt`

3. Start the backend server: `uvicorn main:app --reload`

4. Access the application: Open your web browser and visit `http://localhost:8000`


## License

This project is licensed under the [MIT License](./LICENSE).
