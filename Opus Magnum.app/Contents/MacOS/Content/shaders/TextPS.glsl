
void main()
{
    float alpha = texture(Texture0, fragTexCoord0).r;
    vec3 gradient = texture(Texture1, fragTexCoord1).rgb;
    Output.rgb = fragColor.rgb * gradient * alpha;
    Output.a = fragColor.a * alpha;
}
