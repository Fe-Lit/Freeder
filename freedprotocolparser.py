# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class freedprotocolparser(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(1)
        if not self.magic == b"\xD1":
            raise kaitaistruct.ValidationNotEqualError(b"\xD1", self.magic, self._io, u"/seq/0")
        self.cam_id = self._io.read_u1()
        self.pan_angle = freedprotocolparser.S3be(self._io, self, self._root)
        self.tilt_angle = freedprotocolparser.S3be(self._io, self, self._root)
        self.roll_angle = freedprotocolparser.S3be(self._io, self, self._root)
        self.x_pos = freedprotocolparser.S3be(self._io, self, self._root)
        self.y_pos = freedprotocolparser.S3be(self._io, self, self._root)
        self.z_pos = freedprotocolparser.S3be(self._io, self, self._root)
        self.zoom = freedprotocolparser.S3be(self._io, self, self._root)
        self.focus = freedprotocolparser.S3be(self._io, self, self._root)
        self.custom_value = self._io.read_u2be()
        self.checksum = self._io.read_u1()

    class S3be(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sign = self._io.read_bits_int_be(1) != 0
            self.ext_mod = self._io.read_bits_int_be(23)

        @property
        def value(self):
            if hasattr(self, '_m_value'):
                return self._m_value if hasattr(self, '_m_value') else None

            self._m_value = ((self.ext_mod - (1 << 23)) if self.sign else self.ext_mod)
            return self._m_value if hasattr(self, '_m_value') else None



