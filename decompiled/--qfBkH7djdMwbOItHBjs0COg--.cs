using System;
using Steamworks;

public struct _0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D : IEquatable<_0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D>
{
	public readonly ulong _0023_003Dq9H_0024qMUruoMzsUfuCJpHLCw_003D_003D;

	public _0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D(ulong _0023_003DqFH5KjuukBADhH9_YIT57yA_003D_003D)
	{
		_0023_003Dq9H_0024qMUruoMzsUfuCJpHLCw_003D_003D = _0023_003DqFH5KjuukBADhH9_YIT57yA_003D_003D;
	}

	public override string ToString()
	{
		CSteamID cSteamID = new CSteamID(_0023_003Dq9H_0024qMUruoMzsUfuCJpHLCw_003D_003D);
		return _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850849184) + cSteamID.GetAccountID();
	}

	public static implicit operator _0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D(CSteamID _0023_003DqwU7sO9jxk3ed1wdhmRHOgg_003D_003D)
	{
		return new _0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D(_0023_003DqwU7sO9jxk3ed1wdhmRHOgg_003D_003D.m_SteamID);
	}

	public static implicit operator CSteamID(_0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D _0023_003DqKH0gSWpulyYDqjJzrzpGGA_003D_003D)
	{
		return new CSteamID(_0023_003DqKH0gSWpulyYDqjJzrzpGGA_003D_003D._0023_003Dq9H_0024qMUruoMzsUfuCJpHLCw_003D_003D);
	}

	public bool Equals(_0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D _0023_003DqvwG7DxxSzfmyZ_0024npyAwiZQ_003D_003D)
	{
		return _0023_003Dq9H_0024qMUruoMzsUfuCJpHLCw_003D_003D == _0023_003DqvwG7DxxSzfmyZ_0024npyAwiZQ_003D_003D._0023_003Dq9H_0024qMUruoMzsUfuCJpHLCw_003D_003D;
	}

	public override bool Equals(object _0023_003DqXZ5a7feClg4M6dggRN64QA_003D_003D)
	{
		_0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D? _0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D2 = _0023_003DqXZ5a7feClg4M6dggRN64QA_003D_003D as _0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D?;
		if (_0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D2.HasValue)
		{
			return Equals(_0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D2.Value);
		}
		return false;
	}

	public override int GetHashCode()
	{
		throw new NotImplementedException();
	}

	public static bool operator ==(_0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D _0023_003Dq_rrI2F7ByeOKNHC17SSpgQ_003D_003D, _0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D _0023_003DqwmqpEFYGutZHD7roNfhwvQ_003D_003D)
	{
		return _0023_003Dq_rrI2F7ByeOKNHC17SSpgQ_003D_003D.Equals(_0023_003DqwmqpEFYGutZHD7roNfhwvQ_003D_003D);
	}

	public static bool operator !=(_0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D _0023_003DqrVQxOmXuRszekrEzhPXHow_003D_003D, _0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D _0023_003DqaRM_00246KA7aoPLDGi5ZI3kUw_003D_003D)
	{
		return !_0023_003DqrVQxOmXuRszekrEzhPXHow_003D_003D.Equals(_0023_003DqaRM_00246KA7aoPLDGi5ZI3kUw_003D_003D);
	}

	public static _0023_003DqfBkH7djdMwbOItHBjs0COg_003D_003D _0023_003DqdnNk_iKj1VTD2Va9mJnEIg_003D_003D()
	{
		return SteamUser.GetSteamID();
	}
}
