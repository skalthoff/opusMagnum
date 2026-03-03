
void main()
{
    vec4 tex = texture(Texture0, fragTexCoord0);
    Output = fragColor * tex;
}
