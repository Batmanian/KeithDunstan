"""Offline regression tests: python3 -m unittest discover -s trove -p 'test_download_images.py'."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("download_images", Path(__file__).with_name("download_images.py"))
d = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(d)


class DownloadHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.stubs = self.root / "trove/output/bulletin/stubs"
        self.dest = self.root / "src/trove-scans/bulletin"
        self.control = self.root / "trove/output/image-download"
        for key, value in dict(ROOT=self.root, STUBS=self.stubs, DEST=self.dest, CONTROL=self.control,
                               stopping=False).items():
            patcher = patch.object(d, key, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.stub = self.stubs / "1967/1967-12-31-sample.md"
        self.stub.parent.mkdir(parents=True)
        self.stub.write_text('---\ndate: 1967-12-31\n---\nhttps://nla.gov.au/nla.obj-1')
        (self.root / "trove/image-download-config.json").write_text('{"before":"1968-01-01"}')
        self.control.mkdir(parents=True)
        self.folder = self.dest / "1967/1967-12-31-sample"
        self.key = str(self.stub.relative_to(self.root))
        self.clock = 1000.0
        self.image_requests = []

    def request(self, url, limit):
        if url.endswith("robots.txt"):
            return b"User-agent: *\nDisallow:\n"
        if "/image?" in url:
            self.image_requests.append(self.clock)
            return b"\xff\xd8\xfftest\xff\xd9"
        pages = [{"pid": "nla.obj-" + str(n), "copies": [{"copyrole": "access",
                  "technicalmetadata": {"width": 100, "height": 100}}]} for n in (2, 3)]
        work = {"children": {"article": [{"pid": "nla.obj-1", "title": "Sample",
                 "existson": [{"page": p["pid"]} for p in pages]}], "page": pages}}
        return ("var work = JSON.parse(JSON.stringify(" + json.dumps(work) + "))").encode()

    def pause(self, seconds):
        self.clock += seconds

    def run_worker(self, pause=None):
        with patch.object(d, "request", self.request), patch.object(d, "pause", pause or self.pause), \
             patch.object(d.time, "time", lambda: self.clock), patch.object(d, "log"):
            d.main()

    def history(self):
        return json.loads((self.root / "trove/download-history.json").read_text())["stubs"][self.key]

    def test_migrate_log_when_entire_folder_was_deleted(self):
        target = self.folder / "page-01-nla.obj-2.jpg"
        (self.control / "download.log").write_text(
            f"2026-09-05T00:00:00+00:00 Saved {target.relative_to(self.root)} (9 bytes)\n")
        self.run_worker()
        self.assertEqual(self.history()["status"], "skipped_deleted")
        self.assertEqual(len(self.history()["images"]), 1)
        self.assertFalse(self.folder.exists())
        self.assertEqual(self.image_requests, [])

    def test_completed_folder_deleted_between_runs_is_never_recreated(self):
        self.run_worker()
        self.assertGreaterEqual(self.image_requests[1] - self.image_requests[0], 60)
        shutil.rmtree(self.folder)
        self.run_worker()
        self.assertEqual(len(self.image_requests), 2)
        self.assertEqual(self.history()["status"], "skipped_deleted")
        self.assertFalse(self.folder.exists())

    def test_one_deleted_image_does_not_redownload(self):
        self.run_worker()
        (self.folder / "page-01-nla.obj-2.jpg").unlink()
        self.run_worker()
        self.assertEqual(len(self.image_requests), 2)
        self.assertFalse((self.folder / "page-01-nla.obj-2.jpg").exists())
        self.assertEqual(self.history()["status"], "skipped_deleted")

    def test_folder_deleted_during_minute_wait_stops_remaining_pages(self):
        def pause(seconds):
            self.pause(seconds)
            if seconds >= 60:
                shutil.rmtree(self.folder)
        self.run_worker(pause)
        self.assertEqual(len(self.image_requests), 1)
        self.assertFalse(self.folder.exists())
        self.assertEqual(self.history()["status"], "skipped_deleted")

    def test_interrupted_partial_article_resumes_only_unfetched_pages(self):
        def pause(seconds):
            if seconds >= 60:
                raise InterruptedError("Test interruption")
            self.pause(seconds)
        self.run_worker(pause)
        self.assertEqual(len(self.image_requests), 1)
        self.run_worker()
        self.assertEqual(len(self.image_requests), 2)
        self.assertGreaterEqual(self.image_requests[1] - self.image_requests[0], 60)
        self.assertEqual(self.history()["status"], "complete")

    def test_cutoff_excludes_first_day_of_1968(self):
        (self.stub.parent / "1968-01-01-later.md").write_text('---\ndate: 1968-01-01\n---\n')
        selected, total = d.select_stubs("1968-01-01")
        self.assertEqual(selected, [self.stub])
        self.assertEqual(total, 2)


if __name__ == "__main__":
    unittest.main()
