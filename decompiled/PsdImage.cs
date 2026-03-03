using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;

public sealed class PsdImage
{
	private enum _0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D
	{

	}

	[Serializable]
	private sealed class _003C_003Ec
	{
		public static readonly _003C_003Ec _003C_003E9 = new _003C_003Ec();

		public static Func<byte, string> _003C_003E9__12_0;

		public static Func<PsdImageResource, bool> _003C_003E9__16_0;

		internal string _0023_003DqFA_0024_0024Fp5bR3d1UiunGE_cFBndQdIHrHDWUI7_0024mCjg2bs_003D(byte _0023_003DqNg_0024ZQTUlrbTQruHWRi2guQ_003D_003D)
		{
			return _0023_003DqNg_0024ZQTUlrbTQruHWRi2guQ_003D_003D.ToString(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825794));
		}

		internal bool _0023_003DqjBV5ta5E6azLw_BY0f4xCo6sBc2mkueQaZ91IUo5Q80_003D(PsdImageResource _0023_003DqznceSvBsTEZqcLRqLYHShQ_003D_003D)
		{
			return _0023_003DqznceSvBsTEZqcLRqLYHShQ_003D_003D._0023_003DqCLOmxWwsHDR8ZKHgp19lJA_003D_003D == (_0023_003DqS18cpfWLxkGDncthIFQlOYRB4tkwahaO5hUOSCyZyfs_003D)1032;
		}
	}

	public int _0023_003DqVkzhf_YqwqbjrJAqclqEnQ_003D_003D;

	public int _0023_003DqOFH48EjaoVMXfQxwh9dbDw_003D_003D;

	public int _0023_003DqZ3XCoGw4XYJEn1llrBGFGQ_003D_003D;

	public _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D[] _0023_003DqlS1uEIBQBg2xK32ril4aAA_003D_003D;

	public _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D _0023_003DqVWPkfI5b99Q8TjXHItCO_Q_003D_003D;

	public List<PsdImageResource> _0023_003DqsmwUCSuD1Sm_0024NcONiPb3PQ_003D_003D = new List<PsdImageResource>();

	public static _0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D _0023_003Dq_0024hw45vsFwqukKzxa7ohDq0xvUe0GZiST4zGdmkiqzwY_003D(string _0023_003Dqkv04D1AmiHtKgmONOsK2BA_003D_003D)
	{
		ASCIIEncoding aSCIIEncoding = new ASCIIEncoding();
		FileStream fileStream = new FileStream(_0023_003Dqkv04D1AmiHtKgmONOsK2BA_003D_003D, FileMode.Open, FileAccess.Read);
		try
		{
			BinaryReader binaryReader = new BinaryReader(fileStream);
			try
			{
				string text = aSCIIEncoding.GetString(binaryReader.ReadBytes(4));
				ushort num = binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
				fileStream.Position += 6L;
				ushort num2 = binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
				int num3 = (int)binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
				int num4 = (int)binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
				ushort num5 = binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
				ushort num6 = binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(text == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825849));
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(num == 1);
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(num2 == 3 || num2 == 4);
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(num5 == 8);
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(num6 == 3);
				uint num7 = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
				fileStream.Position += num7;
				num7 = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
				fileStream.Position += num7;
				num7 = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
				fileStream.Position += num7;
				_0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2 = _0023_003DqIK8in_0024D51FTwNShZahzIE8Gduy5HgupOTYmavXrj7aU_003D(binaryReader, num4, num3, num2);
				byte[] array = new byte[num4 * num3 * 4];
				for (int i = 0; i < num3; i++)
				{
					for (int j = 0; j < num4; j++)
					{
						int num8 = (num3 - i - 1) * num4 + j;
						int num9 = i * num4 + j;
						byte b = _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003DqwBY3zuqGBS_i59V3Y4pLLQ_003D_003D[num8];
						byte b2 = _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003DqH2PhqGSp4dykRgVvhgMgyA_003D_003D[num8];
						byte b3 = _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003DqwGypTxOAonudO6XwVyO0ng_003D_003D[num8];
						byte b4 = _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003Dq6ht7pJTJ3wisqYRYpKQIMw_003D_003D[num8];
						b = (byte)(b + b4 - 255);
						b2 = (byte)(b2 + b4 - 255);
						b3 = (byte)(b3 + b4 - 255);
						array[4 * num9] = b;
						array[4 * num9 + 1] = b2;
						array[4 * num9 + 2] = b3;
						array[4 * num9 + 3] = b4;
					}
				}
				return new _0023_003DqZCQQHI5v1zsbOU1QX7Wmiw_003D_003D((_0023_003DqbA6Sa8L4h3TKMfLpMJe3yA_003D_003D)2, num4, num3, array);
			}
			finally
			{
				((IDisposable)binaryReader).Dispose();
			}
		}
		finally
		{
			((IDisposable)fileStream).Dispose();
		}
	}

	public static PsdImage _0023_003DqdpUvyxl_kp7W5U5lEKgb5g_003D_003D(string _0023_003Dqu8KcH8wFhCNZdafD8Bqj2w_003D_003D)
	{
		PsdImage psdImage = new PsdImage();
		ASCIIEncoding aSCIIEncoding = new ASCIIEncoding();
		UnicodeEncoding unicodeEncoding = new UnicodeEncoding(bigEndian: true, byteOrderMark: false);
		FileStream fileStream = new FileStream(_0023_003Dqu8KcH8wFhCNZdafD8Bqj2w_003D_003D, FileMode.Open, FileAccess.Read);
		try
		{
			BinaryReader binaryReader = new BinaryReader(fileStream);
			try
			{
				string text = aSCIIEncoding.GetString(binaryReader.ReadBytes(4));
				ushort num = binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
				fileStream.Position += 6L;
				ushort num2 = binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
				psdImage._0023_003DqOFH48EjaoVMXfQxwh9dbDw_003D_003D = (int)binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
				psdImage._0023_003DqVkzhf_YqwqbjrJAqclqEnQ_003D_003D = (int)binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
				ushort num3 = binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
				ushort num4 = binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(text == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825849));
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(num == 1);
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(num2 == 3 || num2 == 4);
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(num3 == 8);
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(num4 == 3);
				psdImage._0023_003DqZ3XCoGw4XYJEn1llrBGFGQ_003D_003D = num2;
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D() == 0);
				psdImage._0023_003DqsmwUCSuD1Sm_0024NcONiPb3PQ_003D_003D = _0023_003DqkdSGPbu75TCYNo8e1gVsUMGK2DDfRbkZFh8fVbbNbwc_003D(binaryReader);
				uint num5 = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
				long position = fileStream.Position + num5;
				uint num6 = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
				long num7 = fileStream.Position + (int)num6;
				short num8 = binaryReader._0023_003DqCpirCgPOSDkdFnria00c_a6mC_eVBarE09_0024vGoB1ozY_003D();
				if (num8 < 0)
				{
					num8 = Math.Abs(num8);
				}
				psdImage._0023_003DqlS1uEIBQBg2xK32ril4aAA_003D_003D = new _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D[num8];
				for (int i = 0; i < num8; i++)
				{
					_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2 = new _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D();
					_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqZ_0024nxPMGCIx7iJlR2xrLbug_003D_003D = _0023_003DqgHgMib6O7GEcXfSZTccc8g_003D_003D(binaryReader);
					ushort num9 = binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
					for (int j = 0; j < num9; j++)
					{
						_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2 = new _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D();
						_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003Dql8zXqNbRUpdu_m8Mn4E_xA_003D_003D = (_0023_003DqPTAc2gjqNBviSBBRRreSgw_003D_003D)binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
						_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003DqlYTKSpRrnQ0zty3a4vt_0024XnGibYu_0024NqaQfSM4OqEVBgc_003D = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
						if (_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003Dql8zXqNbRUpdu_m8Mn4E_xA_003D_003D == _0023_003DqPTAc2gjqNBviSBBRRreSgw_003D_003D.Red)
						{
							_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqogDQVccwzTdG_z3ByxI_rw_003D_003D = _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2;
						}
						else if (_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003Dql8zXqNbRUpdu_m8Mn4E_xA_003D_003D == _0023_003DqPTAc2gjqNBviSBBRRreSgw_003D_003D.Green)
						{
							_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003Dq4zMoDku9DTH7gklr92y2sQ_003D_003D = _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2;
						}
						else if (_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003Dql8zXqNbRUpdu_m8Mn4E_xA_003D_003D == _0023_003DqPTAc2gjqNBviSBBRRreSgw_003D_003D.Blue)
						{
							_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqT4wBn_0024du7Dot0S_0024TkYV7rg_003D_003D = _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2;
						}
						else if (_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003Dql8zXqNbRUpdu_m8Mn4E_xA_003D_003D == _0023_003DqPTAc2gjqNBviSBBRRreSgw_003D_003D.Transparent)
						{
							_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003Dq5EM4NpwZtkvLNyc8ENnXPQ_003D_003D = _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2;
						}
					}
					_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(aSCIIEncoding.GetString(binaryReader.ReadBytes(4)) == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825838));
					_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqIGYTudtfqYz5aJpGINXcJA_003D_003D = aSCIIEncoding.GetString(binaryReader.ReadBytes(4));
					_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqDJklh23e_0024TeIt3VnSwCJVA_003D_003D = binaryReader.ReadByte();
					binaryReader.ReadByte();
					byte b = binaryReader.ReadByte();
					_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqOZP5AAxlruF_00241gR1v6E1Bg_003D_003D = (b & 2) == 0;
					fileStream.Position++;
					uint num10 = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
					long num11 = fileStream.Position + (int)num10;
					uint num12 = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
					fileStream.Position += num12;
					uint num13 = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
					fileStream.Position += num13;
					byte b2 = binaryReader.ReadByte();
					_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003Dq5J8FJbnjuFVy7kM_kf0kbg_003D_003D = aSCIIEncoding.GetString(binaryReader.ReadBytes(b2));
					_0023_003DqaQ80ozKiZCl7ZpTjHIdk4h0Fr6fKNppVDhcAA0zAy0U_003D(fileStream, 1 + b2, 4);
					while (fileStream.Position < num11)
					{
						_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(aSCIIEncoding.GetString(binaryReader.ReadBytes(4)) == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825838));
						string text2 = aSCIIEncoding.GetString(binaryReader.ReadBytes(4));
						uint num14 = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
						if (text2 == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825827))
						{
							uint num15 = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
							_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003Dq5J8FJbnjuFVy7kM_kf0kbg_003D_003D = unicodeEncoding.GetString(binaryReader.ReadBytes((int)(num15 * 2)));
							_0023_003DqaQ80ozKiZCl7ZpTjHIdk4h0Fr6fKNppVDhcAA0zAy0U_003D(fileStream, (int)(4 + 2 * num15), 4);
						}
						else if (text2 == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825752))
						{
							_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqvMojmjjPjiHHP8tfP3nh7g_003D_003D = (_0023_003DqW2yH0NwHGWz1a0k4HbzZRA_003D_003D)binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
							if (num14 >= 12)
							{
								_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(aSCIIEncoding.GetString(binaryReader.ReadBytes(4)) == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825838));
								_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqIGYTudtfqYz5aJpGINXcJA_003D_003D = aSCIIEncoding.GetString(binaryReader.ReadBytes(4));
								switch (num14)
								{
								case 16u:
									fileStream.Position += 4L;
									break;
								default:
									_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(_0023_003DqwtgUTAJA_0024ki_elb0iFI_0024sw_003D_003D: false);
									break;
								case 0u:
								case 1u:
								case 2u:
								case 3u:
								case 4u:
								case 5u:
								case 6u:
								case 7u:
								case 8u:
								case 9u:
								case 10u:
								case 11u:
								case 12u:
								case 13u:
								case 14u:
								case 15u:
									break;
								}
							}
						}
						else
						{
							fileStream.Position += num14;
						}
					}
					_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(fileStream.Position == num11);
					if (num9 > 4)
					{
						throw new _0023_003DqIoOFxNm_0024B2nZsgKjnscmbA_003D_003D(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825741), _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003Dq5J8FJbnjuFVy7kM_kf0kbg_003D_003D));
					}
					if (num9 < 4)
					{
						throw new _0023_003DqIoOFxNm_0024B2nZsgKjnscmbA_003D_003D(string.Format(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825678), _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003Dq5J8FJbnjuFVy7kM_kf0kbg_003D_003D));
					}
					psdImage._0023_003DqlS1uEIBQBg2xK32ril4aAA_003D_003D[i] = _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2;
				}
				_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D[] array = psdImage._0023_003DqlS1uEIBQBg2xK32ril4aAA_003D_003D;
				foreach (_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D3 in array)
				{
					_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D[] array2 = new _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D[4] { _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D3._0023_003Dq5EM4NpwZtkvLNyc8ENnXPQ_003D_003D, _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D3._0023_003DqogDQVccwzTdG_z3ByxI_rw_003D_003D, _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D3._0023_003Dq4zMoDku9DTH7gklr92y2sQ_003D_003D, _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D3._0023_003DqT4wBn_0024du7Dot0S_0024TkYV7rg_003D_003D };
					foreach (_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D3 in array2)
					{
						_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D3._0023_003DqTWJhRdGoddGyEt1hdamkFg_003D_003D = (_0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D)binaryReader._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
						if (_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D3._0023_003DqTWJhRdGoddGyEt1hdamkFg_003D_003D == _0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D.RLE)
						{
							_0023_003DqVXSiYWs9EUzSOshLx5A9lg_003D_003D(binaryReader, _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D3._0023_003DqZ_0024nxPMGCIx7iJlR2xrLbug_003D_003D._0023_003DqY8PCFijD_0024GCXRzfjbmFFDQ_003D_003D(), 1);
						}
						_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D3._0023_003Dq3gWTyG_0024_fJuILX2NOeZNKQ_003D_003D = _0023_003Dqzs0S9tcclhyvvTFR01MkGblIYKe40hSOPWGFLf9a280_003D(binaryReader, _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D3._0023_003DqTWJhRdGoddGyEt1hdamkFg_003D_003D, _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D3._0023_003DqZ_0024nxPMGCIx7iJlR2xrLbug_003D_003D);
					}
				}
				if (fileStream.Position % 2 == 1)
				{
					fileStream.Position++;
				}
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(fileStream.Position <= num7);
				fileStream.Position = position;
				psdImage._0023_003DqVWPkfI5b99Q8TjXHItCO_Q_003D_003D = _0023_003DqIK8in_0024D51FTwNShZahzIE8Gduy5HgupOTYmavXrj7aU_003D(binaryReader, psdImage._0023_003DqVkzhf_YqwqbjrJAqclqEnQ_003D_003D, psdImage._0023_003DqOFH48EjaoVMXfQxwh9dbDw_003D_003D, psdImage._0023_003DqZ3XCoGw4XYJEn1llrBGFGQ_003D_003D);
			}
			finally
			{
				((IDisposable)binaryReader).Dispose();
			}
		}
		finally
		{
			((IDisposable)fileStream).Dispose();
		}
		Array.Reverse(psdImage._0023_003DqlS1uEIBQBg2xK32ril4aAA_003D_003D);
		return psdImage;
	}

	private static void _0023_003DqaQ80ozKiZCl7ZpTjHIdk4h0Fr6fKNppVDhcAA0zAy0U_003D(Stream _0023_003Dq0djoTZ8eSBnslnYS5UmvVg_003D_003D, int _0023_003Dqy5wFISAhk5tTQDIdDzddug_003D_003D, int _0023_003DqJCUIcRDjVxqnE85DehIP3A_003D_003D)
	{
		for (int i = _0023_003Dqy5wFISAhk5tTQDIdDzddug_003D_003D; i % _0023_003DqJCUIcRDjVxqnE85DehIP3A_003D_003D != 0; i++)
		{
			_0023_003Dq0djoTZ8eSBnslnYS5UmvVg_003D_003D.Position++;
		}
	}

	private static _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D _0023_003DqIK8in_0024D51FTwNShZahzIE8Gduy5HgupOTYmavXrj7aU_003D(BinaryReader _0023_003DqG23zn5x5QZ_rHK_H3q01tQ_003D_003D, int _0023_003DqvzH1J07ZUfI6eA_oCSZr9g_003D_003D, int _0023_003Dqpk_0024yqB_Xpz9X_UOT9_0024X5TA_003D_003D, int _0023_003DqijNnzwPUy0e5MUW4gyuSSA_003D_003D)
	{
		_0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2 = new _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D();
		_0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D _0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D2 = (_0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003Dqxxte0ZzochVEC_1JTMQiVA_003D_003D = (_0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D)_0023_003DqG23zn5x5QZ_rHK_H3q01tQ_003D_003D._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D());
		if (_0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D2 == _0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D.RLE)
		{
			_0023_003DqVXSiYWs9EUzSOshLx5A9lg_003D_003D(_0023_003DqG23zn5x5QZ_rHK_H3q01tQ_003D_003D, _0023_003Dqpk_0024yqB_Xpz9X_UOT9_0024X5TA_003D_003D, _0023_003DqijNnzwPUy0e5MUW4gyuSSA_003D_003D);
		}
		_0023_003Dq6kQBVl9ddNMI5cg_oMf9OA_003D_003D _0023_003Dqv6soc6AVRo_0024Qs56lfakvTA_003D_003D = _0023_003Dq6kQBVl9ddNMI5cg_oMf9OA_003D_003D._0023_003DqkdXHZ5dlWT1tqM_sVkdZiA_003D_003D(0, _0023_003DqvzH1J07ZUfI6eA_oCSZr9g_003D_003D, 0, _0023_003Dqpk_0024yqB_Xpz9X_UOT9_0024X5TA_003D_003D);
		_0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003DqwBY3zuqGBS_i59V3Y4pLLQ_003D_003D = _0023_003Dqzs0S9tcclhyvvTFR01MkGblIYKe40hSOPWGFLf9a280_003D(_0023_003DqG23zn5x5QZ_rHK_H3q01tQ_003D_003D, _0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D2, _0023_003Dqv6soc6AVRo_0024Qs56lfakvTA_003D_003D);
		_0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003DqH2PhqGSp4dykRgVvhgMgyA_003D_003D = _0023_003Dqzs0S9tcclhyvvTFR01MkGblIYKe40hSOPWGFLf9a280_003D(_0023_003DqG23zn5x5QZ_rHK_H3q01tQ_003D_003D, _0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D2, _0023_003Dqv6soc6AVRo_0024Qs56lfakvTA_003D_003D);
		_0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003DqwGypTxOAonudO6XwVyO0ng_003D_003D = _0023_003Dqzs0S9tcclhyvvTFR01MkGblIYKe40hSOPWGFLf9a280_003D(_0023_003DqG23zn5x5QZ_rHK_H3q01tQ_003D_003D, _0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D2, _0023_003Dqv6soc6AVRo_0024Qs56lfakvTA_003D_003D);
		if (_0023_003DqijNnzwPUy0e5MUW4gyuSSA_003D_003D > 3)
		{
			_0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003Dq6ht7pJTJ3wisqYRYpKQIMw_003D_003D = _0023_003Dqzs0S9tcclhyvvTFR01MkGblIYKe40hSOPWGFLf9a280_003D(_0023_003DqG23zn5x5QZ_rHK_H3q01tQ_003D_003D, _0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D2, _0023_003Dqv6soc6AVRo_0024Qs56lfakvTA_003D_003D);
		}
		else
		{
			_0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003Dq6ht7pJTJ3wisqYRYpKQIMw_003D_003D = new byte[_0023_003DqvzH1J07ZUfI6eA_oCSZr9g_003D_003D * _0023_003Dqpk_0024yqB_Xpz9X_UOT9_0024X5TA_003D_003D];
			for (int i = 0; i < _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003Dq6ht7pJTJ3wisqYRYpKQIMw_003D_003D.Length; i++)
			{
				_0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2._0023_003Dq6ht7pJTJ3wisqYRYpKQIMw_003D_003D[i] = byte.MaxValue;
			}
		}
		return _0023_003Dq4oVwaKwWILgorMfpsC3AGosw35tmMyz61JoVhWSMXtU_003D2;
	}

	private static void _0023_003DqVXSiYWs9EUzSOshLx5A9lg_003D_003D(BinaryReader _0023_003Dqc4i5Q6_vsJQygVKdvrc1NA_003D_003D, int _0023_003Dq43NiY73ynylUSoRLKLObhg_003D_003D, int _0023_003DqM7j44dVrOTj8Ls0tcIJKUA_003D_003D)
	{
		_0023_003Dqc4i5Q6_vsJQygVKdvrc1NA_003D_003D.BaseStream.Position += _0023_003Dq43NiY73ynylUSoRLKLObhg_003D_003D * _0023_003DqM7j44dVrOTj8Ls0tcIJKUA_003D_003D * 2;
	}

	private static byte[] _0023_003Dqzs0S9tcclhyvvTFR01MkGblIYKe40hSOPWGFLf9a280_003D(BinaryReader _0023_003DqpLM4QbExSlSmxprZ2D0dXw_003D_003D, _0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D _0023_003Dq9IkzPx9giVJn2Ih5mHwViQ_003D_003D, _0023_003Dq6kQBVl9ddNMI5cg_oMf9OA_003D_003D _0023_003Dqv6soc6AVRo_0024Qs56lfakvTA_003D_003D)
	{
		switch (_0023_003Dq9IkzPx9giVJn2Ih5mHwViQ_003D_003D)
		{
		case _0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D.Raw:
			return _0023_003DqpLM4QbExSlSmxprZ2D0dXw_003D_003D.ReadBytes(_0023_003Dqv6soc6AVRo_0024Qs56lfakvTA_003D_003D._0023_003DqsVshXVR3wk96OFGoBycHcA_003D_003D() * _0023_003Dqv6soc6AVRo_0024Qs56lfakvTA_003D_003D._0023_003DqY8PCFijD_0024GCXRzfjbmFFDQ_003D_003D());
		case _0023_003DqfEQRsTTdJ7wwTAY2KgYW_yWzOVm5q3_0024Segc6V_0024yokrI_003D.RLE:
			return _0023_003Dq0fE_16tSJVGqtN2CE8HG3w_003D_003D(_0023_003DqpLM4QbExSlSmxprZ2D0dXw_003D_003D, _0023_003Dqv6soc6AVRo_0024Qs56lfakvTA_003D_003D._0023_003DqsVshXVR3wk96OFGoBycHcA_003D_003D() * _0023_003Dqv6soc6AVRo_0024Qs56lfakvTA_003D_003D._0023_003DqY8PCFijD_0024GCXRzfjbmFFDQ_003D_003D());
		default:
			_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(_0023_003DqwtgUTAJA_0024ki_elb0iFI_0024sw_003D_003D: false);
			return new byte[0];
		}
	}

	public void _0023_003DqPBNd6RrxOPsqki7MV0K85Q_003D_003D(bool _0023_003Dq2_T3iPN6NL4ZudzlWCVquMA_0024IqMe9FAFHEapgHA123Q_003D)
	{
		Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825621) + _0023_003DqVkzhf_YqwqbjrJAqclqEnQ_003D_003D);
		Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825607) + _0023_003DqOFH48EjaoVMXfQxwh9dbDw_003D_003D);
		Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825656) + ((_0023_003DqZ3XCoGw4XYJEn1llrBGFGQ_003D_003D == 3) ? _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825566) : _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825641)));
		Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825556) + _0023_003DqlS1uEIBQBg2xK32ril4aAA_003D_003D.Length);
		_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D[] array = _0023_003DqlS1uEIBQBg2xK32ril4aAA_003D_003D;
		foreach (_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2 in array)
		{
			Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825541), _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003Dq5J8FJbnjuFVy7kM_kf0kbg_003D_003D);
			Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825585), _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqZ_0024nxPMGCIx7iJlR2xrLbug_003D_003D);
			Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825499), _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqIGYTudtfqYz5aJpGINXcJA_003D_003D);
			Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825473), _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqDJklh23e_0024TeIt3VnSwCJVA_003D_003D);
			Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825514), _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqOZP5AAxlruF_00241gR1v6E1Bg_003D_003D);
			if (!_0023_003Dq2_T3iPN6NL4ZudzlWCVquMA_0024IqMe9FAFHEapgHA123Q_003D)
			{
				continue;
			}
			_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D[] array2 = new _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D[4] { _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqogDQVccwzTdG_z3ByxI_rw_003D_003D, _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003Dq4zMoDku9DTH7gklr92y2sQ_003D_003D, _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003DqT4wBn_0024du7Dot0S_0024TkYV7rg_003D_003D, _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D2._0023_003Dq5EM4NpwZtkvLNyc8ENnXPQ_003D_003D };
			foreach (_0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2 in array2)
			{
				Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825427), _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003Dql8zXqNbRUpdu_m8Mn4E_xA_003D_003D);
				Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825469), _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003DqTWJhRdGoddGyEt1hdamkFg_003D_003D);
				Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825440), _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003DqlYTKSpRrnQ0zty3a4vt_0024XnGibYu_0024NqaQfSM4OqEVBgc_003D);
				Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825345), _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003Dq3gWTyG_0024_fJuILX2NOeZNKQ_003D_003D.Length);
				Console.WriteLine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825381), string.Join(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850848026), _0023_003DqBaP7_OLKHI5Z4vm0iHhvqQ_003D_003D2._0023_003Dq3gWTyG_0024_fJuILX2NOeZNKQ_003D_003D.Select((byte _0023_003DqNg_0024ZQTUlrbTQruHWRi2guQ_003D_003D) => _0023_003DqNg_0024ZQTUlrbTQruHWRi2guQ_003D_003D.ToString(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825794)))));
			}
		}
	}

	public void _0023_003Dqq5_qZ3C4A_TMJ6H4pJ2XFA_003D_003D(_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D _0023_003Dq1Bmi2H_hPJ9Ge0G_WtY3Eg_003D_003D, string _0023_003DqUIUgollKVkcr22eryyGN9Q_003D_003D)
	{
		_0023_003Dq9HVAZnMzcX_g07dd1oLGHJ5qvrMTEk0ftOUGcHJZmTk_003D(new _0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D[1] { _0023_003Dq1Bmi2H_hPJ9Ge0G_WtY3Eg_003D_003D }, _0023_003DqUIUgollKVkcr22eryyGN9Q_003D_003D);
	}

	public void _0023_003Dq9HVAZnMzcX_g07dd1oLGHJ5qvrMTEk0ftOUGcHJZmTk_003D(IEnumerable<_0023_003DqaSZTFP2yo0YmKNl511oAPQ_003D_003D> _0023_003Dqknii0J5YNu725rqVPaUJIQ_003D_003D, string _0023_003DqG07N8lwQibSPScrAiTnZ9w_003D_003D)
	{
		throw new NotImplementedException();
	}

	public List<PsdGuide> _0023_003DqkrLYs70_Gx54QK4Rw8Cf0w_003D_003D()
	{
		return _0023_003DqhdYSZG9OA7POAZzWWmcyGw_003D_003D(_0023_003DqsmwUCSuD1Sm_0024NcONiPb3PQ_003D_003D);
	}

	private static List<PsdGuide> _0023_003DqhdYSZG9OA7POAZzWWmcyGw_003D_003D(List<PsdImageResource> _0023_003DqVym8sjziSoiUOmBMfZvn8A_003D_003D)
	{
		List<PsdGuide> list = new List<PsdGuide>();
		PsdImageResource psdImageResource = _0023_003DqVym8sjziSoiUOmBMfZvn8A_003D_003D.FirstOrDefault(_003C_003Ec._003C_003E9._0023_003DqjBV5ta5E6azLw_BY0f4xCo6sBc2mkueQaZ91IUo5Q80_003D);
		if (psdImageResource != null)
		{
			MemoryStream memoryStream = new MemoryStream(psdImageResource._0023_003DqGQEvfezTIyXBr1UC_w5yYQ_003D_003D);
			try
			{
				BinaryReader binaryReader = new BinaryReader(memoryStream);
				try
				{
					memoryStream.Position += 12L;
					uint num = binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
					_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(psdImageResource._0023_003DqGQEvfezTIyXBr1UC_w5yYQ_003D_003D.Length == 16 + num * 5);
					for (int i = 0; i < num; i++)
					{
						int _0023_003Dq4Rae_Y7U52uCW9suqn4tzA_003D_003D = binaryReader._0023_003Dq5IGOdhGxNO75RcnZ6OF8uAHBB8e3KMwpHEHns1ToDH8_003D();
						_0023_003DqouWK0I4ZSf7k3HGqYfL2pTtU4GDIQOxJgHcOnfosWqg_003D _0023_003DqW8DTszdWFxZnijjKbJzVkQ_003D_003D = (_0023_003DqouWK0I4ZSf7k3HGqYfL2pTtU4GDIQOxJgHcOnfosWqg_003D)binaryReader.ReadByte();
						list.Add(new PsdGuide
						{
							_0023_003Dq4Rae_Y7U52uCW9suqn4tzA_003D_003D = _0023_003Dq4Rae_Y7U52uCW9suqn4tzA_003D_003D,
							_0023_003DqW8DTszdWFxZnijjKbJzVkQ_003D_003D = _0023_003DqW8DTszdWFxZnijjKbJzVkQ_003D_003D
						});
					}
					return list;
				}
				finally
				{
					((IDisposable)binaryReader).Dispose();
				}
			}
			finally
			{
				((IDisposable)memoryStream).Dispose();
			}
		}
		return list;
	}

	[DebuggerStepThrough]
	private static void _0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(bool _0023_003DqwtgUTAJA_0024ki_elb0iFI_0024sw_003D_003D)
	{
		if (!_0023_003DqwtgUTAJA_0024ki_elb0iFI_0024sw_003D_003D)
		{
			throw new _0023_003DqIoOFxNm_0024B2nZsgKjnscmbA_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825295));
		}
	}

	private static _0023_003Dq6kQBVl9ddNMI5cg_oMf9OA_003D_003D _0023_003DqgHgMib6O7GEcXfSZTccc8g_003D_003D(BinaryReader _0023_003DqPKI0uQIypb3OL99GM86jxQ_003D_003D)
	{
		_0023_003Dq6kQBVl9ddNMI5cg_oMf9OA_003D_003D result = default(_0023_003Dq6kQBVl9ddNMI5cg_oMf9OA_003D_003D);
		result._0023_003Dqf4_0024_0024489PTAuWHghez25s2A_003D_003D = _0023_003DqPKI0uQIypb3OL99GM86jxQ_003D_003D._0023_003Dq5IGOdhGxNO75RcnZ6OF8uAHBB8e3KMwpHEHns1ToDH8_003D();
		result._0023_003DqFAr8MqhJ4sDcJuOulKsstQ_003D_003D = _0023_003DqPKI0uQIypb3OL99GM86jxQ_003D_003D._0023_003Dq5IGOdhGxNO75RcnZ6OF8uAHBB8e3KMwpHEHns1ToDH8_003D();
		result._0023_003Dq5Ttufx2gHHi0rulmYSn4zg_003D_003D = _0023_003DqPKI0uQIypb3OL99GM86jxQ_003D_003D._0023_003Dq5IGOdhGxNO75RcnZ6OF8uAHBB8e3KMwpHEHns1ToDH8_003D();
		result._0023_003DqX4XxCzxRBtT2dsyYl6cODQ_003D_003D = _0023_003DqPKI0uQIypb3OL99GM86jxQ_003D_003D._0023_003Dq5IGOdhGxNO75RcnZ6OF8uAHBB8e3KMwpHEHns1ToDH8_003D();
		return result;
	}

	private static byte[] _0023_003Dq0fE_16tSJVGqtN2CE8HG3w_003D_003D(BinaryReader _0023_003DqR8ubG8VkuvaPTsuJ2Yg1wg_003D_003D, int _0023_003DqD5AaaFByAYcf3RLxeaERiA_003D_003D)
	{
		List<byte> list = new List<byte>();
		_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D _0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D = (_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D)0;
		int num = 0;
		int num2 = 0;
		while (list.Count < _0023_003DqD5AaaFByAYcf3RLxeaERiA_003D_003D)
		{
			byte b = _0023_003DqR8ubG8VkuvaPTsuJ2Yg1wg_003D_003D.ReadByte();
			switch (_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D)
			{
			case (_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D)0:
			{
				sbyte b2 = (sbyte)b;
				if (b2 != sbyte.MinValue)
				{
					if (b2 >= 0)
					{
						_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D = (_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D)1;
						num = 1 + b2;
					}
					else
					{
						_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D = (_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D)2;
						num2 = 1 - b2;
					}
				}
				break;
			}
			case (_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D)1:
				list.Add(b);
				num--;
				if (num == 0)
				{
					_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D = (_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D)0;
				}
				break;
			case (_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D)2:
			{
				for (int i = 0; i < num2; i++)
				{
					list.Add(b);
				}
				num2 = 0;
				_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D = (_0023_003Dq2sWloVP7YlarNYWWECoIAixaOsL3QW2Doi9Prk1XdDU_003D)0;
				break;
			}
			}
		}
		_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(list.Count == _0023_003DqD5AaaFByAYcf3RLxeaERiA_003D_003D);
		return list.ToArray();
	}

	private static List<PsdImageResource> _0023_003DqkdSGPbu75TCYNo8e1gVsUMGK2DDfRbkZFh8fVbbNbwc_003D(BinaryReader _0023_003DqUWr0kyzM_T4L8bNTsl75AA_003D_003D)
	{
		Stream baseStream = _0023_003DqUWr0kyzM_T4L8bNTsl75AA_003D_003D.BaseStream;
		List<PsdImageResource> list = new List<PsdImageResource>();
		uint num = _0023_003DqUWr0kyzM_T4L8bNTsl75AA_003D_003D._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
		long num2 = baseStream.Position + num;
		while (baseStream.Position < num2)
		{
			_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(Encoding.ASCII.GetString(_0023_003DqUWr0kyzM_T4L8bNTsl75AA_003D_003D.ReadBytes(4)) == _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825838));
			_0023_003DqS18cpfWLxkGDncthIFQlOYRB4tkwahaO5hUOSCyZyfs_003D _0023_003DqCLOmxWwsHDR8ZKHgp19lJA_003D_003D = (_0023_003DqS18cpfWLxkGDncthIFQlOYRB4tkwahaO5hUOSCyZyfs_003D)_0023_003DqUWr0kyzM_T4L8bNTsl75AA_003D_003D._0023_003DquRu9PB8ycGcKzlGwuTQZWgJY_3WRFCEHM77fYMbnRO4_003D();
			byte b = _0023_003DqUWr0kyzM_T4L8bNTsl75AA_003D_003D.ReadByte();
			_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(b == 0);
			string _0023_003Dqi8cAZfDACAsxj9ZFyr_00241qw_003D_003D = Encoding.ASCII.GetString(_0023_003DqUWr0kyzM_T4L8bNTsl75AA_003D_003D.ReadBytes(b));
			if (baseStream.Position % 2 == 1)
			{
				baseStream.Position++;
			}
			uint count = _0023_003DqUWr0kyzM_T4L8bNTsl75AA_003D_003D._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D();
			byte[] _0023_003DqGQEvfezTIyXBr1UC_w5yYQ_003D_003D = _0023_003DqUWr0kyzM_T4L8bNTsl75AA_003D_003D.ReadBytes((int)count);
			if (baseStream.Position % 2 == 1)
			{
				baseStream.Position++;
			}
			list.Add(new PsdImageResource
			{
				_0023_003DqCLOmxWwsHDR8ZKHgp19lJA_003D_003D = _0023_003DqCLOmxWwsHDR8ZKHgp19lJA_003D_003D,
				_0023_003Dqi8cAZfDACAsxj9ZFyr_00241qw_003D_003D = _0023_003Dqi8cAZfDACAsxj9ZFyr_00241qw_003D_003D,
				_0023_003DqGQEvfezTIyXBr1UC_w5yYQ_003D_003D = _0023_003DqGQEvfezTIyXBr1UC_w5yYQ_003D_003D
			});
		}
		_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(baseStream.Position == num2);
		return list;
	}

	public static List<PsdGuide> _0023_003DqCyH1OLmi6H4IHoE8ZIwis6r6M6iFioqClwVl8YN7PGw_003D(string _0023_003DqaFmBj00OgjPg_0024T59XpKBFA_003D_003D)
	{
		FileStream fileStream = new FileStream(_0023_003DqaFmBj00OgjPg_0024T59XpKBFA_003D_003D, FileMode.Open, FileAccess.Read);
		try
		{
			BinaryReader binaryReader = new BinaryReader(fileStream);
			try
			{
				fileStream.Position += 26L;
				_0023_003DquyZL9B27Ji_0024vGjqMkyUI0A_003D_003D(binaryReader._0023_003DqUqwbATnWxf2Fc7slU88gzzIuA7AxpEkN_lfIviR1lkQ_003D() == 0);
				return _0023_003DqhdYSZG9OA7POAZzWWmcyGw_003D_003D(_0023_003DqkdSGPbu75TCYNo8e1gVsUMGK2DDfRbkZFh8fVbbNbwc_003D(binaryReader));
			}
			finally
			{
				((IDisposable)binaryReader).Dispose();
			}
		}
		finally
		{
			((IDisposable)fileStream).Dispose();
		}
	}
}
