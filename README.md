# Python/Django Challenge

This document contains:

- Instructions to start the service 
- System characteristics
- Comments on decisions made during development
- Optimizations performed
- Possible improvements

The resolution was based on the requirements found in the file [Challenge](./CHALLENGE.md).

## Instructions to start the service

***Requirements**: docker and docker-compose.*

1. Clone the repository.
2. Enter the docker folder
3. Execute:
    ```bash
    docker-compose build
    ```
4. Execute:
    ```bash
    docker-compose up -d
    ```
   The first time may fail to start because Django starts before PostgreSQL. If this happens run the command again.

- Running the tests
    ```bash
    docker exec -it social_media_platform_backend /bin/bash
    cd social_media_platform_project/
    python manage.py test --parallel
    ```
- Running coverage (in container)
    ```bash
    coverage run --source="." manage.py test
    coverage report
    ```
    <img title="Coverage" alt="coverage" src="./coverage.png">

- API Documentation: [Swagger](http://127.0.0.1:8081/swagger) *It is a basic implementation of documentation. You cannot test the endpoints from swagger, only view the documentation.*

- By default a “Social Media User” is created with username “admin” and password “admin”.
    ```bash
    curl -X POST 127.0.0.1:8081/login/ -d username=admin -d password=admin
    curl -X GET 127.0.0.1:8081/api/users/ -H "Authorization: Token <TOKEN>"
    ```

- System: [Site](http://127.0.0.1:8081/)


## System characteristics

The system has three services:
- Backend: Python/Django (4.2 LTS).
- Database: PostgreSQL.
- Web Server: Ngix.

*It was probably not necessary to use PostgreSQL or Nginx.*

## Comments on decisions made during development

- I generally avoided adding business logic to models and serializers. I preferred to develop services that contain the application logic “isolated” from the framework's own functionalities. Depending on the context of the system and its evolution this is correct.
Django Rest Framework induces to have logic in the models and serializers.
- The “Social media user” model inherits from the AbstractUser model provided by Django. This is completely questionable since I am mixing system logic with framework logic. The only benefit is simplicity for development and the efficiency of using a single table
- The standard for API parameter names was not specified. I decided to use the same names as the model attributes 
- The definition of the URLs are outside of the applications, this does not necessarily have to be so. For this example I considered that it was not the responsibility of each application to define its URLs.
- In general I used viewsets blocking some of their methods. However, it may be considered more appropriate to inherit directly from the appropriate mixins.
- For simplicity and to use some of the Django Rest Framework tools I incorporated several ModelSerializers. In case you need to improve the performance of some endpoint you can exclude them and take their functionality to the query in the database.
- For filtering and paging use tools provided by DRF, if more performance is required, custom development is possible.

## Optimizations performed

When using model serializers there is a risk that they run extra queries to obtain data. While extremely practical, they can be very inefficient.

1. To avoid this, use the **select_related** and **prefetch_related** tools to obtain the associated entities in the same query. This way you can avoid new queries later.

    An example of this

    ```python
        user = cls.model.objects.filter(
            id=social_media_user_id
        ).prefetch_related(
            'followed',
            'followers'
        ).annotate(
            total_posts=Count('posts', distinct=True),
            total_comments=Count('comments', distinct=True)
        ).get()
    ```

2. The above code also includes the use of the **Count** operator to count posts and comments in the same query.
   
3. Django Rest Framework provides functions like  *get_object* or *get_object_or_404*  that are very useful but inefficient because they get the instance from the base when it is not necessarily needed.

    Implement the function **exists_object_or_404** that performs an **exists** to the database and therefore is more efficient than getting the instance. 

    ```python
        def exists_object_or_404(model, id: int) -> bool:
            """
            Return True if object exists or raise 404 error.
            args:
                model: model class
                id: id of object
            return:
                bool: true if object exists
            """
            exists = model.objects.filter(id=id).exists()
            if exists:
                return True
            raise NotFound('No %s matches the given query.' % model._meta.object_name)

    ```

4. The following query may have originated in the Post model. However its origin is the Comment model to save a query to the Database.
   ```python
        @classmethod
        def get_all_comments(cls, post_id: int) -> QuerySet[Comment]:
            """Returns all comments of post.

            Args:
                post_id (int): id of post
            Returns:
                comments: queryset of comments
            """
            comments = Comment.objects.filter(
                post__id=post_id
            ).select_related(
                'author'
            ).order_by('-created_at')
            return comments
    ```

5. The created_at fields of the Comment and Post model were defined as indexes. Although this worsens the creation and update time, there is an advantage at the time of sorting.

## Possible improvements

- It is a good practice (in some cases) to prevent services from directly querying the database. In this case I did not implement repositories but it could be an improvement in the separation of responsibilities for the system.

- The following service can be made more efficient by directly receiving the “SocialMediaUser” instances. To do this in the API you must replace the exists_object_or_404 methods by get_object_or_404.
    ```python
        @classmethod
        def add_follow(cls, user_id: int, user_to_follow_id: int) -> None:
            """Adds user to follow.

            Args:
                user_id (int): id of user
                user_to_follow_id (int): id of user to follow
            """
            user = cls.model.objects.get(id=user_id)
            user_to_follow = cls.model.objects.get(id=user_to_follow_id)
            user.followed.add(user_to_follow)
            user.save()

    ```

- The retrieval of the last three comments of a post can probably be improved by performing subqueries on the initial query. In this case I just delegated that responsibility to the serializer.
