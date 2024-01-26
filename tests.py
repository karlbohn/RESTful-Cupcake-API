from unittest import TestCase

from app import app
from models import db, Cupcake

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()


CUPCAKE_DATA = {
    "flavor": "Birthday Cake",
    "size": "Large",
    "rating": 10,
    "image": "https://www.thecreativebite.com/wp-content/uploads/2016/05/Best-Birthday-Cupcakes-The-Creative-Bite-5-copy.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "Bacon",
    "size": "4",
    "rating": 6,
    "image": "https://www.barleyandsage.com/wp-content/uploads/2022/09/maple-bacon-cupcakes-1200x1200-1.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "Birthday Cake",
                        "size": "Large",
                        "rating": 10,
                        "image": "https://www.thecreativebite.com/wp-content/uploads/2016/05/Best-Birthday-Cupcakes-The-Creative-Bite-5-copy.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "Birthday Cake",
                        "size": "Large",
                        "rating": 10,
                        "image": "https://www.thecreativebite.com/wp-content/uploads/2016/05/Best-Birthday-Cupcakes-The-Creative-Bite-5-copy.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "Bacon",
                    "size": "4",
                    "rating": 6,
                    "image": "https://www.barleyandsage.com/wp-content/uploads/2022/09/maple-bacon-cupcakes-1200x1200-1.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)
