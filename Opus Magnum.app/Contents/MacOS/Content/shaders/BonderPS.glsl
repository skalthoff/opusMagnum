
void main()
{
    float angle = fragTexCoord1.x;

    vec2 lightPos = LightPos().xy;
    vec3 lightVec = vec3(normalize(lightPos - fragPosition.xy), 0.0);

    // Transform light vector into local coords.
    lightVec = RotatedZ(lightVec, -angle);
    // Calculate the brightness of the light falling on this part of the cylinder:
    float cylinderY = lerp(1.0, -1.0, fragTexCoord0.y);
    float lightY = lightVec.y;
    float brightness = 1.0 - (0.5 * abs(cylinderY - lightY));

    float pattern = texture(Texture0, fragTexCoord0).a;
    vec3 lightColor = texture(Texture1, vec2(brightness, fragTexCoord0.x)).rgb;
    float opacity = texture(Texture2, fragTexCoord0).a;

    Output.rgb = lightColor * (1.0 - 0.7 * pattern) * opacity;
    Output.a = opacity;
}
