
void main()
{
	vec4 wood = texture(Texture0, fragTexCoord0);
	float mask = texture(Texture1, fragTexCoord0).r;
	Output = wood * mask;
}
