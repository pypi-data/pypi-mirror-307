from blue_objects import objects
from blue_objects.logger.image import log_image_hist
from blue_objects.tests.test_graphics import test_image
from blue_objects.env import DUMMY_TEXT


def test_log_image_hist(test_image):
    object_name = objects.unique_object()

    assert log_image_hist(
        test_image,
        range=(0, 255.0),
        header=[DUMMY_TEXT for _ in range(4)],
        footer=[DUMMY_TEXT for _ in range(2)],
        filename=objects.path_of(
            filename="log.png",
            object_name=object_name,
        ),
    )
