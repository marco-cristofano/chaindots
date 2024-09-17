# Python Challenge

Design and implement a Django API for a social media platform that allows users to create posts, follow other users, and comment on posts.

##### The API should include (but may not be limited to) the following models:
    
- User: Represents a user on the platform. Include fields for username, email, password, and followers/following relationships.
- Post: Represents a user's post. Include fields for the author (foreign key to User model), content, and timestamps (date created).
- Comment: Represents a comment on a post. Include fields for the author (foreign key to User model), post (foreign key to Post model), and content.


##### Implement the following endpoints:
    
1. **GET** /api/users/: Retrieve a list of all users.
2. **GET** /api/users/{id}/: Retrieve details of a specific user. Including number of total posts, number of total comments, followers and following.
3. **POST** /api/users/{id}/follow/{id}: Set first id user as follower of second id user.
4. **POST** /api/users/: Create a new user.
5. **GET** /api/posts/: Retrieve a list of all posts ordered from newest to oldest from all users, with pagination and filters. The filters to implement are: author_id, from_date, to_date. None of the filters is compulsory. The pagination should be achieved with the following parameters: page_size (default = 20), page_number (default = 1)
6. **GET** /api/posts/{id}/: Retrieve details of a specific post with it's last three comments included and the information of it's creator.
7. **POST** /api/posts/: Create a new post.
8. **GET** /api/posts/{id}/comments/: Retrieve all comments for a specific post.
9. **POST** /api/posts/{id}/comments/: Add a new comment to a post.

- Ensure that all endpoints require authentication. Implement token-based authentication using Django's built-in authentication system.

- Optimize the ORM queries to minimize the number of database hits and improve performance.

- Implement appropriate indexing and constraints on database fields to optimize query performance.
- Optimize complex queries involving multiple models and relationships.

- Write unit tests to ensure the API endpoints and ORM queries are functioning correctly.

- Use Django REST framework for building the API.

### Submission

- Provide the source code of your Django project, including all necessary files and folders.
- Include a README file with instructions on how to set up and run the project.
- Briefly explain the optimizations applied to the ORM queries and any challenges faced during the implementation.

### Evaluation Criteria
    
- Correctness: Verify that the API endpoints are functioning as expected and that the ORM queries are optimized.
- Code Quality: Assess the overall code organization, adherence to best practices, and proper use of Django REST framework.
- Optimized Queries: Evaluate the effectiveness of the applied optimizations and their impact on query performance.
- Testing: Check the presence of unit tests and their coverage of the API endpoints and ORM queries.
