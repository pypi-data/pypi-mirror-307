# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

""" Provides version access utilities. """

from . import _BS_C, ffi
from .ffi_utils import bytes_to_string
from .result import Result


def get_version_string(packed_version=None, buffer_length=256):
    """ 
    Gets the version string from a packed version.

    :param packed_version: If version is provided, it is unpacked and presented as the version string. Most useful for printing the firmware version currently installed on a module.
    :type packed_version: unsigned int

    :param buffer_length: The amount of C memory to allocate
    :type buffer_length: unsigned short

    :return: The library version as a string
    :rtype: str
    """

    result = ffi.new("struct Result*")
    
    if not packed_version:
        ffi_buffer = ffi.new("unsigned char[]", buffer_length)
        _BS_C.version_GetString(result, ffi_buffer, buffer_length)
        pResult = bytes_to_string(Result(result.error, [ffi_buffer[i] for i in range(result.value)]))
        if pResult.error:
            raise MemoryError("version_GetString: ".format(pResult.error))
        return 'Brainstem library version: ' + pResult.value

    else:
        return 'Brainstem version: %d.%d.%d' % unpack_version(packed_version)


def unpack_version(packed_version):
    """ 
    Unpacks a packed version. 

    :param packed_version: The packed version number.
    :type packed_version: unsigned int

    :return: Returns the library version as a 3-tuple (major, minor, patch)
    :rtype: str
    """
    result_major = ffi.new("struct Result*")
    result_minor = ffi.new("struct Result*")
    result_patch = ffi.new("struct Result*")

    _BS_C.version_ParseMajor(result_major, packed_version)
    _BS_C.version_ParseMinor(result_minor, packed_version)
    _BS_C.version_ParsePatch(result_patch, packed_version)

    #Shouldn't be able to hit this. These functions don't return errors. 
    if result_major.error or result_minor.error or result_patch.error:
        raise RuntimeError("Error getting version: major: %d, minor: %d, patch: %d" % (result_major.error, result_minor.error, result_patch.error))

    return result_major.value, result_minor.value, result_patch.value
