using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

public static class _0023_003DqaRCHBk37wN_1xkjpmQCj_oSaoDnFbjWHXLHeEPhAgKY_003D
{
	private struct _0023_003DqIgGOLMxaYnlvg9srbErdpQ_003D_003D
	{
		public long _0023_003Dqjv_Zzvl79QyfZx_7iNXeRQ_003D_003D;

		public int _0023_003DqBH4EWuA043LUiOJnRM969Q_003D_003D;
	}

	private static long _0023_003DqzTQixeOoVcySi5nvWPBlIA_003D_003D = 0L;

	private static List<_0023_003DqIgGOLMxaYnlvg9srbErdpQ_003D_003D> _0023_003DqR_Op7B1umGl0cRnON3Tkmg_003D_003D = new List<_0023_003DqIgGOLMxaYnlvg9srbErdpQ_003D_003D>(1048576);

	private static bool _0023_003DqWSQht6fL7ZwVUkq9Q28IgwsyVn_0024_c3hcdVS6e_BgX70_003D = false;

	public static List<string> _0023_003DqsPLagwy_0024TyMCDdhwb9NWeA_003D_003D = new List<string>();

	public static void _0023_003DqcwoodyJA8Mm983e4a2xNjw_003D_003D(int _0023_003DqUNAj1g2pcPmoBkxPZsImlA_003D_003D)
	{
		_0023_003DqR_Op7B1umGl0cRnON3Tkmg_003D_003D.Add(new _0023_003DqIgGOLMxaYnlvg9srbErdpQ_003D_003D
		{
			_0023_003Dqjv_Zzvl79QyfZx_7iNXeRQ_003D_003D = _0023_003DqdxOFKvf5xIUls6vHTW8pMA_003D_003D(),
			_0023_003DqBH4EWuA043LUiOJnRM969Q_003D_003D = _0023_003DqUNAj1g2pcPmoBkxPZsImlA_003D_003D
		});
	}

	public static void _0023_003DqJ3IfjYEubEuYcs3IoFRWwg_003D_003D()
	{
		_0023_003DqWSQht6fL7ZwVUkq9Q28IgwsyVn_0024_c3hcdVS6e_BgX70_003D = true;
	}

	public static void _0023_003Dq1VtvoP9A6djGUTyn5cH7dg_003D_003D()
	{
		if (_0023_003DqWSQht6fL7ZwVUkq9Q28IgwsyVn_0024_c3hcdVS6e_BgX70_003D && _0023_003DqR_Op7B1umGl0cRnON3Tkmg_003D_003D.Count > 0)
		{
			FileStream fileStream = new FileStream(_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850896133), new object[1] { _0023_003DqzTQixeOoVcySi5nvWPBlIA_003D_003D }), FileMode.Create);
			try
			{
				BinaryWriter binaryWriter = new BinaryWriter(fileStream, Encoding.ASCII);
				try
				{
					binaryWriter.Write(_0023_003DqsPLagwy_0024TyMCDdhwb9NWeA_003D_003D.Count);
					foreach (string item in _0023_003DqsPLagwy_0024TyMCDdhwb9NWeA_003D_003D)
					{
						binaryWriter.Write(item);
					}
					binaryWriter.Write(_0023_003DqR_Op7B1umGl0cRnON3Tkmg_003D_003D.Count);
					foreach (_0023_003DqIgGOLMxaYnlvg9srbErdpQ_003D_003D item2 in _0023_003DqR_Op7B1umGl0cRnON3Tkmg_003D_003D)
					{
						binaryWriter.Write(item2._0023_003Dqjv_Zzvl79QyfZx_7iNXeRQ_003D_003D);
						binaryWriter.Write(item2._0023_003DqBH4EWuA043LUiOJnRM969Q_003D_003D);
					}
				}
				finally
				{
					((IDisposable)binaryWriter).Dispose();
				}
			}
			finally
			{
				((IDisposable)fileStream).Dispose();
			}
		}
		_0023_003DqzTQixeOoVcySi5nvWPBlIA_003D_003D++;
		_0023_003DqR_Op7B1umGl0cRnON3Tkmg_003D_003D.Clear();
		_0023_003DqWSQht6fL7ZwVUkq9Q28IgwsyVn_0024_c3hcdVS6e_BgX70_003D = false;
	}

	[DllImport("Renderer_D3D11", CallingConvention = CallingConvention.Cdecl, EntryPoint = "RDTSCP")]
	public static extern long _0023_003DqdxOFKvf5xIUls6vHTW8pMA_003D_003D();
}
