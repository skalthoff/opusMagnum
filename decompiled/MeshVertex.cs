using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Sequential, Pack = 1)]
public struct MeshVertex
{
	public Vector3 Position;

	public Vector3 Normal;

	public Vector2 TexCoord0;

	public Vector2 TexCoord1;

	public _0023_003DqQXklCRBuCAYi_RrjcxDZSQ_003D_003D Color;

	public MeshVertex(Vector3 position, Vector3 normal, Vector2 texCoord0, Vector2 texCoord1, _0023_003DqQXklCRBuCAYi_RrjcxDZSQ_003D_003D color)
	{
		Position = position;
		Normal = normal;
		TexCoord0 = texCoord0;
		TexCoord1 = texCoord1;
		Color = color;
	}
}
