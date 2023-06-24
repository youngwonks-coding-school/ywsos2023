import datetime
from flask_restx import Namespace, Resource


posts = Namespace('posts', description="Operations related to posts")


@posts.route("/get-posts")
class Posts(Resource):
    def get(self):
        # TODO Replace hardcoded data with posts from database
        return [
            {
                "description": "Leftovers from party. Mostly unopened",
                "location": "1234 Main St, San Francisco, CA 94123",
                "user": "bob",
                "time": str(datetime.datetime.now()),
            },
            {
                "description": "Unsold donuts from the bakery.",
                "location": "8923 Main St, San Francisco, CA 94123",
                "user": "jeff",
                "time": str(datetime.datetime.now()
                            - datetime.timedelta(days=3, hours=4, minutes=1)),
            },
            {
                "description": "Leftover pizza from the office party.",
                "location": "210 Main St, Livermore, CA 94123",
                "user": "bob",
                "time": str(datetime.datetime.now()
                            - datetime.timedelta(days=1, hours=2, minutes=1)),
            },
            {
                "description": "Food bought from Costco to donate. Unopened and new.",
                "location": "2390 Fast St, Fresno, CA 90123",
                "user": "jeremy",
                "time": str(datetime.datetime.now()
                            - datetime.timedelta(days=2, hours=1, minutes=1)),
            },
            {
                "description": "Three unopened cakes from bakery.",
                "location": "8291 Main St, San Francisco, CA 94123",
                "user": "jeffrey",
                "time": str(datetime.datetime.now()
                            - datetime.timedelta(days=9, hours=-3, minutes=-10)),
            },
        ]
