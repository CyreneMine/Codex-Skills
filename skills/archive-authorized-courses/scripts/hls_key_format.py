"""Normalize already-authorized HLS key responses; no authorization generation.

Protocol field layouts observed in the official client; see the skill reference.
No vendor player source or real key values are bundled.
"""

ORDERS_21 = {4: ((4, 13, 19, 14, 0, 3, 16, 18, 9, 2, 11, 6, 8, 1, 5, 12),
     (7, 15, 13, 4, 0, 9, 12, 17, 14, 16, 18, 3, 6, 11, 8, 2),
     (17, 0, 13, 3, 11, 6, 15, 2, 12, 14, 4, 1, 18, 10, 7, 19)),
 5: ((18, 5, 6, 4, 16, 2, 12, 0, 15, 7, 9, 3, 13, 19, 17, 14),
     (1, 15, 0, 18, 7, 2, 5, 4, 11, 13, 14, 10, 12, 17, 6, 8),
     (19, 2, 12, 1, 18, 13, 5, 8, 7, 6, 9, 11, 0, 17, 10, 16)),
 6: ((7, 8, 4, 0, 10, 14, 15, 16, 5, 18, 12, 1, 6, 13, 17, 9),
     (15, 0, 12, 2, 6, 10, 16, 11, 19, 18, 4, 17, 5, 8, 14, 1),
     (16, 18, 13, 6, 17, 0, 15, 3, 19, 10, 11, 12, 5, 2, 14, 4)),
 7: ((2, 12, 16, 7, 3, 4, 18, 19, 8, 1, 15, 13, 9, 5, 17, 10),
     (1, 6, 9, 15, 8, 14, 16, 12, 3, 13, 4, 18, 5, 17, 7, 2),
     (15, 7, 10, 8, 17, 4, 14, 6, 18, 11, 0, 9, 12, 5, 3, 16)),
 8: ((2, 17, 1, 11, 19, 13, 6, 3, 18, 4, 9, 16, 12, 15, 7, 0),
     (9, 4, 17, 1, 8, 2, 12, 0, 6, 7, 14, 19, 5, 11, 15, 13),
     (16, 8, 5, 3, 1, 6, 11, 12, 2, 7, 13, 0, 19, 18, 9, 4)),
 9: ((5, 19, 15, 1, 17, 13, 12, 10, 16, 14, 7, 0, 18, 2, 6, 9),
     (13, 0, 5, 4, 1, 19, 2, 12, 18, 14, 9, 17, 10, 15, 8, 16),
     (12, 8, 0, 9, 19, 5, 1, 16, 10, 18, 13, 6, 17, 7, 15, 14)),
 10: ((9, 10, 3, 19, 1, 12, 6, 4, 18, 14, 16, 15, 5, 2, 17, 8),
      (12, 13, 14, 3, 17, 19, 15, 7, 5, 10, 9, 6, 16, 11, 1, 0),
      (19, 15, 0, 4, 12, 1, 3, 2, 18, 7, 10, 6, 11, 14, 13, 5))}

ORDERS_20 = {1: {0: (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 14, 15, 16, 18),
     1: (0, 1, 2, 3, 4, 5, 6, 7, 18, 16, 15, 13, 12, 11, 10, 8)},
 2: {0: (0, 1, 2, 12, 13, 14, 15, 16, 17, 18, 4, 5, 6, 7, 9, 10),
     1: (0, 1, 2, 3, 4, 12, 13, 14, 7, 6, 18, 17, 15, 8, 9, 10)},
 3: {0: (0, 1, 2, 3, 4, 15, 16, 17, 18, 10, 11, 12, 13, 6, 7, 8),
     1: (0, 1, 2, 8, 9, 10, 11, 12, 18, 17, 16, 15, 14, 4, 5, 6)}}


class UnsupportedKeyFormat(ValueError):
    pass


def normalize_key(data, key_format="standard", version=None):
    if key_format not in ("standard", "qiqiuyun"):
        raise UnsupportedKeyFormat("Unknown key format")
    if key_format == "qiqiuyun" and version not in range(1, 11):
        raise UnsupportedKeyFormat("Unverified key format version")
    if len(data) == 16:
        return bytes(data)
    if key_format == "standard":
        raise UnsupportedKeyFormat("Standard AES-128 requires a 16-byte key")
    if version <= 3 and len(data) == 17:
        raw = data[1:]
        return bytes(raw[i] for i in (8,9,2,3,4,5,6,7,0,1,10,11,12,13,14,15))
    if version >= 4 and len(data) == 21 and data[-1] in b"012":
        return bytes(data[i] for i in ORDERS_21[version][data[-1] - 48])
    if version <= 3 and len(data) == 20:
        try:
            position = int(chr(data[0]).lower(), 36) % (7 if version == 1 else 2)
            algorithm = int(data[position:position+2].decode("ascii"), 36) % 3
            if algorithm in (0, 1):
                return bytes(data[i] for i in ORDERS_20[version][algorithm])
            pairs = ((8,9,10,11,15,16,17,18), (3,4,8,9,14,15,18,19), (5,6,9,10,13,14,17,18))[version-1]
            decoded = [data[pairs[i]] - 97 + 26 * (int(chr(data[pairs[i+1]])) + (2 if i == 6 else 1)) - 97 for i in (0,2,4,6)]
            layouts = ((0,1,2,3,4,5,6,7,"a","b",12,13,14,"c","d",19), (0,1,2,"a",5,6,7,"b",10,11,12,13,"c",16,17,"d"), (0,1,2,3,4,"a",7,8,"b",11,12,"c",15,16,"d",19))
            replacements = dict(zip("abcd", decoded))
            return bytes((data[x] if isinstance(x,int) else replacements[x]) & 255 for x in layouts[version-1])
        except (ValueError, IndexError, UnicodeError) as error:
            raise UnsupportedKeyFormat("Malformed versioned key response") from error
    raise UnsupportedKeyFormat("Unsupported key response length or marker")
