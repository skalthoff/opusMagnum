
void main()
{
    vec4 worldPos = ModelMatrix * vec4(Position, 1.0);
    fragPosition = worldPos.xyz;
    fragNormal = Normal;
    fragTexCoord0 = TexCoord0;
    fragTexCoord1 = TexCoord1;
    fragColor = DecodeColor(MeshColorRaw) * DecodeColor(ColorRaw);
    gl_Position = ProjectionMatrix * ViewMatrix * worldPos;
}
