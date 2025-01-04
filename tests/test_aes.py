import unittest
import sqlite3

from src.encryption.aes import decrypt_message

# These tests dont work as the encryption keys are randomly generated
class TestAES(unittest.TestCase):

    def test_decrypt_message(self):

        ## Check if the decryption works
        enc_id = "4ULdDFoRq7lJ82K3F2GOb+0cLmPfO32N0rpnK6A01Cw="
        enc_key = b"s\xcfS)\x80\x9e\x8d\x1e\xca\xf4b#\xa7\x10[\xcb\x01\x94\xf5\xc6Q\xb5\xbf\x16\x12\xf1`\xfc\x19\xa8\x99\x1a"
        decrypted_message = decrypt_message(enc_id, enc_key)
        self.assertEqual(decrypted_message, "MT_00001")

        ## Check if the key stored in database is correct
        conn = sqlite3.connect(r"data/database.sqlite")
        cursor = conn.cursor()

        db_encrypted_message = cursor.execute(
            "SELECT * FROM keys WHERE encrypted_id = ?", (enc_id,)
        ).fetchone()
        self.assertEqual(db_encrypted_message[1], enc_key)



    


