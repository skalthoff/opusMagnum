internal static class _0023_003DqUVRKpJOdrDmWYOn_00240RZOGaxHIrgGQkHlI_a3NXXHMwOVYjt_n_AbEjryifcaqIG2
{
	public static byte[] _0023_003DqHphNwXOj6tfRhNZoZMAImQ_003D_003D(byte[] _0023_003DqmbXDBH9rhHm_YD3KUKwZfVpqrFTOyQ4Ky8x_fNqcmrA_003D, byte[] _0023_003DqDHcwibtG5aC8N_0024xqlxJ9qjU9svRnEClowNfa9Z_00247SP0_003D)
	{
		byte b = _0023_003DqmbXDBH9rhHm_YD3KUKwZfVpqrFTOyQ4Ky8x_fNqcmrA_003D[1];
		int num = _0023_003DqDHcwibtG5aC8N_0024xqlxJ9qjU9svRnEClowNfa9Z_00247SP0_003D.Length;
		byte b2 = (byte)((num + 11) ^ (b + 7));
		uint num2 = (uint)((_0023_003DqmbXDBH9rhHm_YD3KUKwZfVpqrFTOyQ4Ky8x_fNqcmrA_003D[0] | (_0023_003DqmbXDBH9rhHm_YD3KUKwZfVpqrFTOyQ4Ky8x_fNqcmrA_003D[2] << 8)) + (b2 << 3));
		ushort num3 = 0;
		for (int i = 0; i < num; i++)
		{
			if ((i & 1) == 0)
			{
				num2 = num2 * 214013 + 2531011;
				num3 = (ushort)(num2 >> 16);
			}
			byte b3 = (byte)num3;
			num3 >>= 8;
			byte b4 = _0023_003DqDHcwibtG5aC8N_0024xqlxJ9qjU9svRnEClowNfa9Z_00247SP0_003D[i];
			_0023_003DqDHcwibtG5aC8N_0024xqlxJ9qjU9svRnEClowNfa9Z_00247SP0_003D[i] = (byte)(b4 ^ b ^ (b2 + 3) ^ b3);
			b2 = b4;
		}
		return _0023_003DqDHcwibtG5aC8N_0024xqlxJ9qjU9svRnEClowNfa9Z_00247SP0_003D;
	}
}
