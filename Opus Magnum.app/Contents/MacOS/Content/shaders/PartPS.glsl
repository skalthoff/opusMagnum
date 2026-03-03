
void main()
{
    float partAngle = fragTexCoord1.x;
    vec2 lightPos = LightPos().xy;
    vec2 lightVec = normalize(lightPos - fragPosition.xy);

    vec4 left   = texture(Texture0, fragTexCoord0);
    vec4 right  = texture(Texture1, fragTexCoord0);
    vec4 bottom = texture(Texture2, fragTexCoord0);
    vec4 top    = texture(Texture3, fragTexCoord0);
    float opacity = left.a;

    // Determine how this pixel looks when fully lit and fully shadowed.
    // Intermediate lighting levels interpolate between these two color values.
    vec3 light = max(max(max(left.rgb, right.rgb), bottom.rgb), top.rgb);
    vec3 dark  = min(min(min(left.rgb, right.rgb), bottom.rgb), top.rgb);

    // Infer the normal vector of this pixel by looking at the difference in brightness
    // between textures that are lit from opposite directions.
    float left_gray   = ToGrayscale(left.rgb);
    float right_gray  = ToGrayscale(right.rgb);
    float bottom_gray = ToGrayscale(bottom.rgb);
    float top_gray    = ToGrayscale(top.rgb);
    vec2 normal;
    normal.x = right_gray - left_gray;
    normal.y = top_gray - bottom_gray;
    // Normalize the vector to compensate for pixels with dark albedo.
    normal = lerp(normal, normalize(normal), 0.5);

    // Transform the normal from local to world space.
    normal = RotatedZ(normal, partAngle);

    // Calculate the intensity of the lighting on this pixel.
    float illumination = dot(normal, lightVec);
    illumination = saturate(0.3 + 0.7 * illumination);

    // Apply the mask. (used for multi-arms)
    float mask = texture(Texture4, fragTexCoord0).r;

    Output.rgb = lerp(dark, light, illumination) * mask;
    Output.a = opacity * mask;
}
