# 3rd party dependencies
import cv2
import numpy as np

# project dependencies
from deepface import DeepFace
from deepface.models.demography import Age, Emotion, Gender, Race
from deepface.commons.logger import Logger

logger = Logger()


detectors = ["opencv", "mtcnn"]


def test_standard_analyze():
    img = "dataset/img4.jpg"
    demography_objs = DeepFace.analyze(img, silent=True)

    # return type should be list of dict for non batch input
    assert isinstance(demography_objs, list)

    for demography in demography_objs:
        assert isinstance(demography, dict)
        logger.debug(demography)
        assert demography["age"] > 20 and demography["age"] < 40
        assert demography["dominant_gender"] == "Woman"
    logger.info("✅ test standard analyze done")


def test_analyze_with_all_actions_as_tuple():
    img = "dataset/img4.jpg"
    demography_objs = DeepFace.analyze(
        img, actions=("age", "gender", "race", "emotion"), silent=True
    )

    for demography in demography_objs:
        logger.debug(f"Demography: {demography}")
        assert type(demography) == dict
        age = demography["age"]
        gender = demography["dominant_gender"]
        race = demography["dominant_race"]
        emotion = demography["dominant_emotion"]
        logger.debug(f"Age: {age}")
        logger.debug(f"Gender: {gender}")
        logger.debug(f"Race: {race}")
        logger.debug(f"Emotion: {emotion}")
        assert demography.get("age") is not None
        assert demography.get("dominant_gender") is not None
        assert demography.get("dominant_race") is not None
        assert demography.get("dominant_emotion") is not None

    logger.info("✅ test analyze for all actions as tuple done")


def test_analyze_with_all_actions_as_list():
    img = "dataset/img4.jpg"
    demography_objs = DeepFace.analyze(
        img, actions=["age", "gender", "race", "emotion"], silent=True
    )

    for demography in demography_objs:
        logger.debug(f"Demography: {demography}")
        assert type(demography) == dict
        age = demography["age"]
        gender = demography["dominant_gender"]
        race = demography["dominant_race"]
        emotion = demography["dominant_emotion"]
        logger.debug(f"Age: {age}")
        logger.debug(f"Gender: {gender}")
        logger.debug(f"Race: {race}")
        logger.debug(f"Emotion: {emotion}")
        assert demography.get("age") is not None
        assert demography.get("dominant_gender") is not None
        assert demography.get("dominant_race") is not None
        assert demography.get("dominant_emotion") is not None

    logger.info("✅ test analyze for all actions as array done")


def test_analyze_for_some_actions():
    img = "dataset/img4.jpg"
    demography_objs = DeepFace.analyze(img, ["age", "gender"], silent=True)

    for demography in demography_objs:
        assert type(demography) == dict
        age = demography["age"]
        gender = demography["dominant_gender"]

        logger.debug(f"Age: { age }")
        logger.debug(f"Gender: {gender}")

        assert demography.get("age") is not None
        assert demography.get("dominant_gender") is not None

        # these are not in actions
        assert demography.get("dominant_race") is None
        assert demography.get("dominant_emotion") is None

    logger.info("✅ test analyze for some actions done")


def test_analyze_for_preloaded_image():
    img = cv2.imread("dataset/img1.jpg")
    resp_objs = DeepFace.analyze(img, silent=True)

    # return type should be list of dict for non batch input
    assert isinstance(resp_objs, list)

    for resp_obj in resp_objs:
        assert isinstance(resp_obj, dict)
        logger.debug(resp_obj)
        assert resp_obj["age"] > 20 and resp_obj["age"] < 40
        assert resp_obj["dominant_gender"] == "Woman"

    logger.info("✅ test analyze for pre-loaded image done")


def test_analyze_for_different_detectors():
    img_paths = [
        "dataset/img1.jpg",
        "dataset/img5.jpg",
        "dataset/img6.jpg",
        "dataset/img8.jpg",
        "dataset/img1.jpg",
        "dataset/img2.jpg",
        "dataset/img1.jpg",
        "dataset/img2.jpg",
        "dataset/img6.jpg",
        "dataset/img6.jpg",
    ]

    for img_path in img_paths:
        for detector in detectors:
            results = DeepFace.analyze(
                img_path, actions=("gender",), detector_backend=detector, enforce_detection=False
            )
            # return type should be list of dict for non batch input
            assert isinstance(results, list)
            for result in results:
                assert isinstance(result, dict)
                logger.debug(result)

                # validate keys
                assert "gender" in result.keys()
                assert "dominant_gender" in result.keys() and result["dominant_gender"] in [
                    "Man",
                    "Woman",
                ]

                # validate probabilities
                if result["dominant_gender"] == "Man":
                    assert result["gender"]["Man"] > result["gender"]["Woman"]
                else:
                    assert result["gender"]["Man"] < result["gender"]["Woman"]


