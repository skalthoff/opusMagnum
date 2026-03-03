
void main()
{
    vec3 lightPos = LightPos();
    vec3 lightVec = normalize(lightPos - vec3(fragPosition.xy, 0.0));
    float lightAngle = -atan2(lightVec.y, lightVec.x) + (3.14159 / 2.0);
    vec2 litTexCoord = RotatedTexCoord(fragTexCoord0, lightAngle);

    float height = fragColor.r;
    vec4 base       = texture(Texture0, litTexCoord);
    vec4 colors     = texture(Texture1, fragTexCoord0);
    vec4 colorsMask = texture(Texture2, litTexCoord);
    vec4 rimlight   = texture(Texture3, litTexCoord);
    vec4 envlights  = texture(Texture4, fragTexCoord0);
    vec4 highlight  = texture(Texture5, litTexCoord);
    vec4 symbol     = texture(Texture6, fragTexCoord0);
    float opacity = fragColor.g;

    Output = base;
    Output = Blend(Output, colors * colorsMask.r);
    Output = Blend(Output, rimlight);
    Output = Blend(Output, envlights);
    Output = Blend(Output, highlight);
    Output = Blend(Output, symbol);

    // Slightly increase the saturation of output preview molecules:
    float isOutput = fragColor.b;
    Output.rgb = AdjustSaturation(Output.rgb, 1.0 + 0.25 * isOutput);
    
    Output.rgb *= Shadow(fragTexCoord0, height);
    Output *= opacity;
}
