using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public static class _0023_003DqN534GULB5BeNMI5RxlxTEP9rUGakdYGoW5eVZunJ6YE_003D
{
	private sealed class _0023_003Dq8_3tm2qVBshZ1ErSKR5rFF2bYz_iHfEv2s91TPVCYeE_003D
	{
		public byte _0023_003Dq0TQUffHVnhbU80DnKhylTw_003D_003D;

		internal bool _0023_003DqLOTR6daZMvmCdV_a43un_kkEwaIeua23Onk0zFOkmCk_003D(AtomType _0023_003DqhkVz7lyP5DnC_0024NJ4Vo5NnQ_003D_003D)
		{
			return _0023_003DqhkVz7lyP5DnC_0024NJ4Vo5NnQ_003D_003D._0023_003Dqcx_0024UKz7FtRL__sAQd4G2zA_003D_003D == _0023_003Dq0TQUffHVnhbU80DnKhylTw_003D_003D;
		}
	}

	private static readonly string _0023_003Dq97VcwEQ6ffYON0dQfgxPbQ_003D_003D = Path.Combine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850805785), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850832450));

	private static readonly string _0023_003Dq02d61Qlqdbl62HUD_0024lEo61oV_0024j0IiYJ09XQxCojmcyo_003D = Path.Combine(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850805785), _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850832494));

	private static readonly int _0023_003DqJtym_arPcQPxif1UvwX2NA_003D_003D = 55;

	private static readonly int _0023_003Dq92Jl_0024xSveCDtxO16BUAy6w_003D_003D = _0023_003DqJtym_arPcQPxif1UvwX2NA_003D_003D * 3;

	public static void _0023_003DqYnOgsgFPmJhuNyVsOGImSw_003D_003D(IEnumerable<SolitaireGameState> _0023_003DqtO1f45q1XtTJxGwHc6PaGQ_003D_003D)
	{
		BinaryWriter binaryWriter = new BinaryWriter(new FileStream(_0023_003Dq97VcwEQ6ffYON0dQfgxPbQ_003D_003D, FileMode.Create));
		try
		{
			binaryWriter.Write(_0023_003DqtO1f45q1XtTJxGwHc6PaGQ_003D_003D.Count());
			foreach (SolitaireGameState item in _0023_003DqtO1f45q1XtTJxGwHc6PaGQ_003D_003D)
			{
				_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqfxSWRLuFXHZUSet7MLuQHg_003D_003D(item._0023_003DqexLeKAIBX1eZYQpwTGL7iQ_003D_003D.Count == _0023_003DqJtym_arPcQPxif1UvwX2NA_003D_003D, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850832409));
				foreach (KeyValuePair<HexIndex, AtomType> item2 in item._0023_003DqexLeKAIBX1eZYQpwTGL7iQ_003D_003D)
				{
					binaryWriter.Write(item2.Value._0023_003Dqcx_0024UKz7FtRL__sAQd4G2zA_003D_003D);
					binaryWriter.Write((sbyte)item2.Key.Q);
					binaryWriter.Write((sbyte)item2.Key.R);
				}
			}
		}
		finally
		{
			((IDisposable)binaryWriter).Dispose();
		}
	}

	public static SolitaireGameState _0023_003DqACyATo2njRXISv5B_0024xgMmSW6E_rsScYgPgGha_eaHPo_003D(bool _0023_003DqklbncJwISmyWeMbnDOVAUA_003D_003D)
	{
		BinaryReader binaryReader = new BinaryReader(new FileStream(_0023_003DqklbncJwISmyWeMbnDOVAUA_003D_003D ? _0023_003Dq02d61Qlqdbl62HUD_0024lEo61oV_0024j0IiYJ09XQxCojmcyo_003D : _0023_003Dq97VcwEQ6ffYON0dQfgxPbQ_003D_003D, FileMode.Open, FileAccess.Read));
		try
		{
			int _0023_003DqhwmnSzB9kLizahHs7sxnXg_003D_003D = binaryReader.ReadInt32();
			binaryReader.BaseStream.Seek(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqpNEmaD21qG0Idrhw3f937A_003D_003D._0023_003Dq_00247KA5Om54G2_0024buGMqTUl_0024A_003D_003D(0, _0023_003DqhwmnSzB9kLizahHs7sxnXg_003D_003D) * _0023_003Dq92Jl_0024xSveCDtxO16BUAy6w_003D_003D, SeekOrigin.Current);
			HexRotation rotation = new HexRotation(_0023_003Dq4inqwnaZy3EVsj_0024PWmheeQ_003D_003D._0023_003DqpNEmaD21qG0Idrhw3f937A_003D_003D._0023_003Dq_00247KA5Om54G2_0024buGMqTUl_0024A_003D_003D(0, 6));
			SolitaireGameState solitaireGameState = new SolitaireGameState();
			for (int i = 0; i < _0023_003DqJtym_arPcQPxif1UvwX2NA_003D_003D; i++)
			{
				_0023_003Dq8_3tm2qVBshZ1ErSKR5rFF2bYz_iHfEv2s91TPVCYeE_003D _0023_003Dq8_3tm2qVBshZ1ErSKR5rFF2bYz_iHfEv2s91TPVCYeE_003D = new _0023_003Dq8_3tm2qVBshZ1ErSKR5rFF2bYz_iHfEv2s91TPVCYeE_003D();
				_0023_003Dq8_3tm2qVBshZ1ErSKR5rFF2bYz_iHfEv2s91TPVCYeE_003D._0023_003Dq0TQUffHVnhbU80DnKhylTw_003D_003D = binaryReader.ReadByte();
				AtomType value = _0023_003Dq3vzOR3N51kWoTzZyfeIUmQ_003D_003D._0023_003DqFcDIUD_pBOEdu0_5_00245afGw_003D_003D.Where(_0023_003Dq8_3tm2qVBshZ1ErSKR5rFF2bYz_iHfEv2s91TPVCYeE_003D._0023_003DqLOTR6daZMvmCdV_a43un_kkEwaIeua23Onk0zFOkmCk_003D).First();
				HexIndex key = new HexIndex(binaryReader.ReadSByte(), binaryReader.ReadSByte()).RotatedAround(new HexIndex(5, 0), rotation);
				solitaireGameState._0023_003DqexLeKAIBX1eZYQpwTGL7iQ_003D_003D.Add(key, value);
			}
			return solitaireGameState;
		}
		finally
		{
			((IDisposable)binaryReader).Dispose();
		}
	}
}
