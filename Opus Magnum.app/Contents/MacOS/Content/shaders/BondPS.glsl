
void main()
{
    const float highlightOpacity = 0.5;
    const float highlightSize = 5.0;

    float height = fragColor.r;
    float opacity = fragColor.g;
    vec3 highlightColor = vec3(0.91, 0.95, 0.95);
    float angle = fragTexCoord1.x;
    vec4 tex = texture(Texture0, fragTexCoord0);
    opacity *= tex.a;
    float normalY = texture(Texture1, fragTexCoord0).r;

    vec2 lightPos = LightPos().xy;
    vec3 lightVec = vec3(normalize(lightPos - fragPosition.xy), 0.0);

    // Transform light vector into local coords.
    lightVec = RotatedZ(lightVec, -angle);
    // Calculate the brightness of the light falling on this part of the cylinder:
    float lightY = 0.5 + 0.5 * lightVec.y;
    float highlight = highlightOpacity * saturate(1.0 - saturate(highlightSize * abs(normalY - lightY)));
    
    Output.rgb = tex.rgb + highlight * opacity * highlightColor;
    Output.rgb *= (height * opacity);
    Output.a = opacity;
}
