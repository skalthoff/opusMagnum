
void main()
{
    float specularPower = 5.0;

    float height = fragColor.r;
    float opacity = fragColor.g;

    vec3 lightPos = LightPos();
    vec3 lightVec = normalize(lightPos - vec3(fragPosition.xy, 0.0));
    float lightAngle = -atan2(lightVec.y, lightVec.x) + (3.14159 / 2.0);
    vec2 litTexCoord = RotatedTexCoord(fragTexCoord0, lightAngle);

    vec4 tex = texture(Texture4, fragTexCoord0);
    vec4 rimlight = texture(Texture6, litTexCoord);
    vec4 symbol = texture(Texture7, fragTexCoord0);
    vec3 albedo = tex.rgb;
    opacity *= tex.a;

    // Infer the normal vector of this pixel by looking at the difference in
    // lighting from opposite directions.
    float left   = texture(Texture0, fragTexCoord0).r;
    float right  = texture(Texture1, fragTexCoord0).r;
    float bottom = texture(Texture2, fragTexCoord0).r;
    float top    = texture(Texture3, fragTexCoord0).r;
    vec3 normal;
    normal.x = right - left;
    normal.y = top - bottom;
    normal.z = sqrt(1.0 - saturate(dot(normal.xy, normal.xy)));

    // HACK: The normal's inferred Z coordinate is noisy in partly transparent areas. Reduce that noise.
    normal.z *= smoothstep(0.95, 1.0, opacity);
    
    float diffuse = 0.5 + 0.5 * dot(normal, lightVec);
    vec3 lightramp = texture(Texture5, vec2(diffuse, 0.0)).rgb;

    Output.rgb = lightramp;
    Output.rgb = Output.rgb * (1.0 - symbol.a) + symbol.rgb;
    Output.rgb = Output.rgb * (1.0 - rimlight.a) + rimlight.rgb;

    // Slightly increase the saturation of output preview molecules:
    float isOutput = fragColor.b;
    Output.rgb = AdjustSaturation(Output.rgb, 1.0 + 0.25 * isOutput);

    Output.rgb *= Shadow(fragTexCoord0, height);
    Output.rgb *= opacity;
    Output.a = opacity;
}
