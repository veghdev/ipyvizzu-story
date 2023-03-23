"""A module for testing the ipyvizzustory.storylib.story.Story class."""

import unittest
import unittest.mock
import os
import glob
from abc import ABC, abstractmethod

from ipyvizzu import Data, Style

from tests import Story, Slide, Step
from tests import (
    VIZZU_STORY,
    DISPLAY_TEMPLATE,
    DISPLAY_INDENT,
)


class TestHtml(ABC):
    """An abstract class for testing story html output."""

    hex: str = "123456789"
    """A number for mocking uuid."""

    @abstractmethod
    def story(self, *args, **kwargs):  # -> Story
        """An abstract method for returning a story instance."""

    def get_story(self):  # -> Story
        """
        A method for returning a test story instance.

        Returns:
            (Story): A test story instance.
        """

        story = self.story(data=Data.filter(None))
        story.add_slide(Slide(Step(Data.filter(None))))
        story.add_slide(Slide(Step(Data.filter('record.Function !== "Defense"'))))
        return story

    def get_vpd(self) -> str:
        """
        A method for returning a test Vizzu-Player data.

        Returns:
            A test data.
        """

        return (
            "{"
            + '"data": {"filter": null}, '
            + '"slides": ['
            + '[{"filter": null}], '
            + '[{"filter": record => { return (record.Function !== "Defense") }}]'
            + "]}"
        )

    def get_html(self) -> str:
        """
        A method for returning a test story html output.

        Returns:
            A test html output.
        """

        return DISPLAY_TEMPLATE.format(
            id="1234567",
            vizzu_attribute="",
            vizzu_story=VIZZU_STORY,
            vizzu_player_data=self.get_vpd(),
            chart_size="",
            chart_features="",
            chart_events="",
        )

    def get_html_with_size(self) -> str:
        """
        A method for returning a test story html output with size values.

        Returns:
            A test html output.
        """

        return DISPLAY_TEMPLATE.format(
            id="1234567",
            vizzu_attribute="",
            vizzu_story=VIZZU_STORY,
            vizzu_player_data=self.get_vpd(),
            chart_size="vizzuPlayer.style.cssText = 'width: 800px;height: 480px;'",
            chart_features="",
            chart_events="",
        )


class TestStoryInit(unittest.TestCase):
    """A class for testing Story. __init__ method."""

    def test_init_if_no_data_was_passed(self) -> None:
        """
        A method for testing Story.__init__ method if no data was passed.

        Raises:
            AssertionError: If TypeError is not occurred.
        """

        with self.assertRaises(TypeError):
            Story()  # type: ignore  # pylint: disable=no-value-for-parameter

    def test_init_if_no_data_was_set(self) -> None:
        """
        A method for testing Story.__init__ method if no data was set.

        Raises:
            AssertionError: If TypeError is not occurred.
        """

        with self.assertRaises(TypeError):
            Story(data={})  # type: ignore

    def test_init_if_not_valid_data_was_set(self) -> None:
        """
        A method for testing Story.__init__ method if not valid data was set.

        Raises:
            AssertionError: If TypeError is not occurred.
        """

        with self.assertRaises(TypeError):
            Story(data={"filter": None})  # type: ignore

    def test_init_if_data_was_set(self) -> None:
        """
        A method for testing Story.__init__ method if data was set.

        Raises:
            AssertionError: If the story dict is not correct.
        """

        self.assertEqual(
            Story(data=Data.filter(None)), {"data": {"filter": None}, "slides": []}
        )

    def test_init_if_no_style_was_set(self) -> None:
        """
        A method for testing Story.__init__ method if no style was set.

        Raises:
            AssertionError: If the story dict is not correct.
        """

        self.assertEqual(
            Story(data=Data.filter(None), style={}),  # type: ignore
            {"data": {"filter": None}, "slides": []},
        )

    def test_init_if_not_valid_style_was_set(self) -> None:
        """
        A method for testing Story.__init__ method if not valid style was set.

        Raises:
            AssertionError: If TypeError is not occurred.
        """

        with self.assertRaises(TypeError):
            Story(data=Data.filter(None), style={"style": None})  # type: ignore

    def test_init_if_style_was_set(self) -> None:
        """
        A method for testing Story.__init__ method if data was set.

        Raises:
            AssertionError: If the story dict is not correct.
        """

        self.assertEqual(
            Story(data=Data.filter(None), style=Style(None)),
            {"data": {"filter": None}, "style": None, "slides": []},
        )


