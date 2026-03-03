using System;
using System.Diagnostics;

public struct Maybe<T> : IEquatable<Maybe<T>>
{
	private bool _0023_003Dqix_Z_0024_T9hepPR7Wn6QCDkr2A61oATmQap_kFF6iCxxA_003D;

	private T _0023_003DqBPPGbyTCxd0tCQWzXo1LdQ_003D_003D;

	public Maybe(bool _0023_003DqqJnEse_0024tHO5LRjEktKCYXw_003D_003D, T _0023_003DqIDZWYGsKD5Bvd_0024gXFkJwdA_003D_003D)
	{
		_0023_003DqUAbWvjExUmZ3q7ixRnarcQ_003D_003D(_0023_003DqqJnEse_0024tHO5LRjEktKCYXw_003D_003D);
		_0023_003DqBPPGbyTCxd0tCQWzXo1LdQ_003D_003D = _0023_003DqIDZWYGsKD5Bvd_0024gXFkJwdA_003D_003D;
	}

	public bool _0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D()
	{
		return _0023_003Dqix_Z_0024_T9hepPR7Wn6QCDkr2A61oATmQap_kFF6iCxxA_003D;
	}

	private void _0023_003DqUAbWvjExUmZ3q7ixRnarcQ_003D_003D(bool _0023_003DqrqeKwCl0IR1PBpypLgeU9Q_003D_003D)
	{
		_0023_003Dqix_Z_0024_T9hepPR7Wn6QCDkr2A61oATmQap_kFF6iCxxA_003D = _0023_003DqrqeKwCl0IR1PBpypLgeU9Q_003D_003D;
	}

	[DebuggerStepThrough]
	public T _0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()
	{
		if (!_0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			throw new InvalidOperationException(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850848147));
		}
		return _0023_003DqBPPGbyTCxd0tCQWzXo1LdQ_003D_003D;
	}

	private string _0023_003DqUPtSiVOFrhFP9VoTiO4A4PWSDEFEvS8y1FJxshvCUas_003D()
	{
		return ToString();
	}

	public static Maybe<T> _0023_003DqbnnqXYE2oy4BGa47diJXew_003D_003D(T _0023_003DquEscj8Ep1RqRWS_0024wk_SV_g_003D_003D)
	{
		if (_0023_003DquEscj8Ep1RqRWS_0024wk_SV_g_003D_003D == null)
		{
			throw new ArgumentNullException(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850848253));
		}
		return new Maybe<T>(_0023_003DqqJnEse_0024tHO5LRjEktKCYXw_003D_003D: true, _0023_003DquEscj8Ep1RqRWS_0024wk_SV_g_003D_003D);
	}

	public static implicit operator Maybe<T>(T _0023_003DqfVFp7gfNN3ruNdHHSLmSqA_003D_003D)
	{
		return _0023_003DqbnnqXYE2oy4BGa47diJXew_003D_003D(_0023_003DqfVFp7gfNN3ruNdHHSLmSqA_003D_003D);
	}

	public static implicit operator Maybe<T>(_0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D _0023_003DqckJQytWjo1sqr8EnGB1beA_003D_003D)
	{
		return new Maybe<T>(_0023_003DqqJnEse_0024tHO5LRjEktKCYXw_003D_003D: false, default(T));
	}

	public T _0023_003Dq3e1PtR_0024cLyGIxVVzJO8pbQ_003D_003D(T _0023_003DqkO7ce1lOBADS0xm4u5yzBQ_003D_003D)
	{
		if (!_0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			return _0023_003DqkO7ce1lOBADS0xm4u5yzBQ_003D_003D;
		}
		return _0023_003DqBPPGbyTCxd0tCQWzXo1LdQ_003D_003D;
	}

	public Maybe<T> _0023_003DqAbiygpG9lglX2koFXS_0024D7A_003D_003D(Maybe<T> _0023_003Dq3RpRyaBZSRL4HVv8sgnY_0024g_003D_003D)
	{
		if (!_0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			return _0023_003Dq3RpRyaBZSRL4HVv8sgnY_0024g_003D_003D;
		}
		return this;
	}

	public Maybe<TResult> _0023_003DqPcf7nIuTdNPLw_0024os6zyskQ_003D_003D<TResult>(Func<T, TResult> _0023_003Dqp6rgyNPIqHUpiEr1sfwwnA_003D_003D)
	{
		if (!_0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			return _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D;
		}
		return _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003DqI6EZ2kMRqL27dJEppKRE2w_003D_003D(_0023_003Dqp6rgyNPIqHUpiEr1sfwwnA_003D_003D(_0023_003DqBPPGbyTCxd0tCQWzXo1LdQ_003D_003D));
	}

	public void _0023_003DqC9C214FH5q3i9m0bAC59zQ_003D_003D(Action<T> _0023_003DqIyAjhCyuLivaGnI42DSAnw_003D_003D)
	{
		if (_0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			_0023_003DqIyAjhCyuLivaGnI42DSAnw_003D_003D(_0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D());
		}
	}

	public override string ToString()
	{
		if (!_0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			return _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850848065);
		}
		return _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850848115) + _0023_003DqBPPGbyTCxd0tCQWzXo1LdQ_003D_003D.ToString();
	}

	public override int GetHashCode()
	{
		if (!_0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			return 0;
		}
		return _0023_003DqBPPGbyTCxd0tCQWzXo1LdQ_003D_003D.GetHashCode();
	}

	public override bool Equals(object _0023_003DqWE3_GWmPqiGY15pSCMGdTg_003D_003D)
	{
		if (_0023_003DqWE3_GWmPqiGY15pSCMGdTg_003D_003D is Maybe<T>)
		{
			return Equals((Maybe<T>)_0023_003DqWE3_GWmPqiGY15pSCMGdTg_003D_003D);
		}
		return false;
	}

	public bool Equals(Maybe<T> _0023_003Dq4FH1JsPdHcKRoQpyXPfTUA_003D_003D)
	{
		if (!_0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D() && !_0023_003Dq4FH1JsPdHcKRoQpyXPfTUA_003D_003D._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			return true;
		}
		if (_0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D() && _0023_003Dq4FH1JsPdHcKRoQpyXPfTUA_003D_003D._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			ref T reference = ref _0023_003DqBPPGbyTCxd0tCQWzXo1LdQ_003D_003D;
			object obj = _0023_003Dq4FH1JsPdHcKRoQpyXPfTUA_003D_003D._0023_003DqBPPGbyTCxd0tCQWzXo1LdQ_003D_003D;
			return reference.Equals(obj);
		}
		return false;
	}

	public static bool operator ==(Maybe<T> _0023_003Dq_usP7GBckMGU7w6_0024lK7LFQ_003D_003D, Maybe<T> _0023_003DqGkRxnid9kdBqiH_0024XGdj4vg_003D_003D)
	{
		return _0023_003Dq_usP7GBckMGU7w6_0024lK7LFQ_003D_003D.Equals(_0023_003DqGkRxnid9kdBqiH_0024XGdj4vg_003D_003D);
	}

	public static bool operator !=(Maybe<T> _0023_003DqhXFA812pm0mAFs5fp_00249aKA_003D_003D, Maybe<T> _0023_003Dqu2gG9BngBwr7pTE8nuV4_g_003D_003D)
	{
		return !_0023_003DqhXFA812pm0mAFs5fp_00249aKA_003D_003D.Equals(_0023_003Dqu2gG9BngBwr7pTE8nuV4_g_003D_003D);
	}
}
