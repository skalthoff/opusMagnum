using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

public sealed class HttpManager
{
	private sealed class _0023_003Dq0n0364sXFkQ33n2rTBHc8GDCJ3_0024Rrtk1GgPUdgpbyHE_003D
	{
		public Dictionary<string, string> _0023_003DqRxglZ6txf4olJsTbkX8cLw_003D_003D;

		public string _0023_003Dq3Z1_00247ytn_0024ePpK03KWdnhng_003D_003D;

		public HttpManager _0023_003DqMYigLM9dZ_apUqt0Rt2Kxg_003D_003D;

		internal byte[] _0023_003Dq7NSnFxGhm7mOojYF7N3guDXsIl6gpEzAXcGA4xS_11I_003D()
		{
			string text = string.Join(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842802), _0023_003DqRxglZ6txf4olJsTbkX8cLw_003D_003D.Select(_003C_003Ec._003C_003E9._0023_003Dq0Mv5boYZnJec6gyXstUsDKUG_gZtEYCTooxl2wp39fU_003D).ToArray());
			WebRequest webRequest = WebRequest.Create(_0023_003Dq3Z1_00247ytn_0024ePpK03KWdnhng_003D_003D);
			webRequest.Method = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842780);
			webRequest.ContentType = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842794);
			webRequest.ContentLength = text.Length;
			StreamWriter streamWriter = new StreamWriter(webRequest.GetRequestStream());
			try
			{
				streamWriter.Write(text);
			}
			finally
			{
				((IDisposable)streamWriter).Dispose();
			}
			return _0023_003DqMYigLM9dZ_apUqt0Rt2Kxg_003D_003D._0023_003Dq_0024NnQGkMTzwI_0024_0024nDgIPtiGQ_003D_003D(webRequest);
		}
	}

	private sealed class _0023_003DqFkjjJV2B0qv83LzETHARNkRMSCM1_X1gcMCw8bifxuU_003D
	{
		public string _0023_003DqkACuMWRzjiOCKJs0uqeo_Q_003D_003D;

		public byte[] _0023_003DqcFMDRsnrB4wtL_0024SiDaVaCw_003D_003D;

		public HttpManager _0023_003Dqa_xgcbzFqru8ZAvKYKjmTw_003D_003D;

		internal byte[] _0023_003Dqmjw5kiEjcrw6GpPNoWQSZ74NckatzYmUYH_00247RAfnigI_003D()
		{
			WebRequest webRequest = WebRequest.Create(_0023_003DqkACuMWRzjiOCKJs0uqeo_Q_003D_003D);
			webRequest.Method = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842780);
			webRequest.ContentType = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842769);
			webRequest.ContentLength = _0023_003DqcFMDRsnrB4wtL_0024SiDaVaCw_003D_003D.Length;
			using (Stream stream = webRequest.GetRequestStream())
			{
				stream.Write(_0023_003DqcFMDRsnrB4wtL_0024SiDaVaCw_003D_003D, 0, _0023_003DqcFMDRsnrB4wtL_0024SiDaVaCw_003D_003D.Length);
			}
			return _0023_003Dqa_xgcbzFqru8ZAvKYKjmTw_003D_003D._0023_003Dq_0024NnQGkMTzwI_0024_0024nDgIPtiGQ_003D_003D(webRequest);
		}
	}

	private sealed class _0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D
	{
		public _0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D _0023_003DqBMdUHVVlofvGmcLTcrwbcw_003D_003D;

		public Func<byte[]> _0023_003DqgKdCVTkpyDOSAtfChoosiQZnfqbnKrczFrBD4RyaOBE_003D;

		internal void _0023_003DqOOB3TxuQkqMWwto2Duka7F2CgiaNQSgzsFSn_jac7L0_003D()
		{
			try
			{
				_0023_003DqBMdUHVVlofvGmcLTcrwbcw_003D_003D._0023_003DqIlyIdRaFzAKG1lS5OKMapw_003D_003D = _0023_003DqgKdCVTkpyDOSAtfChoosiQZnfqbnKrczFrBD4RyaOBE_003D();
			}
			catch
			{
			}
		}
	}

	private sealed class _0023_003DqUoFG5uf79TotS_0024A6CGXMpxg_0024HIMlBh_00241mKtav_d9Plk_003D
	{
		public string _0023_003Dqt1I_0024TQLMqmPHIfHlbdaXBQ_003D_003D;

		public HttpManager _0023_003DqlT8RTEGjHf6tGH8KwEnT1g_003D_003D;

		internal byte[] _0023_003DqmNUIAhgPpzwecdNj1jqm7w_003D_003D()
		{
			WebRequest webRequest = WebRequest.Create(_0023_003Dqt1I_0024TQLMqmPHIfHlbdaXBQ_003D_003D);
			webRequest.Method = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842854);
			return _0023_003DqlT8RTEGjHf6tGH8KwEnT1g_003D_003D._0023_003Dq_0024NnQGkMTzwI_0024_0024nDgIPtiGQ_003D_003D(webRequest);
		}
	}

	private sealed class _0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D
	{
		public Task _0023_003DqZcyvfaQjtczAfgFMR8AGkw_003D_003D;

		public Action<byte[]> _0023_003Dqf1DVo6_002454t6RJCELn4w8MA_003D_003D;

		public Action _0023_003DqIbq7vmhM6HMZ2ISkeGLC9Q_003D_003D;

		public Maybe<byte[]> _0023_003DqIlyIdRaFzAKG1lS5OKMapw_003D_003D = _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D;
	}

	[Serializable]
	private sealed class _003C_003Ec
	{
		public static readonly _003C_003Ec _003C_003E9 = new _003C_003Ec();

		public static Func<KeyValuePair<string, string>, string> _003C_003E9__3_1;

		internal string _0023_003Dq0Mv5boYZnJec6gyXstUsDKUG_gZtEYCTooxl2wp39fU_003D(KeyValuePair<string, string> _0023_003DqInJjsdLxqf6PZp7tU_00247A0w_003D_003D)
		{
			return _0023_003DqJBeilngA8kvUCvDdQQLcUeLkscEP0xplp3_0024IWEXu6AE_003D(_0023_003DqInJjsdLxqf6PZp7tU_00247A0w_003D_003D.Key) + _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842862) + _0023_003DqJBeilngA8kvUCvDdQQLcUeLkscEP0xplp3_0024IWEXu6AE_003D(_0023_003DqInJjsdLxqf6PZp7tU_00247A0w_003D_003D.Value);
		}
	}

	private List<_0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D> _0023_003Dqdu4MCpMzYpBSszOMSHyLvpRZf8fXeSYEYeoLtuGdwW8_003D = new List<_0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D>();

	public void _0023_003DqVxvgD1zc2fzUYIxILr8OxQ_003D_003D(string _0023_003DqUVJh05vvOwA89g1rTfyZuQ_003D_003D, Action<byte[]> _0023_003DqQUZj1xY9elkF3uyzk4NGMA_003D_003D, Action _0023_003DqUmFUGJi6PuxsezMyW4R10Q_003D_003D)
	{
		_0023_003DqUoFG5uf79TotS_0024A6CGXMpxg_0024HIMlBh_00241mKtav_d9Plk_003D _0023_003DqUoFG5uf79TotS_0024A6CGXMpxg_0024HIMlBh_00241mKtav_d9Plk_003D = new _0023_003DqUoFG5uf79TotS_0024A6CGXMpxg_0024HIMlBh_00241mKtav_d9Plk_003D();
		_0023_003DqUoFG5uf79TotS_0024A6CGXMpxg_0024HIMlBh_00241mKtav_d9Plk_003D._0023_003Dqt1I_0024TQLMqmPHIfHlbdaXBQ_003D_003D = _0023_003DqUVJh05vvOwA89g1rTfyZuQ_003D_003D;
		_0023_003DqUoFG5uf79TotS_0024A6CGXMpxg_0024HIMlBh_00241mKtav_d9Plk_003D._0023_003DqlT8RTEGjHf6tGH8KwEnT1g_003D_003D = this;
		_0023_003Dq5F3FS5eWFvjGh0pztlaTAUVMS807_spb8ldLOWtdXZc_003D(_0023_003DqQUZj1xY9elkF3uyzk4NGMA_003D_003D, _0023_003DqUmFUGJi6PuxsezMyW4R10Q_003D_003D, _0023_003DqUoFG5uf79TotS_0024A6CGXMpxg_0024HIMlBh_00241mKtav_d9Plk_003D._0023_003DqmNUIAhgPpzwecdNj1jqm7w_003D_003D);
	}

	public void _0023_003Dq5c1HY1KQwZf_s2hPgGn_00244g_003D_003D(string _0023_003Dq4vOaCxXCMAoF0QwyDWY2Zg_003D_003D, byte[] _0023_003DqtuUDbQeswUVhrut_brqw2g_003D_003D, Action<byte[]> _0023_003DqQEwHDIcM8hvWDqMA_0024fe2Zw_003D_003D, Action _0023_003DqlsY0sDmQuaN_7Sj8_vRyVA_003D_003D)
	{
		_0023_003DqFkjjJV2B0qv83LzETHARNkRMSCM1_X1gcMCw8bifxuU_003D CS_0024_003C_003E8__locals8 = new _0023_003DqFkjjJV2B0qv83LzETHARNkRMSCM1_X1gcMCw8bifxuU_003D();
		CS_0024_003C_003E8__locals8._0023_003DqkACuMWRzjiOCKJs0uqeo_Q_003D_003D = _0023_003Dq4vOaCxXCMAoF0QwyDWY2Zg_003D_003D;
		CS_0024_003C_003E8__locals8._0023_003DqcFMDRsnrB4wtL_0024SiDaVaCw_003D_003D = _0023_003DqtuUDbQeswUVhrut_brqw2g_003D_003D;
		CS_0024_003C_003E8__locals8._0023_003Dqa_xgcbzFqru8ZAvKYKjmTw_003D_003D = this;
		_0023_003Dq5F3FS5eWFvjGh0pztlaTAUVMS807_spb8ldLOWtdXZc_003D(_0023_003DqQEwHDIcM8hvWDqMA_0024fe2Zw_003D_003D, _0023_003DqlsY0sDmQuaN_7Sj8_vRyVA_003D_003D, delegate
		{
			WebRequest webRequest = WebRequest.Create(CS_0024_003C_003E8__locals8._0023_003DqkACuMWRzjiOCKJs0uqeo_Q_003D_003D);
			webRequest.Method = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842780);
			webRequest.ContentType = _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850842769);
			webRequest.ContentLength = CS_0024_003C_003E8__locals8._0023_003DqcFMDRsnrB4wtL_0024SiDaVaCw_003D_003D.Length;
			using (Stream stream = webRequest.GetRequestStream())
			{
				stream.Write(CS_0024_003C_003E8__locals8._0023_003DqcFMDRsnrB4wtL_0024SiDaVaCw_003D_003D, 0, CS_0024_003C_003E8__locals8._0023_003DqcFMDRsnrB4wtL_0024SiDaVaCw_003D_003D.Length);
			}
			return CS_0024_003C_003E8__locals8._0023_003Dqa_xgcbzFqru8ZAvKYKjmTw_003D_003D._0023_003Dq_0024NnQGkMTzwI_0024_0024nDgIPtiGQ_003D_003D(webRequest);
		});
	}

	public void _0023_003DqSwSn_0024phqr8T4YqiCQYUFvA_003D_003D(string _0023_003Dq8KmncGx3OQjzxb_0024XEJUu3Q_003D_003D, Dictionary<string, string> _0023_003DqMDHO9a27CG00S0lx8N6IOw_003D_003D, Action<byte[]> _0023_003DqFG36h4pBP2vxAkhs86nRNA_003D_003D, Action _0023_003Dq3jiNzwfHubkiRLOoVnpizQ_003D_003D)
	{
		_0023_003Dq0n0364sXFkQ33n2rTBHc8GDCJ3_0024Rrtk1GgPUdgpbyHE_003D _0023_003Dq0n0364sXFkQ33n2rTBHc8GDCJ3_0024Rrtk1GgPUdgpbyHE_003D = new _0023_003Dq0n0364sXFkQ33n2rTBHc8GDCJ3_0024Rrtk1GgPUdgpbyHE_003D();
		_0023_003Dq0n0364sXFkQ33n2rTBHc8GDCJ3_0024Rrtk1GgPUdgpbyHE_003D._0023_003DqRxglZ6txf4olJsTbkX8cLw_003D_003D = _0023_003DqMDHO9a27CG00S0lx8N6IOw_003D_003D;
		_0023_003Dq0n0364sXFkQ33n2rTBHc8GDCJ3_0024Rrtk1GgPUdgpbyHE_003D._0023_003Dq3Z1_00247ytn_0024ePpK03KWdnhng_003D_003D = _0023_003Dq8KmncGx3OQjzxb_0024XEJUu3Q_003D_003D;
		_0023_003Dq0n0364sXFkQ33n2rTBHc8GDCJ3_0024Rrtk1GgPUdgpbyHE_003D._0023_003DqMYigLM9dZ_apUqt0Rt2Kxg_003D_003D = this;
		_0023_003Dq5F3FS5eWFvjGh0pztlaTAUVMS807_spb8ldLOWtdXZc_003D(_0023_003DqFG36h4pBP2vxAkhs86nRNA_003D_003D, _0023_003Dq3jiNzwfHubkiRLOoVnpizQ_003D_003D, _0023_003Dq0n0364sXFkQ33n2rTBHc8GDCJ3_0024Rrtk1GgPUdgpbyHE_003D._0023_003Dq7NSnFxGhm7mOojYF7N3guDXsIl6gpEzAXcGA4xS_11I_003D);
	}

	private byte[] _0023_003Dq_0024NnQGkMTzwI_0024_0024nDgIPtiGQ_003D_003D(WebRequest _0023_003DqCDQxcqGpXhLul2SfVFatfw_003D_003D)
	{
		using WebResponse webResponse = _0023_003DqCDQxcqGpXhLul2SfVFatfw_003D_003D.GetResponse();
		byte[] array = new byte[webResponse.ContentLength];
		using (Stream stream = webResponse.GetResponseStream())
		{
			for (int i = 0; i < array.Length; i += stream.Read(array, i, array.Length - i))
			{
			}
		}
		return array;
	}

	private void _0023_003Dq5F3FS5eWFvjGh0pztlaTAUVMS807_spb8ldLOWtdXZc_003D(Action<byte[]> _0023_003DquJ_0024SfZOzFtCshViyGZzIIg_003D_003D, Action _0023_003DqkiMnsu5lZ0VzHgZyYAPy4A_003D_003D, Func<byte[]> _0023_003DqCNGmEi_0024mNBtn5W8I61VJrfxP17PWGDPCdkETD7yOVjk_003D)
	{
		_0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D _0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D = new _0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D();
		_0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D._0023_003DqgKdCVTkpyDOSAtfChoosiQZnfqbnKrczFrBD4RyaOBE_003D = _0023_003DqCNGmEi_0024mNBtn5W8I61VJrfxP17PWGDPCdkETD7yOVjk_003D;
		_0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D._0023_003DqBMdUHVVlofvGmcLTcrwbcw_003D_003D = new _0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D();
		_0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D._0023_003DqBMdUHVVlofvGmcLTcrwbcw_003D_003D._0023_003Dqf1DVo6_002454t6RJCELn4w8MA_003D_003D = _0023_003DquJ_0024SfZOzFtCshViyGZzIIg_003D_003D;
		_0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D._0023_003DqBMdUHVVlofvGmcLTcrwbcw_003D_003D._0023_003DqIbq7vmhM6HMZ2ISkeGLC9Q_003D_003D = _0023_003DqkiMnsu5lZ0VzHgZyYAPy4A_003D_003D;
		_0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D._0023_003DqBMdUHVVlofvGmcLTcrwbcw_003D_003D._0023_003DqZcyvfaQjtczAfgFMR8AGkw_003D_003D = Task.Run((Action)_0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D._0023_003DqOOB3TxuQkqMWwto2Duka7F2CgiaNQSgzsFSn_jac7L0_003D);
		_0023_003Dqdu4MCpMzYpBSszOMSHyLvpRZf8fXeSYEYeoLtuGdwW8_003D.Add(_0023_003DqM_0024emIW9xyae2tTCXeogEwlt_qZlwffwhV4IgJGiNE4w_003D._0023_003DqBMdUHVVlofvGmcLTcrwbcw_003D_003D);
	}

	public void _0023_003DqP3MkGqcO6lmcxop5FMGJEg_003D_003D()
	{
		_0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D[] array = _0023_003Dqdu4MCpMzYpBSszOMSHyLvpRZf8fXeSYEYeoLtuGdwW8_003D.ToArray();
		foreach (_0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D _0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D in array)
		{
			if (_0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D._0023_003DqZcyvfaQjtczAfgFMR8AGkw_003D_003D.IsCompleted)
			{
				if (_0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D._0023_003DqIlyIdRaFzAKG1lS5OKMapw_003D_003D._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
				{
					_0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D._0023_003Dqf1DVo6_002454t6RJCELn4w8MA_003D_003D(_0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D._0023_003DqIlyIdRaFzAKG1lS5OKMapw_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D());
				}
				else
				{
					_0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D._0023_003DqIbq7vmhM6HMZ2ISkeGLC9Q_003D_003D();
				}
				_0023_003Dqdu4MCpMzYpBSszOMSHyLvpRZf8fXeSYEYeoLtuGdwW8_003D.Remove(_0023_003DqWUc0ekKjlt7t21u4UCRsKw_003D_003D);
			}
		}
	}

	public static string _0023_003DqJBeilngA8kvUCvDdQQLcUeLkscEP0xplp3_0024IWEXu6AE_003D(string _0023_003Dq3hz6EOYnZ84QLfCxgIUrVQ_003D_003D)
	{
		StringBuilder stringBuilder = new StringBuilder();
		for (int i = 0; i < _0023_003Dq3hz6EOYnZ84QLfCxgIUrVQ_003D_003D.Length; i += 30000)
		{
			int length = Math.Min(30000, _0023_003Dq3hz6EOYnZ84QLfCxgIUrVQ_003D_003D.Length - i);
			stringBuilder.Append(Uri.EscapeDataString(_0023_003Dq3hz6EOYnZ84QLfCxgIUrVQ_003D_003D.Substring(i, length)));
		}
		return stringBuilder.ToString();
	}
}
