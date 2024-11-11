
import os
from typing import BinaryIO



class Packer:
    """ This class provides methods to append and extract content at the end of a file. """

    # //////////////////////////////////////////////////////////////////////////
    # // class methods                                                        //
    # //////////////////////////////////////////////////////////////////////////

    @classmethod
    def extract_from_file(cls, source_file: str, destination_file: str, delimiter: bytearray = None) -> bool:
        """ Extracts a packed payload file.
            :param source_file: Source file name that contains a payload.
            :param destination_file: Target file name for the payload.
            :param delimiter: A byte sequence that is used as a delimiter that separates the carrier file from its payload.
            :return: Returns True if the file has been successfully extracted, otherwise returns False. """

        d = cls._Delimiter(delimiter)
        with open(source_file, 'rb') as re:
            while True:
                byte = re.read(1)
                if not byte: break

                if d.delimiter_complete(byte[0]):
                    with open(destination_file, 'wb') as wr:
                        cls._copy_stream(re, wr)
                    return True
        return False


    @classmethod
    def append_to_file(cls, carrier_file: str, payload_file: str, delimiter: bytearray = None) -> bool:
        """ Appends a payload to a carrier file.
            :param carrier_file: Carrier file name (file to append to).
            :param payload_file: Payload file name (file to append).
            :param delimiter: A byte sequence that is used as a delimiter that separates the carrier file from its payload.
            :raises ValueError: Raised when a file already contains the delimiter data. """

        cls._test_carrier(carrier_file, delimiter)
        d = cls._Delimiter(delimiter)

        with open(payload_file, 'rb') as re:
            with open(carrier_file, 'ab') as wr:
                wr.write(d._byte_sequence)
                cls._copy_stream(re, wr)


    @classmethod
    def _test_carrier(cls, carrier_file: str, delimiter: bytearray) -> None:
        """ Tests a carrier file for existing delimiter.
            :param carrier_file: Carrier file name.
            :param delimiter: A byte sequence that is used as a delimiter that separates the carrier file from its payload.
            :raises ValueError: Raised when a file already contains the delimiter data. """

        d = cls._Delimiter(delimiter)

        if os.path.exists(carrier_file):
            with open(carrier_file, 'rb') as re:
                ok = True

                while True:
                    byte = re.read(1)
                    if not byte:
                        break

                    if d.delimiter_complete(byte[0]):
                        ok = False
                        break

            if not ok:
                raise ValueError("File already contains delimiter.")



    @classmethod
    def _copy_stream(cls, source: BinaryIO, destination: BinaryIO) -> None:
        """ Reads a stream into a stream.
            :param source: Source stream.
            :param destination: Destination stream. """

        buf_size = 2048

        while True:
            buf = source.read(buf_size)
            if not buf: break
            destination.write(buf)



    # //////////////////////////////////////////////////////////////////////////
    # // [class] _Delimiter                                                   //
    # //////////////////////////////////////////////////////////////////////////

    class _Delimiter:
        """ This class defines a byte sequence that separates the appended content from the carrier content.
            :var _position: Current position in delimiter.
            :var _byte_sequence: Delimiter byte sequence. """

        # //////////////////////////////////////////////////////////////////////
        # // constructor                                                      //
        # //////////////////////////////////////////////////////////////////////

        def __init__(self, delimiter: bytearray) -> None:
            """ Creates a new instance of this class.
                :param delimiter: Delimiter byte sequence. """
            self._position = 0
            if delimiter is None:
                self._byte_sequence = bytearray(24)

                for i in range(4): self._byte_sequence[i] = 4
                for i in range(4, 7): self._byte_sequence[i] = 7
                for i in range(7, 13): self._byte_sequence[i] = 4
                self._byte_sequence[13] = 2
                self._byte_sequence[14] = 4
                for i in range(15, 17): self._byte_sequence[i] = 8
                for i in range(17, 23): self._byte_sequence[i] = 4
                self._byte_sequence[22] = 24
                self._byte_sequence[23] = 4
            else:
                self._byte_sequence = delimiter



        # //////////////////////////////////////////////////////////////////////
        # // methods                                                          //
        # //////////////////////////////////////////////////////////////////////

        def delimiter_complete(self, b: int) -> bool:
            """ Advances reading and returns TRUE if the delimiter is completely read.
                :param b: Currently read byte.
                :return: Returns True if the prelude is complete, otherwise returns False. """

            if self._byte_sequence[self._position] == b:
                self._position += 1
            else: self._position = 0

            return self._position == len(self._byte_sequence)
        