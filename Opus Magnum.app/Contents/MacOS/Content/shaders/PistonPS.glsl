
void main()
{
    float partAngle = fragTexCoord1.x;
    vec2 lightPos = LightPos().xy;
    vec2 lightVec = normalize(lightPos - fragPosition.xy);

    // The lit and unlit appearances of this pixel come from the top and
    // bottom halves of the texture:
    vec2 coordLight, coordDark;
    coordLight.x = fragTexCoord0.x;
    coordDark.x = fragTexCoord0.x;
    coordLight.y = max(fragTexCoord0.y, 1.0 - fragTexCoord0.y);
    coordDark.y = min(fragTexCoord0.y, 1.0 - fragTexCoord0.y);
    vec4 light = texture(Texture0, coordLight);
    vec4 dark = texture(Texture0, coordDark);
    float opacity = light.a;

    // All parts of the piston arm face either directly up or directly down.
    vec2 normal;
    normal.x = 0.0;
    normal.y = fragTexCoord0.y > 0.5 ? 1.0 : -1.0;

    // Transform the normal from local to world space.
    normal = RotatedZ(normal, partAngle);

    // Calculate the intensity of the lighting on this pixel.
    float illumination = saturate(0.25 + 0.75 * dot(normal, lightVec));

    Output.rgb = lerp(dark.rgb, light.rgb, illumination);
    Output.a = opacity;
}
