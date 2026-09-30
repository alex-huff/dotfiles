#language slang 2026

import kitty_custom_shader_types;

static const float BORDER_WIDTH = 2;
static const float GRAY_VALUE = 0.021219010;

public float4
fragment_main(float4 color, KittyTextures t, KittyCustomShaderData d) {
    int viewport_width = d.viewport_size_pixels[0];
    int viewport_height = d.viewport_size_pixels[1];
    float pixelX = t.pos[0] * viewport_width;
    float pixelY = t.pos[1] * viewport_height;
    if (
        pixelX < BORDER_WIDTH ||
        pixelY < BORDER_WIDTH ||
        pixelX > (viewport_width - BORDER_WIDTH) ||
        pixelY > (viewport_height - BORDER_WIDTH)
    ) {
        return float4(GRAY_VALUE, GRAY_VALUE, GRAY_VALUE, 1.0);
    }

    return color;
}
