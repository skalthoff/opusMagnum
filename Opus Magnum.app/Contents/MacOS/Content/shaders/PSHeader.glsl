#version 330 core

uniform sampler2D Texture0;
uniform sampler2D Texture1;
uniform sampler2D Texture2;
uniform sampler2D Texture3;
uniform sampler2D Texture4;
uniform sampler2D Texture5;
uniform sampler2D Texture6;
uniform sampler2D Texture7;

layout(std140) uniform PerFrame
{
    float Time;
    // VisibleBounds = float4(left, bottom, width, height)
    vec4 VisibleBounds;
};

layout(std140) uniform PerCamera
{
    mat4 ProjectionMatrix;
    mat4 ViewMatrix;
};

layout(std140) uniform PerMesh
{
    mat4 ModelMatrix;
    vec4 MeshColorRaw;
};

in vec3 fragPosition;
in vec3 fragNormal;
in vec2 fragTexCoord0;
in vec2 fragTexCoord1;
in vec4 fragColor;

out vec4 Output;

//=========================================================
// Functions for HLSL compatibility
//=========================================================

float saturate(float x)
{
    return clamp(x, 0.0, 1.0);
}

float lerp(float a, float b, float s)
{
    return mix(a, b, s);
}

vec2 lerp(vec2 a, vec2 b, float s)
{
    return mix(a, b, s);
}

vec3 lerp(vec3 a, vec3 b, float s)
{
    return mix(a, b, s);
}

vec4 lerp(vec4 a, vec4 b, float s)
{
    return mix(a, b, s);
}

float atan2(float y, float x)
{
    return atan(y, x);
}

//=========================================================
// Various helper functions
//=========================================================

float SrgbToLinear(float x)
{
    if (x <= 0.04045)
    {
        return x / 12.92;
    }
    else
    {
        return pow((abs(x) + 0.055) / 1.055, 2.4);
    }
}

vec3 SrgbToLinear(vec3 color)
{
    return vec3(SrgbToLinear(color.r), SrgbToLinear(color.g), SrgbToLinear(color.b));
}

float LinearToSrgb(float x)
{
    if (x <= 0.0031308)
    {
        return x * 12.92;
    }
    else
    {
        return 1.055 * pow(abs(x), 1.0 / 2.4) - 0.055;
    }
}

vec3 LinearToSrgb(vec3 color)
{
    return vec3(LinearToSrgb(color.r), LinearToSrgb(color.g), LinearToSrgb(color.b));
}

// Colors specified as parameters need to have their alpha multiplied.
vec4 DecodeColor(vec4 color)
{
    color.rgb *= color.a;
    return color;
}

float ToGrayscale(vec3 rgb)
{
    return dot(rgb, vec3(0.21, 0.72, 0.07));
}

vec2 RotatedZ(vec2 v, float radians)
{
    float sinr = sin(radians);
    float cosr = cos(radians);
    return vec2(v.x * cosr - v.y * sinr, v.x * sinr + v.y * cosr);
}

vec3 RotatedZ(vec3 v, float radians)
{
    float sinr = sin(radians);
    float cosr = cos(radians);
    return vec3(v.x * cosr - v.y * sinr, v.x * sinr + v.y * cosr, v.z);
}

vec3 LightPos()
{
    return vec3(
        VisibleBounds.x + 0.5 * VisibleBounds.z,
        (VisibleBounds.y + VisibleBounds.w) * 1.05,
        1200.0);
}

float LightRadius()
{
    return VisibleBounds.w * 1.45;
}

vec4 Blend(vec4 dst, vec4 src)
{
    dst.rgb = dst.rgb * (1.0 - src.a) + src.rgb;
    dst.a += src.a;
    return dst;
}

float Overlay(float dst, float src)
{
    if (dst < 0.5) return 2.0 * dst * src;
    else return 1.0 - 2.0 * (1.0 - dst) * (1.0 - src);
}

vec3 Overlay(vec3 dst, float src)
{
    return vec3(Overlay(dst.r, src), Overlay(dst.g, src), Overlay(dst.b, src));
}

vec2 RotatedTexCoord(vec2 texCoord, float angle)
{
    return 0.5 + RotatedZ(texCoord - 0.5, angle);
}

// Calculate shadow effect based on height.
float Shadow(vec2 texCoord, float height)
{
    float radius = saturate(distance(texCoord, vec2(0.5, 0.5)));
    float shadow = smoothstep(height, height - 0.1, radius) * height;
    return shadow;
}

vec3 AdjustSaturation(vec3 color, float adjustment)
{
    const vec3 mat = vec3(0.2125, 0.7154, 0.0721);
    float i = dot(color, mat);
    vec3 intensity = vec3(i, i, i);
    return lerp(intensity, color, adjustment);
}
