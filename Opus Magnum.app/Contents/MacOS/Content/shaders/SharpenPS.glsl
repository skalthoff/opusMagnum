
vec3 SharpenSample(float weight, vec2 texCoord)
{
    return weight * texture(Texture0, texCoord).rgb;
}

void main()
{
    // This value controls the strength of the sharpen effect:
    float p = fragColor.r;

    vec2 t = fragTexCoord0;
    float dx = 1.0 / fragTexCoord1.x;
    float dy = 1.0 / fragTexCoord1.y;
    vec3 color = vec3(0.0, 0.0, 0.0);
    color += SharpenSample(1.0 + 8.0 * p, t + vec2(0.0, 0.0));
    color += SharpenSample(-p, t + vec2(-dx, -dy));
    color += SharpenSample(-p, t + vec2(-dx, 0.0));
    color += SharpenSample(-p, t + vec2(-dx, +dy));
    color += SharpenSample(-p, t + vec2(0.0, -dy));
    color += SharpenSample(-p, t + vec2(0.0, +dy));
    color += SharpenSample(-p, t + vec2(+dx, -dy));
    color += SharpenSample(-p, t + vec2(+dx, 0.0));
    color += SharpenSample(-p, t + vec2(+dx, +dy));

    Output.rgb = color;
    Output.a = 1.0;
}
