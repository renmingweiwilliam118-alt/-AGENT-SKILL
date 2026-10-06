"""The memo sits between a caller and a call it would otherwise make.

So it has exactly two ways to do harm: raise into a caller that was doing fine without it,
or hand back something nobody stored. Every test here is one of those, plus the limits that
keep a cache directory from becoming a liability. Each test gets its own empty cache home,
so nothing here reads or writes the real one.
"""
from __future__ import annotations

import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from jevkit import memo

WEEK = 7 * 24 * 3600


class MemoCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        env = mock.patch.dict(os.environ, {"XDG_CACHE_HOME": self._tmp.name})
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("JEV_MEMO", None)
        self.home = Path(self._tmp.name)
        self.file = self.home / "jev" / "memo" / "plan.json"
        self.k = memo.key("plan", "open safari")

    def write(self, payload) -> None:
        self.file.parent.mkdir(parents=True, exist_ok=True)
        self.file.write_bytes(payload if isinstance(payload, bytes) else json.dumps(payload).encode())


class RoundTripTests(MemoCase):
    def test_a_value_put_is_the_value_got(self):
        value = {"steps": [{"kind": "open_app", "target": "Safari"}]}
        memo.put("plan", self.k, value)
        self.assertEqual(memo.get("plan", self.k, WEEK), value)

    def test_another_key_and_another_namespace_are_misses(self):
        memo.put("plan", self.k, {"n": 1})
        self.assertIsNone(memo.get("plan", memo.key("plan", "open notes"), WEEK))
        self.assertIsNone(memo.get("other", self.k, WEEK))

    def test_the_file_is_the_documented_shape(self):
        """Someone will read this file by hand to see what is in it. It says what it is."""
        memo.put("plan", self.k, {"n": 1})
        data = json.loads(self.file.read_text())
        self.assertEqual(sorted(data), ["entries", "schema"])
        self.assertEqual(data["schema"], "jev.memo_v1")
        self.assertEqual(data["entries"][self.k]["v"], {"n": 1})
        self.assertIsInstance(data["entries"][self.k]["at"], float)

    def test_an_entry_older_than_the_ttl_is_a_miss(self):
        with mock.patch.object(memo.time, "time", return_value=1_000_000.0):
            memo.put("plan", self.k, {"n": 1})
        with mock.patch.object(memo.time, "time", return_value=1_000_000.0 + WEEK - 1):
            self.assertEqual(memo.get("plan", self.k, WEEK), {"n": 1})
        with mock.patch.object(memo.time, "time", return_value=1_000_000.0 + WEEK + 1):
            self.assertIsNone(memo.get("plan", self.k, WEEK))

    def test_put_with_a_ttl_takes_expired_entries_out_of_the_file(self):
        """get() refusing to serve an old entry is not the same as the entry being gone. It
        sat on disk until 256 newer ones evicted it. Without a ttl nothing is purged."""
        old, older = memo.key("plan", "old"), memo.key("plan", "older")
        with mock.patch.object(memo.time, "time", return_value=1_000_000.0):
            memo.put("plan", old, {"n": "old"})
            memo.put("plan", older, {"n": "older"})
        with mock.patch.object(memo.time, "time", return_value=1_000_000.0 + WEEK + 1):
            memo.put("plan", self.k, {"n": 1})
            self.assertEqual(len(json.loads(self.file.read_text())["entries"]), 3)
            memo.put("plan", self.k, {"n": 2}, ttl_s=WEEK)
        self.assertEqual(list(json.loads(self.file.read_text())["entries"]), [self.k])
        self.assertNotIn("older", self.file.read_text())

    def test_an_entry_dated_in_the_future_is_a_miss(self):
        """Otherwise a hand-written "at" far ahead is an entry that outlives every TTL."""
        for at in (4_000_000_000_000, float("inf"), float("nan"), "soon", True, None):
            with self.subTest(at=at):
                self.write(json.dumps({"schema": memo.SCHEMA, "entries": {self.k: {"at": 0, "v": {"n": 1}}}})
                           .replace('"at": 0', f'"at": {json.dumps(at)}').encode())
                self.assertIsNone(memo.get("plan", self.k, WEEK))

    def test_drop_removes_one_entry_and_leaves_the_rest(self):
        other = memo.key("plan", "open notes")
        memo.put("plan", self.k, {"n": 1})
        memo.put("plan", other, {"n": 2})
        memo.drop("plan", self.k)
        self.assertIsNone(memo.get("plan", self.k, WEEK))
        self.assertEqual(memo.get("plan", other, WEEK), {"n": 2})
        memo.drop("plan", self.k)               # already gone: nothing to do, nothing raised
        memo.drop("never-written", self.k)


