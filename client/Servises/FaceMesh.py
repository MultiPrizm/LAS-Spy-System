import mediapipe as mp
import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
from sklearn.decomposition import PCA
from Servises.ConfigManager import DBManager
import json

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

def process_frame(frame):
    """Обробка кадру для отримання landmarks обличчя."""
    results = mp_face_mesh.process(frame)
    if results.multi_face_landmarks:
        return results.multi_face_landmarks[0].landmark
    return None

def select_user_from_face(db, face_landmarks, frame_width, frame_height):
    """Вибір користувача на основі схожості облич."""
    if face_landmarks is None:
        return None  # Якщо обличчя не знайдено
    
    face_vector = get_face_vector(normalize_landmarks(face_landmarks, frame_width, frame_height))
    users = db.getUsers()  # Отримуємо список користувачів
    
    best_match = None
    best_similarity = 0
    
    for user in users:
        print(user)  # Виведення користувача (можливо для дебагу)
        user_face_vector = get_face_vector_from_svg(user[1])  # Отримуємо вектор обличчя користувача
        similarity = face_comparator(face_vector, user_face_vector)  # Порівнюємо схожість
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = user[0]
    
    # Якщо схожість більша за 90%, повертаємо користувача
    return best_match if best_similarity > 0.9 else None

def normalize_landmarks(landmarks, width, height):
    """Нормалізація landmarks до розмірів зображення."""
    return np.array([[lm.x * width, lm.y * height, lm.z] for lm in landmarks])

def normalize_vector(face_vec):
    """Нормалізація вектора (перетворення в одиничний вектор)."""
    norm = np.linalg.norm(face_vec)
    if norm == 0:  # Якщо вектор має нульову довжину
        return face_vec
    return face_vec / norm

def get_face_vector(landmarks):
    """Перетворення landmarks у вектор."""
    if isinstance(landmarks, np.ndarray):
        return landmarks.flatten()
    elif hasattr(landmarks[0], 'x'):
        # Перетворення списку об'єктів Landmark в одновимірний масив
        return np.array([coord for lm in landmarks for coord in (lm.x, lm.y, lm.z)])
    else:
        raise ValueError("Unsupported landmarks format")

def get_face_vector_from_svg(user_face_data):
    """Отримуємо вектор з даних користувача (зображення чи SVG)."""
    # Це місце для розширення: тут можна додати обробку SVG чи інших даних користувача
    return np.array(user_face_data).flatten()

def compare_faces(face_vector1, face_vector2, method='cosine'):
    """Порівняння двох облич за допомогою різних методів."""
    face_vector1 = normalize_vector(face_vector1)
    face_vector2 = normalize_vector(face_vector2)
    
    if method == 'cosine':
        # Косинусна схожість
        return np.dot(face_vector1, face_vector2)  

    # Додаткові методи порівняння можуть бути додані тут
    return 0

def face_comparator(face1_vec, face2_vec):
    """Порівняння облич за допомогою косинусної схожості."""
    if face1_vec is None or face2_vec is None:
        return 0
    return compare_faces(face1_vec, face2_vec, method='cosine')

def save_face_vector_to_svg(face_vector):
    """Серіалізація багатовимірного масиву у формат JSON."""
    return json.dumps(face_vector.tolist())  # Перетворюємо масив в список та серіалізуємо його в JSON формат

def get_face_vector_from_svg(svg_face_vector):
    """Перетворює серіалізований рядок JSON назад у багатовимірний масив."""
    face_list = json.loads(svg_face_vector)  # Парсимо JSON рядок
    return np.array(face_list)  # Перетворюємо список назад в numpy масив