
void main()
{
    vec3 lightPos = LightPos();
    vec3 lightVec = normalize(lightPos - vec3(fragPosition.xy, 0.0));
    float lightAngle = -atan2(lightVec.y, lightVec.x) + (3.14159 / 2.0);
    vec2 litTexCoord = RotatedTexCoord(fragTexCoord0, lightAngle);

    float height = fragColor.r;
    vec4 tex = texture(Texture0, litTexCoord);
    vec3 base = tex.rgb;
    vec4 fog       = texture(Texture1, fragTexCoord0);
    vec4 base2     = texture(Texture2, litTexCoord);
    vec4 envlights = texture(Texture3, fragTexCoord0);
    vec4 highlight = texture(Texture4, litTexCoord);
    vec4 symbol    = texture(Texture5, fragTexCoord0);
    float mask       = texture(Texture7, fragTexCoord0).a;
    float opacity = fragColor.g * tex.a * mask;

    Output.rgb = base;
    Output.rgb = Output.rgb * (1.0 - fog.a) + fog.rgb;
    Output.rgb = Output.rgb * (1.0 - base2.a) + base2.rgb;
    Output.rgb = Output.rgb * (1.0 - envlights.a) + envlights.rgb;
    Output.rgb = Output.rgb * (1.0 - highlight.a) + highlight.rgb;
    Output.rgb = Output.rgb * (1.0 - symbol.a) + symbol.rgb;

    // Slightly increase the saturation of output preview molecules:
    float isOutput = fragColor.b;
    Output.rgb = AdjustSaturation(Output.rgb, 1.0 + 0.25 * isOutput);
    
    Output.rgb *= Shadow(fragTexCoord0, height);
    Output.rgb *= opacity;
    Output.a = opacity;
}
