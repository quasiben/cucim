
# Changelog

## 0.18.2 (2021-03-29)

- Use the white background only for Philips TIFF file.
  - Generic TIFF file would have the black background by default.
- Fix upside-downed image for TIFF file if the image is not RGB & tiled image with JPEG/Deflate-compressed tiles.
  - Use slow path if the image is not RGB & tiled image with JPEG/Deflate-compressed tiles.
    - Show an error message if the out-of-boundary cases are requested with the slow path.
    - `ValueError: Cannot handle the out-of-boundary cases for a non-RGB image or a non-Jpeg/Deflate-compressed image.`

## 0.18.1 (2021-03-17)

- Disable using cuFile
  - Remove warning messages when libcufile.so is not available.
    - `[warning] CuFileDriver cannot be open. Falling back to use POSIX file IO APIs.`

## 0.18.0 (2021-03-16)

- First release on PyPI with only cuClaraImage features.
- The namespace of the project is changed from `cuimage` to `cucim` and project name is now `cuCIM`
- Support Deflate(zlib) compression in Generic TIFF Format.
  - [libdeflate](https://github.com/ebiggers/libdeflate) library is used to decode the deflate-compressed data.
