import app
import unittest
import json
from random import randint

mocked_value = randint(0, 255)


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()



    def test_01_put_wrong_data(self):
        headers = [("Content-Type", "application/json")]
        data = "{'wrong data pla pla ..'}"
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)
        self.assertEqual(rv.status_code, 400)

    def test_02_put_good_data(self):
        headers = [("Content-Type", "application/json")]
        data = json.dumps({"value": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)
        rv_object = json.loads(rv.data)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv_object["value"], mocked_value)

    def test_03_put_good_data_with_expire(self):
        headers = [("Content-Type", "application/json")]
        data = json.dumps({"value": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put(f"/keys?expire_in=60", headers=headers, data=data)
        rv_object = json.loads(rv.data)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv_object["value"], mocked_value)

    def test_07_exist_key(self):
        headers = [("Content-Type", "application/json")]
        data = json.dumps({"check_value": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)

        rv = self.app.head(f"/keys/check_value/", headers=headers)
        self.assertEqual(rv.status_code, 302)

    def test_08_not_exist_key(self):
        headers = [("Content-Type", "application/json")]
        data = json.dumps({"check_value": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)

        rv = self.app.head(f"/keys/check/")
        self.assertEqual(rv.status_code, 404)



    def test_04_get_data(self):
        headers = [("Content-Type", "application/json")]
        data = json.dumps({"value": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)

        rv = self.app.get(f"/keys/value/", headers=headers)

        rv_object = json.loads(rv.data)

        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv_object["value"], str(mocked_value))

    def test_05_get_all_data(self):
        headers = [("Content-Type", "application/json")]
        data = json.dumps({"value": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)
        data = json.dumps({"value2": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)
        data = json.dumps({"value3": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)

        rv = self.app.get(f"/keys", headers=headers)
        rv_object = json.loads(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv_object["value"], str(mocked_value))
        self.assertEqual(rv_object["value2"], str(mocked_value))
        self.assertEqual(rv_object["value3"], str(mocked_value))

    def test_06_get_all_data_with_filter(self):
        headers = [("Content-Type", "application/json")]
        data = json.dumps({"valye": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)
        data = json.dumps({"val": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)
        data = json.dumps({"value": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)

        rv = self.app.get(f"/keys??filter=va$", headers=headers)
        rv_object = json.loads(rv.data)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv_object["valye"], str(mocked_value))
        self.assertEqual(rv_object["val"], str(mocked_value))
        self.assertEqual(rv_object["value"], str(mocked_value))



    def test_09_delete_specific_key(self):
        headers = [("Content-Type", "application/json")]
        data = json.dumps({"value": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)

        data = json.dumps({"value2": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)

        rv = self.app.get("/keys/value/", headers=headers)
        rv_object = json.loads(rv.data)
        self.assertEqual(rv_object["value"], str(mocked_value))

        rv = self.app.delete("/keys/value/", headers=headers)
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get(f"/keys/value/", headers=headers)
        rv_object = json.loads(rv.data)
        self.assertNotEqual(rv_object["value"], str(mocked_value))

        rv = self.app.get("/keys/value2/", headers=headers)
        print(rv)
        rv_object = json.loads(rv.data)
        print(rv_object)
        self.assertEqual(rv_object["value2"], str(mocked_value))

    def test_10_delete_all(self):
        headers = [("Content-Type", "application/json")]
        data = json.dumps({"value": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)

        data = json.dumps({"value2": mocked_value})
        headers.append(("Content-Length", len(data)))
        rv = self.app.put("/keys", headers=headers, data=data)

        rv = self.app.get("/keys/value/", headers=headers)
        rv_object = json.loads(rv.data)
        self.assertEqual(rv_object["value"], str(mocked_value))

        rv = self.app.delete("/keys", headers=headers)
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get(f"/keys/value/", headers=headers)
        rv_object = json.loads(rv.data)
        self.assertNotEqual(rv_object["value"], str(mocked_value))

        rv = self.app.get("/keys/value2/", headers=headers)
        rv_object = json.loads(rv.data)
        self.assertNotEqual(rv_object["value2"], str(mocked_value))


if __name__ == "__main__":
    unittest.main()
