import cv2
import dlib
import os
import uuid
import face_recognition
import pickle

# Path to save face encodings
ENCODINGS_PATH = 'output/encodings.pkl'

def load_encodings():
    """Load existing face encodings."""
    if os.path.exists(ENCODINGS_PATH):
        with open(ENCODINGS_PATH, 'rb') as f:
            return pickle.load(f)
    return {}

def save_encodings(encodings):
    """Save face encodings to a file."""
    with open(ENCODINGS_PATH, 'wb') as f:
        pickle.dump(encodings, f)

def detect_faces_and_save(image_path, output_folder='output'):
    detector = dlib.get_frontal_face_detector()
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 1)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    face_encodings = face_recognition.face_encodings(rgb_image)
    known_encodings = load_encodings()
    match_count = 0

    for i, rect in enumerate(faces):
        x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
        face_encoding = face_encodings[i]

        matches = face_recognition.compare_faces(list(known_encodings.values()), face_encoding)
        name = None

        if True in matches:
            match_index = matches.index(True)
            name = list(known_encodings.keys())[match_index]
            color = (0, 0, 255)  # Red rectangle for matched faces
            match_count += 1
        else:
            name = str(uuid.uuid4())
            known_encodings[name] = face_encoding
            color = (0, 255, 0)  # Green rectangle for new faces

        face_image = image[y:y+h, x:x+w]
        face_filename = os.path.join(output_folder, f"{name}.jpg")
        cv2.imwrite(face_filename, face_image)
        
        # Draw rectangle and put text with the saved name/ID
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        if name:  # Use the ID/name of the matched face
            cv2.putText(image, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    save_encodings(known_encodings)
    return image, len(faces), match_count