class KeyTests(MemoCase):
    def test_the_key_is_the_documented_hash(self):
        import hashlib
        expected = hashlib.sha256("\x00".join(["jev.memo_v1", "plan", "open safari", "finder"]).encode()).hexdigest()
        self.assertEqual(memo.key("plan", "open safari", "finder"), expected)

    def test_parts_cannot_be_shifted_across_the_separator(self):
        """("ab", "c") and ("a", "bc") must differ, and a NUL inside a part must not let
        ("a\\0b", "c") pass for ("a", "b\\0c")."""
        self.assertNotEqual(memo.key("plan", "ab", "c"), memo.key("plan", "a", "bc"))
        self.assertNotEqual(memo.key("plan", "a\x00b", "c"), memo.key("plan", "a", "b\x00c"))

    def test_a_part_that_cannot_be_encoded_still_gives_a_key(self):
        self.assertRegex(memo.key("plan", "lone surrogate \udc80", 7, None), r"^[0-9a-f]{64}$")


class ModeTests(MemoCase):
    def test_shadow_is_the_default_and_a_typo_does_not_turn_reuse_on(self):
        for value, expected in ((None, "shadow"), ("", "shadow"), ("shadow", "shadow"), ("on", "on"),
                                (" ON ", "on"), ("off", "off"), ("true", "shadow"), ("1", "shadow"),
                                ("onn", "shadow")):
            with self.subTest(value=value):
                with mock.patch.dict(os.environ, {} if value is None else {"JEV_MEMO": value}):
                    self.assertEqual(memo.mode(), expected)


