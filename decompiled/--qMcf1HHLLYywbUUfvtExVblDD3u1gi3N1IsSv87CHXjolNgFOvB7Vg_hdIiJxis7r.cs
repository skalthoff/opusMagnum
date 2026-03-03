using System;
using System.Runtime.InteropServices;

public static class _0023_003DqMcf1HHLLYywbUUfvtExVblDD3u1gi3N1IsSv87CHXjolNgFOvB7Vg_hdIiJxis7r
{
	public struct _0023_003DqT8FInhhYLD32p0U55CV0ng_003D_003D
	{
		public int _0023_003Dqiq3ZXGu1D7wp1xyDYsStfw_003D_003D;

		public int _0023_003DqG1f28Rr_iZIEJYGjV4KfiA_003D_003D;

		public long _0023_003DqLPtjn_RBdH6q92fppaUrpw_003D_003D;

		public long _0023_003DqHHG3gewt3wmDHqto80bh6A_003D_003D;

		public long _0023_003DqqXcST2gulfJC9thd6GCtTdUjGiaA2eanIja9sP2Rak8_003D;

		public long _0023_003DqhNaDVfILdb5cs2V2b4fp_0024w_003D_003D;

		public long _0023_003DqcXB_OVjFr5di_0024AECp9ft1A_003D_003D;

		public IntPtr _0023_003DqnAAztXvkN05JSWzLXB9Rlw_003D_003D;
	}

	public static IntPtr _0023_003Dq9_TeOmVmHQxe88rm9jy9gZYpRl9g_HP66QVVHkJ0Wx0_003D()
	{
		return Marshal.AllocHGlobal(4096);
	}

	[DllImport("libvorbisfile-3.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "ov_clear")]
	public static extern int _0023_003DqiDg7auILN1W_YcaszO_0024HKA_003D_003D(IntPtr _0023_003DqzarXEJlw32bpFSutpqsYww_003D_003D);

	[DllImport("libvorbisfile-3.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "ov_fopen")]
	public static extern int _0023_003DqHn9YX7dVrjqIkX4s_0024hHGkA_003D_003D(string _0023_003DqES7K_0024e7gJe6qZroZUpBTtA_003D_003D, IntPtr _0023_003DqlS8MPPu416QqGCptE19E6A_003D_003D);

	[DllImport("libvorbisfile-3.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "ov_streams")]
	public static extern int _0023_003Dqyty_eN8p0M5hpXUCvbtf9A_003D_003D(IntPtr _0023_003Dqwt1BedkJwBDKE5wmINWOMA_003D_003D);

	[DllImport("libvorbisfile-3.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "ov_info")]
	public static extern IntPtr _0023_003Dqfhiw30e33XkxShprYxInXA_003D_003D(IntPtr _0023_003DqocW_AbE_rR6IN2IxwJ0czw_003D_003D, int _0023_003DqBnNAs2b8g1Rn1_6raUHdSg_003D_003D);

	[DllImport("libvorbisfile-3.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "ov_read")]
	public unsafe static extern int _0023_003Dq2ydrvkb0DxWDfT1E3gqmdQ_003D_003D(IntPtr _0023_003DqETdUC6_8jZxZJjyNx6hE7w_003D_003D, byte* _0023_003Dq7yJWA_0024OTCdtx0X7CmXPnXA_003D_003D, int _0023_003DqTmum_0024u5BIkeg9mC4NzozqQ_003D_003D, int _0023_003Dq9qtlUWNf96I51tX0EkTJrQ_003D_003D, int _0023_003DqF8TKI5TjtEdykt1JnppvPA_003D_003D, int _0023_003DqKNWh5K0nafxhTRbiyfzirw_003D_003D, out int _0023_003DqRxdgCa4Ub1SVwBC9F3013g_003D_003D);

	[DllImport("libvorbisfile-3.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "ov_time_seek")]
	public static extern int _0023_003DqZVXAxbqBob_5OpcNl6jofw_003D_003D(IntPtr _0023_003DqfCfOJfTCevus2jJZbAebcA_003D_003D, double _0023_003DqV_IdtdfqgGeC2vIieDW78w_003D_003D);
}