class TestStoryAddSlide(unittest.TestCase):
    """A class for testing Story.add_slide method."""

    def test_add_slide_if_no_slide_was_set(self) -> None:
        """
        A method for testing Story.add_slide method if no slide was set.

        Raises:
            AssertionError: If TypeError is not occurred.
        """

        story = Story(data=Data.filter(None))
        with self.assertRaises(TypeError):
            story.add_slide({})  # type: ignore

    def test_add_slide_if_not_valid_slide_was_set(self) -> None:
        """
        A method for testing Story.add_slide method if not valid slide was set.

        Raises:
            AssertionError: If TypeError is not occurred.
        """

        story = Story(data=Data.filter(None))
        with self.assertRaises(TypeError):
            story.add_slide({"filter": None})  # type: ignore

    def test_add_slide_if_slides_were_set(self) -> None:
        """
        A method for testing Story.add_slide method if slides were set.

        Raises:
            AssertionError: If the story dict is not correct.
        """

        story = Story(data=Data.filter(None))
        story.add_slide(Slide(Step(Data.filter(None))))
        story.add_slide(Slide(Step(Data.filter(None))))
        self.assertEqual(
            story,
            {
                "data": {"filter": None},
                "slides": [[{"filter": None}], [{"filter": None}]],
            },
        )


class TestStoryUrlProperties(TestHtml, unittest.TestCase):
    """A class for testing story url releated properties."""

    def story(self, *args, **kwargs):
        """
        A method for returning a story instance.

        Args:
            *args: Non-keyword arguments.
            **kwargs: Keyword arguments.

        Returns:
            A story instance initialized with the given `args` and `kwargs`.
        """

        return Story(*args, **kwargs)