class NeverRaisesTests(MemoCase):
    """A cache that can crash its caller is worse than no cache."""

    def test_a_missing_file_is_a_miss(self):
        self.assertIsNone(memo.get("plan", self.k, WEEK))

    def test_a_corrupt_file_is_a_miss_and_the_next_put_repairs_it(self):
        for junk in (b"", b"{not json", b"\xff\xfe\x00binary", b"[]", b'"a string"', b"null",
                     b"[" * 200_000,                         # nests deeper than the parser's recursion limit
                     json.dumps({"schema": memo.SCHEMA, "entries": []}).encode(),
                     json.dumps({"schema": memo.SCHEMA, "entries": {self.k: "not an entry"}}).encode(),
                     json.dumps({"schema": memo.SCHEMA, "entries": {self.k: {"at": 1, "v": ["not", "a", "dict"]}}}).encode()):
            with self.subTest(junk=junk[:24]):
                self.write(junk)
                self.assertIsNone(memo.get("plan", self.k, WEEK))
                memo.put("plan", self.k, {"n": 1})
                self.assertEqual(memo.get("plan", self.k, WEEK), {"n": 1})

    def test_a_file_from_another_schema_is_a_miss(self):
        """A newer version may store something this one would misread. It is not ours to guess at."""
        with mock.patch.object(memo.time, "time", return_value=1_000_000.0):
            self.write({"schema": "jev.memo_v2", "entries": {self.k: {"at": 1_000_000.0, "v": {"n": 1}}}})
            self.assertIsNone(memo.get("plan", self.k, WEEK))

    def test_a_file_over_two_megabytes_is_not_parsed(self):
        """We never write one, so we did not write this one."""
        entry = {self.k: {"at": 1_000_000.0, "v": {"n": 1}}}
        padded = json.dumps({"schema": memo.SCHEMA, "entries": entry, "padding": "x" * memo.MAX_FILE_BYTES})
        with mock.patch.object(memo.time, "time", return_value=1_000_000.0):
            self.write(padded.encode())
            with mock.patch.object(memo.json, "loads", side_effect=AssertionError("parsed an oversized file")):
                self.assertIsNone(memo.get("plan", self.k, WEEK))
            self.write({"schema": memo.SCHEMA, "entries": entry})        # control: the same entry, unpadded
            self.assertEqual(memo.get("plan", self.k, WEEK), {"n": 1})

    def test_a_cache_home_that_cannot_be_written_costs_the_memo_not_the_caller(self):
        blocker = self.home / "not-a-directory"
        blocker.write_text("a file where the cache home should be")
        with mock.patch.dict(os.environ, {"XDG_CACHE_HOME": str(blocker)}):
            memo.put("plan", self.k, {"n": 1})
            self.assertIsNone(memo.get("plan", self.k, WEEK))
            memo.drop("plan", self.k)
            self.assertEqual(memo.clear(), 0)
            self.assertEqual(memo.stats()["namespaces"], {})

    def test_a_value_that_is_not_json_is_not_stored_and_not_raised(self):
        memo.put("plan", self.k, {"when": object()})
        memo.put("plan", self.k, ["a", "list"])
        self.assertIsNone(memo.get("plan", self.k, WEEK))

    def test_a_failed_write_leaves_no_temp_file_and_the_old_entry_intact(self):
        memo.put("plan", self.k, {"n": 1})
        with mock.patch.object(memo.os, "replace", side_effect=OSError("disk full")):
            memo.put("plan", self.k, {"n": 2})
        self.assertEqual(memo.get("plan", self.k, WEEK), {"n": 1})
        self.assertEqual([p.name for p in self.file.parent.iterdir()], ["plan.json"])


class LimitTests(MemoCase):
    def test_a_value_over_16_kb_is_refused(self):
        memo.put("plan", self.k, {"text": "x" * (16 * 1024)})
        self.assertIsNone(memo.get("plan", self.k, WEEK))
        self.assertFalse(self.file.exists())
        memo.put("plan", self.k, {"text": "x" * (15 * 1024)})          # control: under the limit is kept
        self.assertIsNotNone(memo.get("plan", self.k, WEEK))

    def test_the_257th_entry_evicts_the_oldest(self):
        keys = [memo.key("plan", f"command {n}") for n in range(memo.MAX_ENTRIES + 1)]
        seeded = {k: {"at": 1_000_000.0 + n, "v": {"n": n}} for n, k in enumerate(keys[:-1])}
        self.write({"schema": memo.SCHEMA, "entries": seeded})
        with mock.patch.object(memo.time, "time", return_value=1_000_500.0):
            memo.put("plan", keys[-1], {"n": "newest"})
            self.assertIsNone(memo.get("plan", keys[0], WEEK))                  # the oldest went
            self.assertEqual(memo.get("plan", keys[1], WEEK), {"n": 1})         # the next oldest stayed
            self.assertEqual(memo.get("plan", keys[-1], WEEK), {"n": "newest"})
        self.assertEqual(len(json.loads(self.file.read_text())["entries"]), memo.MAX_ENTRIES)

    def test_what_is_written_can_always_be_read_back(self):
        """256 values of 16 KB are twice the size the reader accepts. A writer that did not
        trim to fit would produce a file that reads as empty, and rewrite it every call."""
        with mock.patch.object(memo, "MAX_FILE_BYTES", 40_000):
            for n in range(12):
                with mock.patch.object(memo.time, "time", return_value=1_000_000.0 + n):
                    memo.put("plan", memo.key("plan", f"command {n}"), {"text": "x" * 8_000})
            self.assertLessEqual(self.file.stat().st_size, 40_000)
            with mock.patch.object(memo.time, "time", return_value=1_000_020.0):
                self.assertIsNotNone(memo.get("plan", memo.key("plan", "command 11"), WEEK))
                self.assertIsNone(memo.get("plan", memo.key("plan", "command 0"), WEEK))


