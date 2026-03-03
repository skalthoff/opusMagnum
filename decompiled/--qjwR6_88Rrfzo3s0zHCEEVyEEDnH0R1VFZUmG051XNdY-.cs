using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.CompilerServices;

public static class _0023_003DqjwR6_88Rrfzo3s0zHCEEVyEEDnH0R1VFZUmG051XNdY_003D
{
	private sealed class _0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D> : IEnumerator<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D>, IEnumerable<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D>, IEnumerable, IEnumerator, IDisposable
	{
		private int _0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D;

		private _0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D _0023_003Dq3W24hvjf5Ba8RCY_0024PGvEHg_003D_003D;

		private int _0023_003DqFtjJsj4yM5Z6vducrJ3Kao4q1I6wcZ__0024rOfXhgq4Y_Y_003D;

		private IEnumerable<Maybe<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D>> _0023_003Dqf0Bcfl0g84epCAzB2zE6Lw_003D_003D;

		public IEnumerable<Maybe<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D>> _0023_003Dqn2lvCV4M9lcPMbpgLfU9ug_003D_003D;

		private IEnumerator<Maybe<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D>> _0023_003Dqj1FbQ5DXs1aX3tWr5tZ_0024kA_003D_003D;

		[DebuggerHidden]
		public _0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D(int _0023_003DqRC4qCzi2YHTVEjMcwF7ehw_003D_003D)
		{
			_0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D = _0023_003DqRC4qCzi2YHTVEjMcwF7ehw_003D_003D;
			_0023_003DqFtjJsj4yM5Z6vducrJ3Kao4q1I6wcZ__0024rOfXhgq4Y_Y_003D = Environment.CurrentManagedThreadId;
		}

		[DebuggerHidden]
		private void _0023_003DqyxBPLSm4VcybpBWsQqLWSg32W4B6QYE4_0024mmpA4BtZv8_003D()
		{
			int num = _0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D;
			if (num == -3 || num == 1)
			{
				try
				{
				}
				finally
				{
					_0023_003DqF5CY_00246FZrpcdqIGurkBTCg_003D_003D();
				}
			}
		}

		void IDisposable.Dispose()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qyxBPLSm4VcybpBWsQqLWSg32W4B6QYE4$mmpA4BtZv8=
			this._0023_003DqyxBPLSm4VcybpBWsQqLWSg32W4B6QYE4_0024mmpA4BtZv8_003D();
		}

		private bool MoveNext()
		{
			try
			{
				switch (_0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D)
				{
				default:
					return false;
				case 0:
					_0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D = -1;
					_0023_003Dqj1FbQ5DXs1aX3tWr5tZ_0024kA_003D_003D = _0023_003Dqf0Bcfl0g84epCAzB2zE6Lw_003D_003D.GetEnumerator();
					_0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D = -3;
					break;
				case 1:
					_0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D = -3;
					break;
				}
				while (_0023_003Dqj1FbQ5DXs1aX3tWr5tZ_0024kA_003D_003D.MoveNext())
				{
					Maybe<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D> current = _0023_003Dqj1FbQ5DXs1aX3tWr5tZ_0024kA_003D_003D.Current;
					if (current._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
					{
						_0023_003Dq3W24hvjf5Ba8RCY_0024PGvEHg_003D_003D = current._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D();
						_0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D = 1;
						return true;
					}
				}
				_0023_003DqF5CY_00246FZrpcdqIGurkBTCg_003D_003D();
				_0023_003Dqj1FbQ5DXs1aX3tWr5tZ_0024kA_003D_003D = null;
				return false;
			}
			catch
			{
				//try-fault
				_0023_003DqyxBPLSm4VcybpBWsQqLWSg32W4B6QYE4_0024mmpA4BtZv8_003D();
				throw;
			}
		}

		bool IEnumerator.MoveNext()
		{
			//ILSpy generated this explicit interface implementation from .override directive in MoveNext
			return this.MoveNext();
		}

		private void _0023_003DqF5CY_00246FZrpcdqIGurkBTCg_003D_003D()
		{
			_0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D = -1;
			if (_0023_003Dqj1FbQ5DXs1aX3tWr5tZ_0024kA_003D_003D != null)
			{
				_0023_003Dqj1FbQ5DXs1aX3tWr5tZ_0024kA_003D_003D.Dispose();
			}
		}

		[DebuggerHidden]
		private _0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D _0023_003DqvfXGvI9uwHNj0rzcgU0PbCUi_NS0PmfF1W08ION9MI6hJ8vP_00248DqmHnMX_0024sk5kE_0024Ma7_YDD6e7h_r9phXQk6zg_003D_003D()
		{
			return _0023_003Dq3W24hvjf5Ba8RCY_0024PGvEHg_003D_003D;
		}

		_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D IEnumerator<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D>.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qvfXGvI9uwHNj0rzcgU0PbCUi_NS0PmfF1W08ION9MI6hJ8vP$8DqmHnMX$sk5kE$Ma7_YDD6e7h_r9phXQk6zg==
			return this._0023_003DqvfXGvI9uwHNj0rzcgU0PbCUi_NS0PmfF1W08ION9MI6hJ8vP_00248DqmHnMX_0024sk5kE_0024Ma7_YDD6e7h_r9phXQk6zg_003D_003D();
		}

