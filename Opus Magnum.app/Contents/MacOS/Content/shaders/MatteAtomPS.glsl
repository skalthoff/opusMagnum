
void main()
{
    vec3 lightPos = LightPos();
    vec3 lightVec = normalize(lightPos - vec3(fragPosition.xy, 0.0));
    float lightAngle = -atan2(lightVec.y, lightVec.x) + (3.14159 / 2.0);
    vec2 litTexCoord = RotatedTexCoord(fragTexCoord0, lightAngle);

    float height = fragColor.r;
    vec4 tex = texture(Texture0, fragTexCoord0);
    float mask = texture(Texture7, fragTexCoord0).a;
    vec3 base = tex.rgb;
    float opacity = fragColor.g * tex.a * mask;
    vec4 shade = texture(Texture1, litTexCoord);
    vec4 symbol = texture(Texture2, fragTexCoord0);

    Output.rgb = base;
    Output.rgb = Output.rgb * (1.0 - shade.a) + shade.rgb;
    Output.rgb = Output.rgb * (1.0 - symbol.a) + symbol.rgb;

    // Slightly increase the saturation of output preview molecules:
    float isOutput = fragColor.b;
    Output.rgb = AdjustSaturation(Output.rgb, 1.0 + 0.5 * isOutput);

    Output.rgb *= Shadow(fragTexCoord0, height);
    Output.rgb *= opacity;
    Output.a = opacity;
}
