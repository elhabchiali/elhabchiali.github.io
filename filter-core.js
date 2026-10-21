'use strict';
// Pure numerical core shared by the browser experiment and regression tests.
(function (root) {
  function applyKernel(pixels, width, height, coefficients, divisor = 1) {
    if (pixels.length !== width * height || coefficients.length !== 9 || !divisor) throw new Error('Invalid filter input');
    const output = new Float32Array(pixels.length);
    for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
      let sum = 0;
      for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) {
        const yy = Math.min(height - 1, Math.max(0, y + j));
        const xx = Math.min(width - 1, Math.max(0, x + i));
        sum += pixels[yy * width + xx] * coefficients[(j + 1) * 3 + i + 1];
      }
      output[y * width + x] = sum / divisor;
    }
    return output;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { applyKernel };
  else root.VisionFilters = { applyKernel };
})(typeof window !== 'undefined' ? window : {});