		[DebuggerHidden]
		private void _0023_003Dqcka8_iNwbpTA8EyYng7_0024mtHgoDF_0024FeNvdZvp_r5PyQ7DgR3pREBko3N4oNMI6hWB()
		{
			throw new NotSupportedException();
		}

		void IEnumerator.Reset()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qcka8_iNwbpTA8EyYng7$mtHgoDF$FeNvdZvp_r5PyQ7DgR3pREBko3N4oNMI6hWB
			this._0023_003Dqcka8_iNwbpTA8EyYng7_0024mtHgoDF_0024FeNvdZvp_r5PyQ7DgR3pREBko3N4oNMI6hWB();
		}

		[DebuggerHidden]
		private object _0023_003DqZF4MVD6B4Oik6Vgd_0024k_DdI_00241YMk808sEdeMs9EBU8SPhHYrr94Hs27Qo5bYGOEXE()
		{
			return _0023_003Dq3W24hvjf5Ba8RCY_0024PGvEHg_003D_003D;
		}

		object IEnumerator.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qZF4MVD6B4Oik6Vgd$k_DdI$1YMk808sEdeMs9EBU8SPhHYrr94Hs27Qo5bYGOEXE
			return this._0023_003DqZF4MVD6B4Oik6Vgd_0024k_DdI_00241YMk808sEdeMs9EBU8SPhHYrr94Hs27Qo5bYGOEXE();
		}

		[DebuggerHidden]
		private IEnumerator<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D> _0023_003DqkfIhoVb6iwMMviH0CD1txM1Cmtt7uJujTiEeEhUxRByiI9e16qZPlASLcdaFqoF_WKCowX_4mcEkSAoqAsEZoQ_003D_003D()
		{
			_0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D> _0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D;
			if (_0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D == -2 && _0023_003DqFtjJsj4yM5Z6vducrJ3Kao4q1I6wcZ__0024rOfXhgq4Y_Y_003D == Environment.CurrentManagedThreadId)
			{
				_0023_003Dq1haDoky3RPJGEHCNSEuvEQ_003D_003D = 0;
				_0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D = this;
			}
			else
			{
				_0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D = new _0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D>(0);
			}
			_0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D._0023_003Dqf0Bcfl0g84epCAzB2zE6Lw_003D_003D = _0023_003Dqn2lvCV4M9lcPMbpgLfU9ug_003D_003D;
			return _0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D;
		}

		IEnumerator<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D> IEnumerable<_0023_003Dq195pDNlW1PT0SyAPuxNpGg_003D_003D>.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qkfIhoVb6iwMMviH0CD1txM1Cmtt7uJujTiEeEhUxRByiI9e16qZPlASLcdaFqoF_WKCowX_4mcEkSAoqAsEZoQ==
			return this._0023_003DqkfIhoVb6iwMMviH0CD1txM1Cmtt7uJujTiEeEhUxRByiI9e16qZPlASLcdaFqoF_WKCowX_4mcEkSAoqAsEZoQ_003D_003D();
		}

		[DebuggerHidden]
		private IEnumerator _0023_003Dq3K4WrnkZrnwJQXi5jBdBSP43FZh6nIYIz5EUhwiVahjm9Hp_2KqK8JQKeqKAa8wa()
		{
			return _0023_003DqkfIhoVb6iwMMviH0CD1txM1Cmtt7uJujTiEeEhUxRByiI9e16qZPlASLcdaFqoF_WKCowX_4mcEkSAoqAsEZoQ_003D_003D();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q3K4WrnkZrnwJQXi5jBdBSP43FZh6nIYIz5EUhwiVahjm9Hp_2KqK8JQKeqKAa8wa
			return this._0023_003Dq3K4WrnkZrnwJQXi5jBdBSP43FZh6nIYIz5EUhwiVahjm9Hp_2KqK8JQKeqKAa8wa();
		}
	}

	private sealed class _0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D<_0023_003DqD22rjuFm3DuTY5XmYh02eQ_003D_003D, _0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D> : IEnumerator<_0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D>, IEnumerable<_0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D>, IEnumerable, IEnumerator, IDisposable
	{
		private int _0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D;

		private _0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D _0023_003Dq3ad3FKxnJRfSAM8iYANbjQ_003D_003D;

		private int _0023_003Dq6Kwf1hUuJftqj5iVsMxCOPwuCAzI_GTSO7fkglrXsYs_003D;

		private IEnumerable<_0023_003DqD22rjuFm3DuTY5XmYh02eQ_003D_003D> _0023_003Dq6UWSnrRXQ8vB4kH_gkF6UA_003D_003D;

		public IEnumerable<_0023_003DqD22rjuFm3DuTY5XmYh02eQ_003D_003D> _0023_003DqwqmMkr0V29Ela63JK_00247WiA_003D_003D;

		private Func<_0023_003DqD22rjuFm3DuTY5XmYh02eQ_003D_003D, Maybe<_0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D>> _0023_003Dq8mcI0CWWIysjfaB_0024NuAV4w_003D_003D;

		public Func<_0023_003DqD22rjuFm3DuTY5XmYh02eQ_003D_003D, Maybe<_0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D>> _0023_003DqdqxAznryglyoKs1d0W2E2w_003D_003D;

		private IEnumerator<_0023_003DqD22rjuFm3DuTY5XmYh02eQ_003D_003D> _0023_003DqI6xdr9s7LR6IY4ecgOq6WA_003D_003D;

		[DebuggerHidden]
		public _0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D(int _0023_003DqDFBdxgN9MZO22oK0cXGdxQ_003D_003D)
		{
			_0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D = _0023_003DqDFBdxgN9MZO22oK0cXGdxQ_003D_003D;
			_0023_003Dq6Kwf1hUuJftqj5iVsMxCOPwuCAzI_GTSO7fkglrXsYs_003D = Environment.CurrentManagedThreadId;
		}

		[DebuggerHidden]
		private void _0023_003DqsMYNGaP3rKryOp8J213clvH8_FDMi8VRJUjYM02cZiY_003D()
		{
			int num = _0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D;
			if (num == -3 || num == 1)
			{
				try
				{
				}
				finally
				{
					_0023_003DqKR0JfC6cOxiGsDhs_DWKmQ_003D_003D();
				}
			}
		}

		void IDisposable.Dispose()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qsMYNGaP3rKryOp8J213clvH8_FDMi8VRJUjYM02cZiY=
			this._0023_003DqsMYNGaP3rKryOp8J213clvH8_FDMi8VRJUjYM02cZiY_003D();
		}

		private bool MoveNext()
		{
			try
			{
				switch (_0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D)
				{
				default:
					return false;
				case 0:
					_0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D = -1;
					_0023_003DqI6xdr9s7LR6IY4ecgOq6WA_003D_003D = _0023_003Dq6UWSnrRXQ8vB4kH_gkF6UA_003D_003D.GetEnumerator();
					_0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D = -3;
					break;
				case 1:
					_0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D = -3;
					break;
				}
				while (_0023_003DqI6xdr9s7LR6IY4ecgOq6WA_003D_003D.MoveNext())
				{
					_0023_003DqD22rjuFm3DuTY5XmYh02eQ_003D_003D current = _0023_003DqI6xdr9s7LR6IY4ecgOq6WA_003D_003D.Current;
					Maybe<_0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D> maybe = _0023_003Dq8mcI0CWWIysjfaB_0024NuAV4w_003D_003D(current);
					if (maybe._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
					{
						_0023_003Dq3ad3FKxnJRfSAM8iYANbjQ_003D_003D = maybe._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D();
						_0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D = 1;
						return true;
					}
				}
				_0023_003DqKR0JfC6cOxiGsDhs_DWKmQ_003D_003D();
				_0023_003DqI6xdr9s7LR6IY4ecgOq6WA_003D_003D = null;
				return false;
			}
			catch
			{
				//try-fault
				_0023_003DqsMYNGaP3rKryOp8J213clvH8_FDMi8VRJUjYM02cZiY_003D();
				throw;
			}
		}

		bool IEnumerator.MoveNext()
		{
			//ILSpy generated this explicit interface implementation from .override directive in MoveNext
			return this.MoveNext();
		}

		private void _0023_003DqKR0JfC6cOxiGsDhs_DWKmQ_003D_003D()
		{
			_0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D = -1;
			if (_0023_003DqI6xdr9s7LR6IY4ecgOq6WA_003D_003D != null)
			{
				_0023_003DqI6xdr9s7LR6IY4ecgOq6WA_003D_003D.Dispose();
			}
		}

		[DebuggerHidden]
		private _0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D _0023_003Dqh5eFDlBKRUwyb_unQ1OQPWzVvJFKiMQWa71ICnNTtj6tSjD4St1yJAfl7Yk7pGIJ1Crd4Za_0024KolT0yinI69YQA_003D_003D()
		{
			return _0023_003Dq3ad3FKxnJRfSAM8iYANbjQ_003D_003D;
		}

		_0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D IEnumerator<_0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D>.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qh5eFDlBKRUwyb_unQ1OQPWzVvJFKiMQWa71ICnNTtj6tSjD4St1yJAfl7Yk7pGIJ1Crd4Za$KolT0yinI69YQA==
			return this._0023_003Dqh5eFDlBKRUwyb_unQ1OQPWzVvJFKiMQWa71ICnNTtj6tSjD4St1yJAfl7Yk7pGIJ1Crd4Za_0024KolT0yinI69YQA_003D_003D();
		}

		[DebuggerHidden]
		private void _0023_003Dqbs1BmQN9ZuHR953VgDxCLb0MhLc9CsXKMYjxjcZ2WFjLrHl8_00240X04vq4GufUv3K_0024()
		{
			throw new NotSupportedException();
		}

		void IEnumerator.Reset()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qbs1BmQN9ZuHR953VgDxCLb0MhLc9CsXKMYjxjcZ2WFjLrHl8$0X04vq4GufUv3K$
			this._0023_003Dqbs1BmQN9ZuHR953VgDxCLb0MhLc9CsXKMYjxjcZ2WFjLrHl8_00240X04vq4GufUv3K_0024();
		}

		[DebuggerHidden]
		private object _0023_003Dq2jDy7cUQn8X5GofSFJUoqkrX5KlQr00kk6w9e1gJ_0024FgSyNQ2RuvQL9CW7Y5bcvf1()
		{
			return _0023_003Dq3ad3FKxnJRfSAM8iYANbjQ_003D_003D;
		}

		object IEnumerator.get_Current()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=q2jDy7cUQn8X5GofSFJUoqkrX5KlQr00kk6w9e1gJ$FgSyNQ2RuvQL9CW7Y5bcvf1
			return this._0023_003Dq2jDy7cUQn8X5GofSFJUoqkrX5KlQr00kk6w9e1gJ_0024FgSyNQ2RuvQL9CW7Y5bcvf1();
		}

		[DebuggerHidden]
		private IEnumerator<_0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D> _0023_003DqGBS_0024stLkOvgbNsdmDcu07WX7OkNU8ZQ0Ijtd_0024Ka_LyeW2na7IS_GndXvu8zU3zDk1hjtSqEmvPhTmXX5WYMQCg_003D_003D()
		{
			_0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D<_0023_003DqD22rjuFm3DuTY5XmYh02eQ_003D_003D, _0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D> _0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D;
			if (_0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D == -2 && _0023_003Dq6Kwf1hUuJftqj5iVsMxCOPwuCAzI_GTSO7fkglrXsYs_003D == Environment.CurrentManagedThreadId)
			{
				_0023_003DqC04F6DMUs1Rf6l1eD68BrQ_003D_003D = 0;
				_0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D = this;
			}
			else
			{
				_0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D = new _0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D<_0023_003DqD22rjuFm3DuTY5XmYh02eQ_003D_003D, _0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D>(0);
			}
			_0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D._0023_003Dq6UWSnrRXQ8vB4kH_gkF6UA_003D_003D = _0023_003DqwqmMkr0V29Ela63JK_00247WiA_003D_003D;
			_0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D._0023_003Dq8mcI0CWWIysjfaB_0024NuAV4w_003D_003D = _0023_003DqdqxAznryglyoKs1d0W2E2w_003D_003D;
			return _0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D;
		}

		IEnumerator<_0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D> IEnumerable<_0023_003DqjXw_0024B6_0024oPvWtEvPIBJWyYg_003D_003D>.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qGBS$stLkOvgbNsdmDcu07WX7OkNU8ZQ0Ijtd$Ka_LyeW2na7IS_GndXvu8zU3zDk1hjtSqEmvPhTmXX5WYMQCg==
			return this._0023_003DqGBS_0024stLkOvgbNsdmDcu07WX7OkNU8ZQ0Ijtd_0024Ka_LyeW2na7IS_GndXvu8zU3zDk1hjtSqEmvPhTmXX5WYMQCg_003D_003D();
		}

		[DebuggerHidden]
		private IEnumerator _0023_003DqH7ltptFywR1fDOJ2Ikmzi5E2FmQJiU3_8gaGapkTHJW6NBaFVh92GGgmQp_0024DJ_qE()
		{
			return _0023_003DqGBS_0024stLkOvgbNsdmDcu07WX7OkNU8ZQ0Ijtd_0024Ka_LyeW2na7IS_GndXvu8zU3zDk1hjtSqEmvPhTmXX5WYMQCg_003D_003D();
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			//ILSpy generated this explicit interface implementation from .override directive in #=qH7ltptFywR1fDOJ2Ikmzi5E2FmQJiU3_8gaGapkTHJW6NBaFVh92GGgmQp$DJ_qE
			return this._0023_003DqH7ltptFywR1fDOJ2Ikmzi5E2FmQJiU3_8gaGapkTHJW6NBaFVh92GGgmQp_0024DJ_qE();
		}
	}

	public static Maybe<V> _0023_003DqC6vtwVlPrUBgtP2taoHUaQ_003D_003D<K, V>(this IDictionary<K, V> _0023_003DqaJvxgFFv7r8elFD6Oc9_Tw_003D_003D, K _0023_003DqtCsASnU2IQLhdiZ_psC9Ig_003D_003D)
	{
		if (_0023_003DqaJvxgFFv7r8elFD6Oc9_Tw_003D_003D.TryGetValue(_0023_003DqtCsASnU2IQLhdiZ_psC9Ig_003D_003D, out var value))
		{
			return value;
		}
		return _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D;
	}

	[IteratorStateMachine(typeof(_0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D))]
	public static IEnumerable<T> _0023_003Dqgr898NH6S8NROCHUGIUkuw_003D_003D<T>(this IEnumerable<Maybe<T>> _0023_003DqrbEyCZcl_uofNDB3MwFLyg_003D_003D)
	{
		return new _0023_003Dq3Mrm5v0ZTwePFPYJiGim5Q_003D_003D<T>(-2)
		{
			_0023_003Dqn2lvCV4M9lcPMbpgLfU9ug_003D_003D = _0023_003DqrbEyCZcl_uofNDB3MwFLyg_003D_003D
		};
	}

	[IteratorStateMachine(typeof(_0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D))]
	public static IEnumerable<R> _0023_003DqTnoha8SMgZNYla68obDa8g_003D_003D<T, R>(this IEnumerable<T> _0023_003DqW8es8dmRbshC0gI4S9Jqag_003D_003D, Func<T, Maybe<R>> _0023_003DqkIwUsrUW0Yq_0024m_0024j0xJ2XVQ_003D_003D)
	{
		return new _0023_003DqFVPGM83o6Ud9DWTXbKOL_0024iqipoduBOAYCZfNjB_0024_0024NQQ_003D<T, R>(-2)
		{
			_0023_003DqwqmMkr0V29Ela63JK_00247WiA_003D_003D = _0023_003DqW8es8dmRbshC0gI4S9Jqag_003D_003D,
			_0023_003DqdqxAznryglyoKs1d0W2E2w_003D_003D = _0023_003DqkIwUsrUW0Yq_0024m_0024j0xJ2XVQ_003D_003D
		};
	}

	public static bool _0023_003Dqc99NvZke7P1sg2faI4lRfQ_003D_003D<T>(this Maybe<T> _0023_003DqZL2yklutRpm_nG1JOi7FbA_003D_003D, out T _0023_003DquEY_0024MzT9MHGsrXhV38y2Kw_003D_003D)
	{
		if (_0023_003DqZL2yklutRpm_nG1JOi7FbA_003D_003D._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			_0023_003DquEY_0024MzT9MHGsrXhV38y2Kw_003D_003D = _0023_003DqZL2yklutRpm_nG1JOi7FbA_003D_003D._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D();
			return true;
		}
		_0023_003DquEY_0024MzT9MHGsrXhV38y2Kw_003D_003D = default(T);
		return false;
	}
}
