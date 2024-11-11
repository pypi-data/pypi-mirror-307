import unittest
from .utils import asn1toolBaseTest
import asn1tool


class asn1toolTwoModulesTest(asn1toolBaseTest):

    maxDiff = None

    def test_uper(self):
        files = [
            'tests/files/module-1.asn',
            'tests/files/module-2.asn'
        ]

        spec = asn1tool.compile_files(files, 'uper')

        # Message 1.
        decoded = {
            'priority': 'high',
            'src': 1,
            'dst': 2,
            'num': 0,
            'length': 256
        }

        encoded = b'\x14\x04\x00'

        self.assert_encode_decode(spec, 'ASequence', decoded, encoded)

        # Message 2.
        decoded = {
            'isvalide': True,
            'name': 'toto',
            'identity': 5
        }

        encoded = b'\x82\x74\xdf\xd3\x7d'

        self.assert_encode_decode(spec, 'SeqMod2', decoded, encoded)


if __name__ == '__main__':
    unittest.main()
