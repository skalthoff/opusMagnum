using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public sealed class ConfigFile
{
	[Serializable]
	private sealed class _003C_003Ec
	{
		public static readonly _003C_003Ec _003C_003E9 = new _003C_003Ec();

		public static Func<KeyValuePair<string, string>, string> _003C_003E9__11_0;

		internal string _0023_003DqzrboeVNwbwhGL97faivlN02rmMLHR62CVHprOHOh4ao_003D(KeyValuePair<string, string> _0023_003DqHSMM_0024Wpzi1nh358fkPr8bg_003D_003D)
		{
			return _0023_003DqHSMM_0024Wpzi1nh358fkPr8bg_003D_003D.Key;
		}
	}

	private readonly string _0023_003DqKHK5IF2NJz6W5cYYzpCY0A_003D_003D;

	private Dictionary<string, string> _0023_003DqOHWfF8NCHA7Iqd25O7TfzQ_003D_003D = new Dictionary<string, string>();

	private bool _0023_003Dqga7TaAcd_plPdpwjpK0Rjg_003D_003D = true;

	private bool _0023_003DqG7WzCAoIeVBilZ_PxwnvPQ_003D_003D;

	public ConfigFile(string _0023_003Dq5XM_HEhJ4_0024Yf_Dwvk7C2jw_003D_003D)
	{
		_0023_003DqKHK5IF2NJz6W5cYYzpCY0A_003D_003D = _0023_003Dq5XM_HEhJ4_0024Yf_Dwvk7C2jw_003D_003D;
	}

	public void _0023_003Dq_53TovDY0AnSdisVj66tnQ_003D_003D(string _0023_003DqM9ZPYT5v6bv3m7S8IdjSVQ_003D_003D, string _0023_003DqJ_v3X2tsMWwoU9nvNr3A1w_003D_003D)
	{
		_0023_003DqKs_76fvdvORlz2PRZtTN8neunUrQHPX_RF3yD5RS3b4_003D();
		_0023_003DqOHWfF8NCHA7Iqd25O7TfzQ_003D_003D[_0023_003DqM9ZPYT5v6bv3m7S8IdjSVQ_003D_003D] = _0023_003DqJ_v3X2tsMWwoU9nvNr3A1w_003D_003D;
		_0023_003DqG7WzCAoIeVBilZ_PxwnvPQ_003D_003D = true;
	}

	public void _0023_003DqdQv7MHyMeWVveDlhNmA5eg_003D_003D(string _0023_003DqKsFInhSMsEDLHBEG97JINQ_003D_003D)
	{
		_0023_003DqKs_76fvdvORlz2PRZtTN8neunUrQHPX_RF3yD5RS3b4_003D();
		_0023_003DqOHWfF8NCHA7Iqd25O7TfzQ_003D_003D.Remove(_0023_003DqKsFInhSMsEDLHBEG97JINQ_003D_003D);
		_0023_003DqG7WzCAoIeVBilZ_PxwnvPQ_003D_003D = true;
	}

	public void _0023_003Dq1aUi7rRPY0MLTXHLpxs3iQ_003D_003D(string _0023_003DqRSy3MRBCO7RBMPI_4VS_3Q_003D_003D, Maybe<string> _0023_003DqztafvmG_TtdpxhR0pzHjQg_003D_003D)
	{
		if (_0023_003DqztafvmG_TtdpxhR0pzHjQg_003D_003D._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			_0023_003Dq_53TovDY0AnSdisVj66tnQ_003D_003D(_0023_003DqRSy3MRBCO7RBMPI_4VS_3Q_003D_003D, _0023_003DqztafvmG_TtdpxhR0pzHjQg_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D());
		}
		else
		{
			_0023_003DqdQv7MHyMeWVveDlhNmA5eg_003D_003D(_0023_003DqRSy3MRBCO7RBMPI_4VS_3Q_003D_003D);
		}
	}

	public Maybe<string> _0023_003Dqt3r1kJGB3m8jvPwkrCU2zw_003D_003D(string _0023_003DqyRy_0024sMBDn7_002450o8iYH1TCg_003D_003D)
	{
		_0023_003DqKs_76fvdvORlz2PRZtTN8neunUrQHPX_RF3yD5RS3b4_003D();
		return _0023_003DqOHWfF8NCHA7Iqd25O7TfzQ_003D_003D._0023_003DqC6vtwVlPrUBgtP2taoHUaQ_003D_003D(_0023_003DqyRy_0024sMBDn7_002450o8iYH1TCg_003D_003D);
	}

	public Maybe<T> _0023_003DqZO_0024doCifbBbiq6jXiWQFwg_003D_003D<T>(global::_0023_003DqtKydocUFiqoTVliZV1HvAJzUIvMpdHPpnpuq_0024oqq4P0_003D<T> _0023_003Dqp3tn_00240ytQSwG4fuGz4tZGg_003D_003D, string _0023_003Dq8EfVN2OL0Ul_jyvVdrY7nA_003D_003D)
	{
		_0023_003DqKs_76fvdvORlz2PRZtTN8neunUrQHPX_RF3yD5RS3b4_003D();
		if (_0023_003DqOHWfF8NCHA7Iqd25O7TfzQ_003D_003D.TryGetValue(_0023_003Dq8EfVN2OL0Ul_jyvVdrY7nA_003D_003D, out var value) && _0023_003Dqp3tn_00240ytQSwG4fuGz4tZGg_003D_003D(value, out var _0023_003Dq8z6Qdc3064hqwrMb4xga_Q_003D_003D))
		{
			return _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003DqI6EZ2kMRqL27dJEppKRE2w_003D_003D(_0023_003Dq8z6Qdc3064hqwrMb4xga_Q_003D_003D);
		}
		return _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D;
	}

	private void _0023_003DqKs_76fvdvORlz2PRZtTN8neunUrQHPX_RF3yD5RS3b4_003D()
	{
		if (!_0023_003Dqga7TaAcd_plPdpwjpK0Rjg_003D_003D)
		{
			return;
		}
		_0023_003Dqga7TaAcd_plPdpwjpK0Rjg_003D_003D = false;
		if (!File.Exists(_0023_003DqKHK5IF2NJz6W5cYYzpCY0A_003D_003D))
		{
			return;
		}
		string[] array = File.ReadAllText(_0023_003DqKHK5IF2NJz6W5cYYzpCY0A_003D_003D).Split('\n');
		for (int i = 0; i < array.Length; i++)
		{
			string[] array2 = array[i].Split(new char[1] { '=' }, 2);
			if (array2.Length == 2)
			{
				_0023_003DqOHWfF8NCHA7Iqd25O7TfzQ_003D_003D.Add(array2[0].Trim(), array2[1].Trim());
			}
		}
	}

	public void _0023_003DqxUtJGJgJbHOsSuZkqj6EjlMBwK7ahkyQqQgp_mO0_jw_003D()
	{
		if (!_0023_003DqG7WzCAoIeVBilZ_PxwnvPQ_003D_003D)
		{
			return;
		}
		_0023_003DqG7WzCAoIeVBilZ_PxwnvPQ_003D_003D = false;
		_0023_003DqKs_76fvdvORlz2PRZtTN8neunUrQHPX_RF3yD5RS3b4_003D();
		List<string> list = new List<string>();
		foreach (KeyValuePair<string, string> item in _0023_003DqOHWfF8NCHA7Iqd25O7TfzQ_003D_003D.OrderBy(_003C_003Ec._003C_003E9._0023_003DqzrboeVNwbwhGL97faivlN02rmMLHR62CVHprOHOh4ao_003D))
		{
			list.Add(_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850805827), new object[2] { item.Key, item.Value }));
		}
		string _0023_003DqdraSFRwiJwYq_nJy7shFFw_003D_003D = string.Join(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850805875), list);
		_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqE2UCoKUDW6hVF11Ger3hhg_003D_003D._0023_003Dq8538ntTv9vI9I_0024SEEUBkWg_003D_003D(_0023_003DqKHK5IF2NJz6W5cYYzpCY0A_003D_003D, _0023_003DqdraSFRwiJwYq_nJy7shFFw_003D_003D);
	}
}
