using System;
using System.Runtime.InteropServices;
using SDL2;

public static class _0023_003Dqqo4xMcVklrj_0024daF4p_p2Sg_003D_003D
{
	public enum _0023_003Dq6HpcG3cybtTLTAWbLMnIqQ_003D_003D
	{

	}

	public static void _0023_003Dq25qXFdisgrBs7XrB78g5p6A3Wb2wR5hi3Lk_00248VUufb8_003D(out SDL.SDL_version _0023_003Dqsb48xDzazRqTQ7rQlukuOQ_003D_003D)
	{
		_0023_003Dqsb48xDzazRqTQ7rQlukuOQ_003D_003D.major = 2;
		_0023_003Dqsb48xDzazRqTQ7rQlukuOQ_003D_003D.minor = 0;
		_0023_003Dqsb48xDzazRqTQ7rQlukuOQ_003D_003D.patch = 0;
	}

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_LinkedVersion")]
	private static extern IntPtr _0023_003DqeldQCR6P6xjrEKA8k_0024aIED7a3qajUXhvMa_0024QQpeTVx8_003D();

	public static SDL.SDL_version _0023_003DqVRxdYU3oG5IQgmsn6rNo7HxUvdjrs7HXFr8NNqTcoVE_003D()
	{
		return (SDL.SDL_version)Marshal.PtrToStructure(_0023_003DqeldQCR6P6xjrEKA8k_0024aIED7a3qajUXhvMa_0024QQpeTVx8_003D(), typeof(SDL.SDL_version));
	}

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_Init")]
	public static extern int _0023_003Dq9inG2pZF94N1Mhli8YXDIQ_003D_003D(_0023_003Dq6HpcG3cybtTLTAWbLMnIqQ_003D_003D _0023_003Dq69uVb_ATvSpslsDYpUQdLA_003D_003D);

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_Quit")]
	public static extern void _0023_003DqNrOthD2ASek1ngu7B6_Flg_003D_003D();

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_Load")]
	public static extern IntPtr _0023_003Dq8_0024BqXXaUlnVIxMY2b_0024qfkA_003D_003D([In][MarshalAs(UnmanagedType.CustomMarshaler, MarshalType = "SDL2.LPUtf8StrMarshaler")] string _0023_003Dqh7tROlVo9_0024CX8FbQT8yyOA_003D_003D);

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_Load_RW")]
	public static extern IntPtr _0023_003DqCmXqUCt3WicM3vNmTlE5JQ_003D_003D(IntPtr _0023_003DquCin66hEGySKSBtsRwFipA_003D_003D, int _0023_003DqRTDB1T1XHy5a_3Qv0Lt3HQ_003D_003D);

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_LoadTyped_RW")]
	public static extern IntPtr _0023_003DqhmjuUA9PudO_1dh5VPOUUcvBF0z3N_0024SAE_0024HCnpTI1xQ_003D(IntPtr _0023_003DqUGMs2CfbUagR8Jcb2i67BQ_003D_003D, int _0023_003DqZvxY_0024uE8C6JxhgMoUHZ5Ng_003D_003D, [In][MarshalAs(UnmanagedType.CustomMarshaler, MarshalType = "SDL2.LPUtf8StrMarshaler")] string _0023_003DqMcJlm475v6pIPJ4g0WCbVg_003D_003D);

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_LoadTexture")]
	public static extern IntPtr _0023_003DqS8P237cpiGu1lSwgpawxKRTGp65PqmMQM_0024Up7rGSiIc_003D(IntPtr _0023_003DqWW332WcIg7_T4qBTGiVNzQ_003D_003D, [In][MarshalAs(UnmanagedType.CustomMarshaler, MarshalType = "SDL2.LPUtf8StrMarshaler")] string _0023_003DqVJ_YyR8nFjd_0024LOTQE1QaRw_003D_003D);

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_LoadTexture_RW")]
	public static extern IntPtr _0023_003DqHlKlvKKCQ9IvC8ataD49nKxoiKv1wAQyKhozl08gYaY_003D(IntPtr _0023_003DqGc7xpypZTMQ7Sek6uBw3KQ_003D_003D, IntPtr _0023_003DqdaVnHFO1mxyG0LJ6tm_J8A_003D_003D, int _0023_003DqOEDO69cuQ1RuVmmMc6pWhA_003D_003D);

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_LoadTextureTyped_RW")]
	public static extern IntPtr _0023_003DqgFS_0024cWyaLbmYQXuMqmXWt_0024rELD8lQ5qtL61jyKVUyBk_003D(IntPtr _0023_003DqmLKoM7JTyn3qFZ4E8_0024a3yg_003D_003D, IntPtr _0023_003Dq47RjNB1ckZ5w0nKeIgICSg_003D_003D, int _0023_003DqQ7XlEr3TfE816v0_r58wfg_003D_003D, [In][MarshalAs(UnmanagedType.CustomMarshaler, MarshalType = "SDL2.LPUtf8StrMarshaler")] string _0023_003Dqd4jaAh0R79mfiQtTUfN9kA_003D_003D);

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_InvertAlpha")]
	public static extern int _0023_003DqU4_UyK3Z3jpai7eSlnMnokUS7ae6Q_k8ZJy6DXSaBFc_003D(int _0023_003Dq1D1Jkn6SmVH_TbI9orxvwQ_003D_003D);

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_ReadXPMFromArray")]
	public static extern IntPtr _0023_003DqliMUyaphWykShGfzIfrXpM4Xu4r5QbFI3lG8ZsCs0W0_003D([In][MarshalAs(UnmanagedType.LPArray, ArraySubType = UnmanagedType.LPStr, SizeConst = 0)] string[] _0023_003DqjRO4NP7hC4xDMsPaiES_jg_003D_003D);

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_SavePNG")]
	public static extern int _0023_003DqNujNWDajGFdj7hAV_4Ug3g_003D_003D(IntPtr _0023_003DqVjztt7YImZ0D6SEj5ThtVg_003D_003D, [In][MarshalAs(UnmanagedType.CustomMarshaler, MarshalType = "SDL2.LPUtf8StrMarshaler")] string _0023_003DqkS0pzarL0bry7oab77YCWA_003D_003D);

	[DllImport("SDL2_image.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "IMG_SavePNG_RW")]
	public static extern int _0023_003DqT1Ye40JiPPDImcxOIAPI7A_003D_003D(IntPtr _0023_003DqJ_zif80mz9iwWc56FRTs3w_003D_003D, IntPtr _0023_003DqgZiZX4NFG6_0024AqVuw7dyyWg_003D_003D, int _0023_003DqzaRcJJqG7TPKaZQwFRXL_0024w_003D_003D);
}