class PrivacyTests(MemoCase):
    @unittest.skipIf(os.name == "nt", "POSIX permission bits")
    def test_the_directory_is_0700_and_the_file_0600_whatever_the_umask(self):
        """The entries are a record of what someone asked their computer to do."""
        old = os.umask(0o000)
        try:
            memo.put("plan", self.k, {"n": 1})
        finally:
            os.umask(old)
        self.assertEqual(stat.S_IMODE(self.file.parent.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(self.file.stat().st_mode), 0o600)

    @unittest.skipIf(os.name == "nt", "POSIX permission bits")
    def test_a_directory_that_already_existed_wide_open_is_closed(self):
        self.file.parent.mkdir(parents=True)
        os.chmod(self.file.parent, 0o755)
        memo.put("plan", self.k, {"n": 1})
        self.assertEqual(stat.S_IMODE(self.file.parent.stat().st_mode), 0o700)

    def test_a_namespace_that_is_a_path_is_refused(self):
        for hostile in ("../x", "..", "a/b", "/etc/x", "plan.json", "", "x" * 33, "PLAN", "pl an", "plan\n", None, 7):
            with self.subTest(namespace=hostile):
                memo.put(hostile, self.k, {"n": 1})
                self.assertIsNone(memo.get(hostile, self.k, WEEK))
                memo.drop(hostile, self.k)
        written = [p for p in self.home.rglob("*") if p.is_file()]
        self.assertEqual(written, [], "a refused namespace still wrote a file")

    def test_a_key_that_is_not_a_hash_is_refused(self):
        for hostile in ("", "open safari", "../x", "g" * 64, None):
            with self.subTest(key=hostile):
                memo.put("plan", hostile, {"n": 1})
                self.assertIsNone(memo.get("plan", hostile, WEEK))
        self.assertFalse(self.file.exists())


class HousekeepingTests(MemoCase):
    def test_stats_counts_entries_per_namespace_and_shows_no_key_and_no_value(self):
        memo.put("plan", self.k, {"text": "the launch is on the ninth"})
        memo.put("plan", memo.key("plan", "open notes"), {"n": 2})
        memo.put("other", self.k, {"n": 3})
        report = memo.stats()
        self.assertEqual({name: row["entries"] for name, row in report["namespaces"].items()},
                         {"plan": 2, "other": 1})
        self.assertEqual(report["namespaces"]["plan"]["bytes"], self.file.stat().st_size)
        self.assertEqual((report["schema"], report["mode"]), ("jev.memo_v1", "shadow"))
        printed = json.dumps(report)
        self.assertNotIn(self.k, printed)
        self.assertNotIn("ninth", printed)

    def test_clear_removes_everything_and_says_how_much(self):
        memo.put("plan", self.k, {"n": 1})
        memo.put("plan", memo.key("plan", "open notes"), {"n": 2})
        memo.put("other", self.k, {"n": 3})
        stray = self.file.parent / "plan.json.tmp.4242"          # a process killed between write and replace
        stray.write_text("{}")
        self.assertEqual(memo.clear(), 3)
        self.assertEqual(list(self.file.parent.iterdir()), [])
        self.assertEqual(memo.clear(), 0)
        self.assertEqual(memo.stats()["namespaces"], {})

    def test_clear_leaves_alone_a_file_it_could_not_have_written(self):
        memo.put("plan", self.k, {"n": 1})
        bystander = self.file.parent / "Notes To Self.json"
        bystander.write_text("{}")
        memo.clear()
        self.assertTrue(bystander.exists())


class PurgeTests(MemoCase):
    """An entry that is not SERVED is not an entry that is GONE, and these hold dictation."""

    def test_purge_removes_what_is_past_the_ttl_and_leaves_what_is_not(self):
        stale, fresh = memo.key("plan", "stale"), memo.key("plan", "fresh")
        with mock.patch.object(memo.time, "time", return_value=1_000_000.0):
            memo.put("plan", stale, {"text": "the note nobody has said since last week"})
        with mock.patch.object(memo.time, "time", return_value=1_000_000.0 + WEEK + 10):
            memo.put("plan", fresh, {"text": "today"})
            self.assertIn("last week", self.file.read_text())      # a put without a ttl does not reach it
            self.assertEqual(memo.purge("plan", WEEK), 1)
            self.assertNotIn("last week", self.file.read_text())
            self.assertEqual(memo.get("plan", fresh, WEEK), {"text": "today"})

    def test_purge_does_not_rewrite_a_file_with_nothing_expired(self):
        """It runs before every cache read. A write per read would cost the fast path, and
        would be one more chance to drop another process's entry, for nothing."""
        memo.put("plan", self.k, {"n": 1})
        with mock.patch.object(memo, "_save", side_effect=AssertionError("rewrote an unexpired file")):
            self.assertEqual(memo.purge("plan", WEEK), 0)

    def test_purge_leaves_alone_everything_it_cannot_read(self):
        """A newer version's file is not ours to empty, and a corrupt one is repaired by the
        next put, not by housekeeping that cannot tell what is in it."""
        self.assertEqual(memo.purge("plan", WEEK), 0)              # nothing written yet
        self.assertEqual(memo.purge("../x", WEEK), 0)
        for junk in (b"{not json", b"", json.dumps({"schema": "jev.memo_v2", "entries": {}}).encode()):
            with self.subTest(junk=junk[:12]):
                self.write(junk)
                self.assertEqual(memo.purge("plan", WEEK), 0)
                self.assertEqual(self.file.read_bytes(), junk)


class ConcurrentWriterTests(MemoCase):
    """Two processes writing one namespace at once. The file says the last writer wins."""

    def test_the_writer_that_finishes_second_wins_and_the_other_entry_is_simply_gone(self):
        """Not a corrupt file, not a merged one, not a torn value: one entry fewer, which
        costs its caller the one call it would have made without a memo at all."""
        mine, theirs = memo.key("plan", "mine"), memo.key("plan", "theirs")
        memo.put("plan", mine, {"n": "before"})
        first, second = memo._load(self.file), memo._load(self.file)     # both read the same file
        first[theirs] = {"at": memo.time.time(), "v": {"n": "theirs"}}
        second[mine] = {"at": memo.time.time(), "v": {"n": "mine"}}
        memo._save(self.file, first)
        memo._save(self.file, second)
        self.assertIsNone(memo.get("plan", theirs, WEEK))                # the loss, exactly as documented
        self.assertEqual(memo.get("plan", mine, WEEK), {"n": "mine"})
        self.assertEqual(sorted(json.loads(self.file.read_text())), ["entries", "schema"])

    def test_four_processes_writing_at_once_never_leave_anything_incoherent(self):
        """os.replace is atomic, so a reader sees one whole file or the other one. What must
        never appear is a half-written file, a torn value, or a temp file left behind."""
        import subprocess
        import sys
        import textwrap
        root = Path(memo.__file__).resolve().parents[1]
        writer = self.home / "writer.py"
        writer.write_text(textwrap.dedent("""
            import sys
            from jevkit import memo
            tag = sys.argv[1]
            for n in range(30):
                memo.put("plan", memo.key("plan", tag, n),
                         {"steps": [{"kind": "open_app", "target": tag}], "n": n})
        """))
        env = dict(os.environ, XDG_CACHE_HOME=str(self.home), PYTHONPATH=str(root))
        running = [subprocess.Popen([sys.executable, str(writer), "writer-%d" % n], cwd=str(root), env=env)
                   for n in range(4)]
        for process in running:
            self.assertEqual(process.wait(timeout=120), 0)
        entries = json.loads(self.file.read_text())["entries"]
        self.assertTrue(entries, "every writer's work was lost")
        self.assertLessEqual(len(entries), memo.MAX_ENTRIES)
        for name, entry in entries.items():
            self.assertRegex(name, r"^[0-9a-f]{64}$")
            self.assertIsInstance(entry["at"], float)
            self.assertEqual(sorted(entry["v"]), ["n", "steps"])
            self.assertTrue(entry["v"]["steps"][0]["target"].startswith("writer-"))
            self.assertIsInstance(entry["v"]["n"], int)
        self.assertEqual(list(self.file.parent.glob("*.tmp.*")), [])


class MemoCliTests(unittest.TestCase):
    def test_jev_memo_reports_counts_and_never_a_key_or_a_value(self):
        import contextlib, io, os, tempfile
        from unittest import mock
        from jevkit import cli, memo
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"XDG_CACHE_HOME": tmp, "JEV_MEMO": "on"}):
            k = memo.key("plan", "open the secret project")
            memo.put("plan", k, {"steps": [{"kind": "open_app", "target": "Notes"}]})
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                self.assertEqual(cli.main(["memo", "stats"]), 0)
            shown = buffer.getvalue()
            self.assertEqual(json.loads(shown)["namespaces"]["plan"]["entries"], 1)
            self.assertNotIn(k, shown)
            self.assertNotIn("Notes", shown)
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                self.assertEqual(cli.main(["memo", "clear"]), 0)
            self.assertEqual(json.loads(buffer.getvalue())["cleared"], 1)
            self.assertIsNone(memo.get("plan", k, 3600))