def test_analyze_for_batched_image_as_list_of_string():
    img_paths = ["dataset/img1.jpg", "dataset/img2.jpg", "dataset/couple.jpg"]
    expected_faces = [1, 1, 2]

    demography_batch = DeepFace.analyze(img_path=img_paths, silent=True)
    # return type should be list of list of dict for batch input
    assert isinstance(demography_batch, list)

    # 3 image in batch, so 3 demography objects
    assert len(demography_batch) == len(img_paths)

    for idx, demography_objs in enumerate(demography_batch):
        assert isinstance(demography_objs, list)
        assert len(demography_objs) == expected_faces[idx]
        for demography_obj in demography_objs:
            assert isinstance(demography_obj, dict)

            assert demography_obj["age"] > 20 and demography_obj["age"] < 40
            assert demography_obj["dominant_gender"] in ["Woman", "Man"]

    logger.info("✅ test analyze for batched image as list of string done")


def test_analyze_for_batched_image_as_list_of_numpy():
    img_paths = ["dataset/img1.jpg", "dataset/img2.jpg", "dataset/couple.jpg"]
    expected_faces = [1, 1, 2]

    imgs = []
    for img_path in img_paths:
        img = cv2.imread(img_path)
        imgs.append(img)

    demography_batch = DeepFace.analyze(img_path=imgs, silent=True)
    # return type should be list of list of dict for batch input
    assert isinstance(demography_batch, list)

    # 3 image in batch, so 3 demography objects
    assert len(demography_batch) == len(img_paths)

    for idx, demography_objs in enumerate(demography_batch):
        assert isinstance(demography_objs, list)
        assert len(demography_objs) == expected_faces[idx]
        for demography_obj in demography_objs:
            assert isinstance(demography_obj, dict)

            assert demography_obj["age"] > 20 and demography_obj["age"] < 40
            assert demography_obj["dominant_gender"] in ["Woman", "Man"]

    logger.info("✅ test analyze for batched image as list of numpy done")


def test_analyze_for_numpy_batched_image():
    img1_path = "dataset/img4.jpg"
    img2_path = "dataset/couple.jpg"

    # Copy and combine the same image to create multiple faces
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    expected_num_faces = [1, 2]

    img1 = cv2.resize(img1, (500, 500))
    img2 = cv2.resize(img2, (500, 500))

    img = np.stack([img1, img2])
    assert len(img.shape) == 4  # Check dimension.
    assert img.shape[0] == 2  # Check batch size.

    demography_batch = DeepFace.analyze(img, silent=True)
    # return type should be list of list of dict for batch input

    assert isinstance(demography_batch, list)

    # 2 image in batch, so 2 demography objects.
    assert len(demography_batch) == 2

    for i, demography_objs in enumerate(demography_batch):
        assert isinstance(demography_objs, list)

        assert len(demography_objs) == expected_num_faces[i]
        for demography in demography_objs:  # Iterate over faces
            assert isinstance(demography, dict)

            assert demography["age"] > 20 and demography["age"] < 40
            assert demography["dominant_gender"] in ["Woman", "Man"]

    logger.info("✅ test analyze for multiple faces done")


def test_batch_detect_age_for_multiple_faces():
    # Load test image and resize to model input size
    img = cv2.resize(cv2.imread("dataset/img1.jpg"), (224, 224))
    imgs = [img, img]
    results = Age.ApparentAgeClient().predict(imgs)
    # Check there are two ages detected
    assert len(results) == 2
    # Check two faces ages are the same in integer format（e.g. 23.6 -> 23）
    # Must use int() to compare because of max float precision issue in different platforms
    assert np.array_equal(int(results[0]), int(results[1]))
    logger.info("✅ test batch detect age for multiple faces done")


def test_batch_detect_emotion_for_multiple_faces():
    # Load test image and resize to model input size
    img = cv2.resize(cv2.imread("dataset/img1.jpg"), (224, 224))
    imgs = [img, img]
    results = Emotion.EmotionClient().predict(imgs)
    # Check there are two emotions detected
    assert len(results) == 2
    # Check two faces emotions are the same
    assert np.array_equal(results[0], results[1])
    logger.info("✅ test batch detect emotion for multiple faces done")


def test_batch_detect_gender_for_multiple_faces():
    # Load test image and resize to model input size
    img = cv2.resize(cv2.imread("dataset/img1.jpg"), (224, 224))
    imgs = [img, img]
    results = Gender.GenderClient().predict(imgs)
    # Check there are two genders detected
    assert len(results) == 2
    # Check two genders are the same
    assert np.array_equal(results[0], results[1])
    logger.info("✅ test batch detect gender for multiple faces done")


def test_batch_detect_race_for_multiple_faces():
    # Load test image and resize to model input size
    img = cv2.resize(cv2.imread("dataset/img1.jpg"), (224, 224))
    imgs = [img, img]
    results = Race.RaceClient().predict(imgs)
    # Check there are two races detected
    assert len(results) == 2
    # Check two races are the same
    assert np.array_equal(results[0], results[1])
    logger.info("✅ test batch detect race for multiple faces done")
