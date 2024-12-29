import mediapipe as mp
import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import cosine_similarity # type: ignore

def normalize_landmarks(landmarks, width, height):
    normalized_landmarks = []
    for landmark in landmarks:
        normalized_landmarks.append([landmark.x * width, landmark.y * height, landmark.z])
    return np.array(normalized_landmarks)

# Функція для отримання вектора обличчя
def get_face_vector(landmarks):
    face_vector = []
    for landmark in landmarks:
        face_vector.extend([landmark.x, landmark.y, landmark.z])
    return np.array(face_vector)

# Порівняння обличчя
def compare_faces(face_vector1, face_vector2, method='euclidean'):
    if method == 'euclidean':
        return euclidean(face_vector1, face_vector2)
    elif method == 'cosine':
        return cosine_similarity([face_vector1], [face_vector2])[0][0]
    elif method == 'manhattan':
        return np.sum(np.abs(face_vector1 - face_vector2))
    
def face_comparator(face1, face2):

    if face1.multi_face_landmarks is not None and face2.multi_face_landmarks is not None:
        face1_vec = get_face_vector(face1.multi_face_landmarks[0].landmark)
        face2_vec = get_face_vector(face2.multi_face_landmarks[0].landmark)

        similarity_score = compare_faces(face1_vec, face2_vec, method='cosine')

        print(similarity_score)

        return similarity_score

def save_face_vector_to_svg(face_vector):
    
    return ','.join(map(str, face_vector))

def get_face_vector_from_svg(svg_face_vector):

    return np.array([float(x) for x in svg_face_vector.split(',')])