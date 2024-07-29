import unittest
from app.utils import detect_faces

class TestFaceDetection(unittest.TestCase):
    def test_detect_faces(self):
        image_path = 'resources/sample.jpg'
        result = detect_faces(image_path)
        self.assertIsNotNone(result)
        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()
