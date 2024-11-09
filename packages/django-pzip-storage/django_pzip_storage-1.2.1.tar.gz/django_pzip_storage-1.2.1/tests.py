import os
import tempfile
import unittest
from unittest.mock import MagicMock

import pzip
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile

from pzip_storage import PZipStorage, bad_keys, needs_encryption, needs_rotation


class CompressedStorageTests(unittest.TestCase):
    def setUp(self):
        self.storage = PZipStorage()

    def test_improper_config(self):
        with self.assertRaises(ImproperlyConfigured):
            PZipStorage(keys=[])
        # PZipStorage does not check callables at creation time.
        storage = PZipStorage(keys=lambda: [])
        with self.assertRaises(ImproperlyConfigured):
            storage.save("testfile", ContentFile(b"test data"))

    def test_round_trip(self):
        plaintext = b"Hello world!"
        name = self.storage.save("hello.txt", ContentFile(plaintext))
        with self.storage.open(name) as f:
            self.assertEqual(plaintext, f.read())
        self.assertEqual(len(plaintext), self.storage.size(name))
        self.assertTrue(self.storage.exists(name))
        self.storage.delete(name)
        self.assertFalse(self.storage.exists(name))

    def test_multiple_keys(self):
        plaintext = (
            b"Answer to the Ultimate Question of Life, The Universe, and Everything."
        )
        keys = [b"first"]
        handler = MagicMock()
        needs_rotation.connect(handler, sender=PZipStorage)
        storage = PZipStorage(keys=lambda: keys)
        name = storage.save("testfile", ContentFile(plaintext))
        keys.insert(0, b"second")
        keys.insert(0, b"third")
        with storage.open(name) as f:
            self.assertEqual(plaintext, f.read())
            handler.assert_called_once_with(
                signal=needs_rotation,
                sender=PZipStorage,
                storage=storage,
                name=name,
                key=b"first",
            )
        storage.delete(name)

    def test_no_compression(self):
        name = self.storage.save("test.jpg", ContentFile(b"JPEG data"))
        with self.storage.open(name) as f:
            self.assertIsInstance(f, pzip.PZip)
            self.assertEqual(f.compression, pzip.Compression.NONE)

    def test_unencrypted(self):
        handler = MagicMock()
        needs_encryption.connect(handler, sender=PZipStorage)
        self.assertEqual(self.storage.size("unencrypted"), 11)
        with self.storage.open("unencrypted") as f:
            self.assertNotIsInstance(f, pzip.PZip)
            self.assertEqual(f.read(), b"hello world")
            handler.assert_called_once_with(
                signal=needs_encryption,
                sender=PZipStorage,
                storage=self.storage,
                name="unencrypted",
            )

    def test_bad_keys(self):
        handler = MagicMock()
        bad_keys.connect(handler, sender=PZipStorage)
        with self.storage.open("encrypted" + PZipStorage.DEFAULT_EXTENSION) as f:
            self.assertNotEqual(f.read(), b"unrecoverable data")
            handler.assert_called_once_with(
                signal=bad_keys,
                sender=PZipStorage,
                storage=self.storage,
                name="encrypted" + PZipStorage.DEFAULT_EXTENSION,
            )


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tempdir:
        # Write a pre-existing unencrypted file to the storage root.
        with open(os.path.join(tempdir, "unencrypted"), "wb") as f:
            f.write(b"hello world")
        # Write a pre-existing encrypted file (with a random key) to the storage root.
        random_key = os.urandom(32)
        with pzip.open(
            os.path.join(tempdir, "encrypted" + PZipStorage.DEFAULT_EXTENSION),
            "wb",
            key=random_key,
        ) as f:
            f.write(b"unrecoverable data")
        # Set up Django settings to have a stable SECRET_KEY and MEDIA_ROOT.
        settings.configure(SECRET_KEY=os.urandom(32), MEDIA_ROOT=tempdir)
        unittest.main()
