
void main()
{
    vec2 glossOffset = fragTexCoord1.xy;
    float mask = texture(Texture0, fragTexCoord0).a;
    vec4 gloss = texture(Texture1, fragTexCoord0 + glossOffset);

    Output.rgb = gloss.rgb * mask;
    Output.a = gloss.a * mask;
}