class TestStoryHtml(TestHtml, unittest.TestCase):
    """A class for testing story html releated methods."""

    def setUp(self):
        self.test_dir = os.path.dirname(os.path.realpath(__file__))

    def tearDown(self):
        file_list = glob.glob(self.test_dir + "/.test.*")
        for file_path in file_list:
            os.remove(file_path)

    def story(self, *args, **kwargs):
        """
        A method for returning a story instance.

        Args:
            *args: Non-keyword arguments.
            **kwargs: Keyword arguments.

        Returns:
            A story instance initialized with the given `args` and `kwargs`.
        """

        return Story(*args, **kwargs)

    def test_export_to_html(self) -> None:
        """
        A method for testing Story.export_to_html method.

        Raises:
            AssertionError: If the story html is not correct.
        """

        with unittest.mock.patch(
            "ipyvizzustory.storylib.story.uuid.uuid4", return_value=self
        ):
            test_html = self.test_dir + "/.test.test_export_to_html.html"
            story = self.get_story()
            story.export_to_html(test_html)
            with open(test_html, "r", encoding="utf8") as file_desc:
                test_html_content = file_desc.read()
            self.assertEqual(
                test_html_content,
                self.get_html(),
            )

    def test_to_html(self) -> None:
        """
        A method for testing Story.to_html method.

        Raises:
            AssertionError: If the story html is not correct.
        """

        with unittest.mock.patch(
            "ipyvizzustory.storylib.story.uuid.uuid4", return_value=self
        ):
            self.assertEqual(
                self.get_story().to_html(),
                self.get_html(),
            )

    def test_to_html_with_size(self) -> None:
        """
        A method for testing Story.to_html method with size.

        Raises:
            AssertionError: If the story html is not correct.
        """

        with unittest.mock.patch(
            "ipyvizzustory.storylib.story.uuid.uuid4", return_value=self
        ):
            story = self.get_story()
            story.set_size(width=None, height=None)
            self.assertEqual(
                story.to_html(),
                DISPLAY_TEMPLATE.format(
                    id="1234567",
                    vizzu_attribute="",
                    vizzu_story=VIZZU_STORY,
                    vizzu_player_data=self.get_vpd(),
                    chart_size="",
                    chart_features="",
                    chart_events="",
                ),
            )

    def test_to_html_with_size_width(self) -> None:
        """
        A method for testing Story.to_html method with size/width.

        Raises:
            AssertionError: If the story html is not correct.
        """

        with unittest.mock.patch(
            "ipyvizzustory.storylib.story.uuid.uuid4", return_value=self
        ):
            story = self.get_story()
            story.set_size(width="800px", height=None)
            self.assertEqual(
                story.to_html(),
                DISPLAY_TEMPLATE.format(
                    id="1234567",
                    vizzu_attribute="",
                    vizzu_story=VIZZU_STORY,
                    vizzu_player_data=self.get_vpd(),
                    chart_size="vizzuPlayer.style.cssText = 'width: 800px;'",
                    chart_features="",
                    chart_events="",
                ),
            )

    def test_to_html_with_size_height(self) -> None:
        """
        A method for testing Story.to_html method with size/height.

        Raises:
            AssertionError: If the story html is not correct.
        """

        with unittest.mock.patch(
            "ipyvizzustory.storylib.story.uuid.uuid4", return_value=self
        ):
            story = self.get_story()
            story.set_size(width=None, height="480px")
            self.assertEqual(
                story.to_html(),
                DISPLAY_TEMPLATE.format(
                    id="1234567",
                    vizzu_attribute="",
                    vizzu_story=VIZZU_STORY,
                    vizzu_player_data=self.get_vpd(),
                    chart_size="vizzuPlayer.style.cssText = 'height: 480px;'",
                    chart_features="",
                    chart_events="",
                ),
            )

    def test_to_html_with_size_width_and_height(self) -> None:
        """
        A method for testing Story.to_html method with size/width and height.

        Raises:
            AssertionError: If the story html is not correct.
        """

        with unittest.mock.patch(
            "ipyvizzustory.storylib.story.uuid.uuid4", return_value=self
        ):
            story = self.get_story()
            story.set_size(width="800px", height="480px")
            self.assertEqual(
                story.to_html(),
                self.get_html_with_size(),
            )

    def test_to_html_with_feature(self) -> None:
        """
        A method for testing Story.to_html method with feature.

        Raises:
            AssertionError: If the story html is not correct.
        """

        with unittest.mock.patch(
            "ipyvizzustory.storylib.story.uuid.uuid4", return_value=self
        ):
            story = self.get_story()
            story.set_feature("tooltip", True)
            story.set_feature("tooltip", True)
            self.assertEqual(
                story.to_html(),
                DISPLAY_TEMPLATE.format(
                    id="1234567",
                    vizzu_attribute="",
                    vizzu_story=VIZZU_STORY,
                    vizzu_player_data=self.get_vpd(),
                    chart_size="",
                    chart_features=(
                        "chart.feature('tooltip', true);"
                        + f"\n{DISPLAY_INDENT * 3}"
                        + "chart.feature('tooltip', true);"
                    ),
                    chart_events="",
                ),
            )

    def test_to_html_with_event(self) -> None:
        """
        A method for testing Story.to_html method with event.

        Raises:
            AssertionError: If the story html is not correct.
        """

        with unittest.mock.patch(
            "ipyvizzustory.storylib.story.uuid.uuid4", return_value=self
        ):
            story = self.get_story()
            handler = """
                let Year = parseFloat(event.data.text);
                if (!isNaN(Year) && Year > 1950 && Year < 2020 && Year % 5 !== 0) {
                    event.preventDefault();
                }
                """
            story.add_event("plot-axis-label-draw", handler)
            story.add_event("plot-axis-label-draw", handler)
            self.assertEqual(
                story.to_html(),
                DISPLAY_TEMPLATE.format(
                    id="1234567",
                    vizzu_attribute="",
                    vizzu_story=VIZZU_STORY,
                    vizzu_player_data=self.get_vpd(),
                    chart_size="",
                    chart_features="",
                    chart_events=(
                        "chart.on('plot-axis-label-draw', "
                        + f"event => {{{' '.join(handler.split())}}});"
                        + f"\n{DISPLAY_INDENT * 3}"
                        + "chart.on('plot-axis-label-draw', "
                        + f"event => {{{' '.join(handler.split())}}});"
                    ),
                ),
            )
