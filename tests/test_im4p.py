from pathlib import Path

import pyimg4


def test_input_lzss(dec_lzss) -> None:
    im4p = pyimg4.IM4P(dec_lzss)

    assert im4p.payload.compression == pyimg4.Compression.LZSS

    im4p.payload.decompress()

    assert im4p.payload.compression == pyimg4.Compression.NONE


def test_input_lzfse_dec(dec_lzfse) -> None:
    im4p = pyimg4.IM4P(dec_lzfse)

    assert im4p.payload.compression == pyimg4.Compression.LZFSE

    im4p.payload.decompress()

    assert im4p.payload.compression == pyimg4.Compression.NONE


def test_input_lzfse_enc(enc_lzfse) -> None:
    im4p = pyimg4.IM4P(enc_lzfse)

    assert im4p.payload.encrypted == True

    dec_kbag = pyimg4.Keybag(
        iv='0d0a39d2e3ea94f70076192e7d225e9e',
        key='4567c8444b839a08b4a7c408531efb54ae69f1dcc24557ad0e21768b472f95cd',
    )

    im4p.payload.decrypt(dec_kbag)

    assert im4p.payload.compression == pyimg4.Compression.LZFSE

    im4p.payload.decompress()

    assert im4p.payload.compression == pyimg4.Compression.NONE


def test_create_lzss() -> None:
    with (Path(__file__).parent / 'bin' / 'test_payload').open('rb') as f:
        payload = pyimg4.IM4PData(f.read())

    assert payload.compression == pyimg4.Compression.NONE
    assert payload.encrypted == False

    payload.compress(pyimg4.Compression.LZSS)

    im4p = payload.create_im4p('test', 'Test IM4P file.')

    assert im4p.fourcc == 'test'
    assert im4p.description == 'Test IM4P file.'

    assert im4p.payload.compression == pyimg4.Compression.LZSS
    assert im4p.payload.encrypted == False


def test_create_lzfse() -> None:
    with (Path(__file__).parent / 'bin' / 'test_payload').open('rb') as f:
        payload = pyimg4.IM4PData(f.read())

    assert payload.compression == pyimg4.Compression.NONE
    assert payload.encrypted == False

    payload.compress(pyimg4.Compression.LZFSE)

    im4p = payload.create_im4p('test', 'Test IM4P file.')

    assert im4p.fourcc == 'test'
    assert im4p.description == 'Test IM4P file.'

    assert im4p.payload.compression == pyimg4.Compression.LZFSE
    assert im4p.payload.encrypted == False
