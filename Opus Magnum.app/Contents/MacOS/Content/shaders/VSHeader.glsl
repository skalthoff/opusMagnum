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

in vec3 Position;
in vec3 Normal;
in vec2 TexCoord0;
in vec2 TexCoord1;
in vec4 ColorRaw;

out vec3 fragPosition;
out vec3 fragNormal;
out vec2 fragTexCoord0;
out vec2 fragTexCoord1;
out vec4 fragColor;

// Colors specified as parameters need to have their alpha multiplied.
vec4 DecodeColor(vec4 color)
{
    color.rgb *= color.a;
    return color;
}