if __name__ == "__main__":
    unittest.main()


class HostileStateTests(MemoCase):
    @unittest.skipUnless(hasattr(os, "mkfifo"), "no named pipes here")
    def test_a_named_pipe_where_the_file_should_be_is_a_miss_and_not_a_hang(self):
        """open() on a pipe nobody writes to never returns, so one `mkfifo` in the cache
        directory stopped every plan() for good: the failure that is never a miss."""
        import threading
        self.file.parent.mkdir(parents=True)
        os.mkfifo(str(self.file))
        seen = []
        reader = threading.Thread(target=lambda: seen.append(memo.get("plan", self.k, WEEK)), daemon=True)
        reader.start()
        reader.join(5)
        self.assertFalse(reader.is_alive(), "get() is still waiting on the pipe")
        self.assertEqual(seen, [None])
        memo.put("plan", self.k, {"n": 1})                       # and a write replaces it with a real file
        self.assertEqual(memo.get("plan", self.k, WEEK), {"n": 1})

    def test_two_threads_do_not_write_through_the_same_temp_file(self):
        """The temp name held only the pid, so two threads truncated each other's bytes:
        eight threads putting thirty entries each left five."""
        import threading
        names = []
        real_open = os.open

        def spy(path, flags, *mode):
            if ".tmp." in str(path):
                names.append(str(path))
            return real_open(path, flags, *mode)

        with mock.patch.object(memo.os, "open", spy):
            memo.put("plan", self.k, {"n": 1})
            other = threading.Thread(target=memo.put, args=("plan", memo.key("plan", "open notes"), {"n": 2}))
            other.start()
            other.join()
        self.assertEqual(len(set(names)), 2)
        self.assertEqual(list(self.file.parent.glob("*.tmp.*")), [])
        self.assertEqual(memo.get("plan", self.k, WEEK), {"n": 1})
