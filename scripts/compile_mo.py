"""
Pure-Python GNU gettext MO compiler.
Zero external dependency (no gettext or msgfmt binary required).
Reads .po files and compiles them to binary .mo format.
"""

import struct
from pathlib import Path


def parse_po_file(filepath):
    """
    Parses a .po file into a list of (msgid, msgstr) tuples.
    Properly handles multiline strings and escape sequences.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    current_msgid = None
    current_msgstr = None
    state = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            if current_msgid is not None and current_msgstr is not None:
                entries.append((current_msgid, current_msgstr))
                current_msgid = None
                current_msgstr = None
                state = None
            continue

        if line.startswith("msgid "):
            if current_msgid is not None and current_msgstr is not None:
                entries.append((current_msgid, current_msgstr))
                current_msgid = None
                current_msgstr = None
            state = "msgid"
            current_msgid = eval(line[6:].strip())
        elif line.startswith("msgstr "):
            state = "msgstr"
            current_msgstr = eval(line[7:].strip())
        elif line.startswith('"') and state == "msgid":
            current_msgid += eval(line)
        elif line.startswith('"') and state == "msgstr":
            current_msgstr += eval(line)

    if current_msgid is not None and current_msgstr is not None:
        entries.append((current_msgid, current_msgstr))

    return entries


def generate_mo(entries):
    """
    Encodes list of (msgid, msgstr) tuples into GNU gettext binary MO format.
    Magic number: 0x950412de (little endian).
    """
    # Sort entries by UTF-8 bytes of msgid
    entries = sorted(entries, key=lambda x: x[0].encode("utf-8"))
    count = len(entries)

    header_size = 28
    orig_table_offset = header_size
    trans_table_offset = orig_table_offset + count * 8
    strings_start = trans_table_offset + count * 8

    orig_table = []
    trans_table = []
    strings_data = bytearray()

    for msgid, msgstr in entries:
        id_bytes = msgid.encode("utf-8") + b"\x00"
        str_bytes = msgstr.encode("utf-8") + b"\x00"

        orig_offset = strings_start + len(strings_data)
        orig_table.append((len(id_bytes) - 1, orig_offset))
        strings_data.extend(id_bytes)

        trans_offset = strings_start + len(strings_data)
        trans_table.append((len(str_bytes) - 1, trans_offset))
        strings_data.extend(str_bytes)

    mo = bytearray()
    mo.extend(struct.pack("<Iiiiiii", 0x950412DE, 0, count, orig_table_offset, trans_table_offset, 0, 0))
    for length, offset in orig_table:
        mo.extend(struct.pack("<ii", length, offset))
    for length, offset in trans_table:
        mo.extend(struct.pack("<ii", length, offset))
    mo.extend(strings_data)
    return bytes(mo)


def compile_all(base_dir=None):
    """
    Compiles all .po files under locale/ to .mo files.
    """
    if base_dir is None:
        base_dir = Path(__file__).resolve().parent.parent

    locale_dir = base_dir / "locale"
    if not locale_dir.exists():
        print(f"Directory {locale_dir} does not exist.")
        return

    success_count = 0
    for po_path in locale_dir.glob("*/LC_MESSAGES/*.po"):
        mo_path = po_path.with_suffix(".mo")
        entries = parse_po_file(po_path)
        mo_bytes = generate_mo(entries)
        with open(mo_path, "wb") as f:
            f.write(mo_bytes)
        print(f"Compiled {len(entries)} strings: {po_path.name} -> {mo_path}")
        success_count += 1

    print(f"Successfully compiled {success_count} catalogs into binary MO format.")


if __name__ == "__main__":
    compile_all()
