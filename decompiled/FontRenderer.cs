using System;
using System.Runtime.InteropServices;

public static class FontRenderer
{
	[DllImport("Renderer_D3D11", CallingConvention = CallingConvention.Cdecl)]
	public static extern IntPtr CreateFontRenderer([MarshalAs(UnmanagedType.LPStr)] string fontFilename, float pointSize, out float ascent, out float descent, out float lineAdvance);

	[DllImport("Renderer_D3D11", CallingConvention = CallingConvention.Cdecl)]
	public static extern IntPtr DestroyFontRenderer(IntPtr fontRenderer);

	[DllImport("Renderer_D3D11", CallingConvention = CallingConvention.Cdecl)]
	public static extern int GetGlyphIndex(IntPtr fontRenderer, int codepoint);

	[DllImport("Renderer_D3D11", CallingConvention = CallingConvention.Cdecl)]
	public static extern void GetGlyphBitmap(IntPtr fontRenderer, int glyphIndex, byte[] bitmap, out int bitmapWidth, out int bitmapHeight, out int offsetX, out int offsetY, out float advanceX);
}
