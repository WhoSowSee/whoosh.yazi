from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import gen_star_history as charts


class StarHistoryTests(unittest.TestCase):
    def test_weekly_api_pages_are_all_collected(self):
        first = [{"week": index, "days": [0] * 7} for index in range(30)]
        second = [{"week": 31, "days": [1, 0, 0, 0, 0, 0, 0]}]
        with patch.object(charts, "request_json", side_effect=[first, second]) as request:
            self.assertEqual(charts.fetch_history("owner/repo"), first + second)
        self.assertEqual(request.call_count, 2)
        self.assertTrue(request.call_args_list[1].args[0].endswith("page=2"))

    def test_reversed_weeks_become_chronological_cumulative_stars(self):
        weeks = [
            {"week": 7 * 86400, "days": [3, 0, 0, 0, 0, 0, 0]},
            {"week": 0, "days": [1, 2, 0, 0, 0, 0, 0]},
        ]
        series = charts.cumulative_series(weeks)
        self.assertEqual([count for _, count in series], [1, 3, 6])
        self.assertEqual(series, sorted(series))

    def test_sampling_preserves_history_endpoints(self):
        start = datetime(2025, 1, 1, tzinfo=timezone.utc)
        series = [(start + timedelta(days=index), index + 1) for index in range(500)]
        sampled = charts.sample_series(series)
        self.assertEqual(len(sampled), 160)
        self.assertEqual(sampled[0], series[0])
        self.assertEqual(sampled[-1], series[-1])

    def test_empty_and_single_day_charts_are_valid_and_deterministic(self):
        start = datetime(2025, 1, 1, tzinfo=timezone.utc)
        for theme in charts.COLORS:
            for series in [[], [(start, 3)]]:
                with self.subTest(theme=theme, stars=series):
                    svg = charts.render_svg("owner/repo & chart", series, start, theme)
                    root = ET.fromstring(svg)
                    self.assertEqual(root.attrib["viewBox"], "0 0 820 420")
                    title = root.find("{http://www.w3.org/2000/svg}title")
                    self.assertIn("owner/repo & chart", title.text)
                    self.assertEqual(
                        svg, charts.render_svg("owner/repo & chart", series, start, theme)
                    )
                    self.assertNotIn("nan", svg)
                    self.assertNotIn("inf", svg)

    def test_russian_labels_preserve_chart_geometry(self):
        start = datetime(2025, 1, 1, tzinfo=timezone.utc)
        series = [(start, 1), (start + timedelta(days=2), 3)]
        namespace = "{http://www.w3.org/2000/svg}"
        for theme in charts.COLORS:
            with self.subTest(theme=theme):
                english = ET.fromstring(
                    charts.render_svg("owner/repo & chart", series, start, theme)
                )
                russian = ET.fromstring(
                    charts.render_svg("owner/repo & chart", series, start, theme, "ru")
                )
                self.assertEqual(english.find(namespace + "text").text, "Star History")
                self.assertEqual(russian.find(namespace + "text").text, "История звёзд")
                self.assertIn("owner/repo & chart", russian.find(namespace + "title").text)
                labels = [node.text for node in russian.findall(namespace + "text")]
                self.assertTrue(any("Звёзд: 3" in text for text in labels))
                self.assertTrue(any("янв" in text for text in labels))
                for element in ("line", "polygon", "polyline", "circle"):
                    self.assertEqual(
                        [node.attrib for node in english.findall(namespace + element)],
                        [node.attrib for node in russian.findall(namespace + element)],
                    )

    def test_command_generates_both_languages_and_color_schemes(self):
        filenames = {
            "star-history-light.svg",
            "star-history-dark.svg",
            "star-history-light-ru.svg",
            "star-history-dark-ru.svg",
        }
        with tempfile.TemporaryDirectory() as directory:
            with (
                patch("sys.argv", ["charts", "--repo", "owner/repo", "--output-dir", directory]),
                patch.object(charts, "request_json", return_value={"created_at": "2025-01-01T00:00:00Z"}),
                patch.object(charts, "fetch_history", return_value=[]),
                patch("builtins.print"),
            ):
                charts.main()
            paths = list(Path(directory).iterdir())
            self.assertEqual({path.name for path in paths}, filenames)
            for path in paths:
                root = ET.fromstring(path.read_text(encoding="utf-8"))
                heading = root.find("{http://www.w3.org/2000/svg}text").text
                self.assertEqual(
                    heading, "История звёзд" if path.name.endswith("-ru.svg") else "Star History"
                )


if __name__ == "__main__":
    unittest.main()
