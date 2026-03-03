using System;
using System.Runtime.InteropServices;

public sealed class _0023_003Dqdbf_0024_0024bbkj46ZWn2bE5VQF1sZs8q3Tu5CC4glbfgrVlSMnkskAObjnoliPLTgsa0U : _0023_003DqXhSbdylNCfjvgmRm2IVwL0TTag6K5xOns1KYXb4Pc6s_003D
{
	public IntPtr _0023_003Dq_X4iMu7MOxonxnJquM928A_003D_003D;

	private bool _0023_003DqNJDHFKGMbQJ3Hu7spxdOQA_003D_003D;

	public unsafe override void _0023_003DqtfljzuyBUDneaF3KnQEFbw_003D_003D(short* _0023_003Dq4W_llVt0Pvj32vbefDskuA_003D_003D, int _0023_003DqzBm53gO6Idq_0024_A76fY5u3Q_003D_003D, float _0023_003DqW2DiGHw9q2snsh1KVF8MOA_003D_003D, bool _0023_003Dqfw7ou2CpLk1XSTQNT8OhCw_003D_003D)
	{
		short[] array = new short[_0023_003DqzBm53gO6Idq_0024_A76fY5u3Q_003D_003D];
		int num2;
		for (int i = 0; i < _0023_003DqzBm53gO6Idq_0024_A76fY5u3Q_003D_003D; i += num2)
		{
			int num = _0023_003DqzBm53gO6Idq_0024_A76fY5u3Q_003D_003D - i;
			fixed (short* ptr = array)
			{
				num2 = _0023_003DqMcf1HHLLYywbUUfvtExVblDD3u1gi3N1IsSv87CHXjolNgFOvB7Vg_hdIiJxis7r._0023_003Dq2ydrvkb0DxWDfT1E3gqmdQ_003D_003D(_0023_003Dq_X4iMu7MOxonxnJquM928A_003D_003D, (byte*)ptr + (nint)i * (nint)2, num * 2, 0, 2, 1, out var _);
			}
			if (num2 == 0)
			{
				if (!_0023_003Dqfw7ou2CpLk1XSTQNT8OhCw_003D_003D)
				{
					_0023_003DqNJDHFKGMbQJ3Hu7spxdOQA_003D_003D = true;
					for (; i < _0023_003DqzBm53gO6Idq_0024_A76fY5u3Q_003D_003D; i++)
					{
						array[i] = 0;
					}
					break;
				}
				_0023_003DqMcf1HHLLYywbUUfvtExVblDD3u1gi3N1IsSv87CHXjolNgFOvB7Vg_hdIiJxis7r._0023_003DqZVXAxbqBob_5OpcNl6jofw_003D_003D(_0023_003Dq_X4iMu7MOxonxnJquM928A_003D_003D, 0.0);
			}
			else if (num2 < 0)
			{
				throw new _0023_003DqRaaOoTBvHvWK2vyz8S665Q_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850811138));
			}
			num2 /= 2;
		}
		for (int j = 0; j < _0023_003DqzBm53gO6Idq_0024_A76fY5u3Q_003D_003D; j++)
		{
			int num3 = _0023_003Dq4W_llVt0Pvj32vbefDskuA_003D_003D[j];
			int num4 = array[j];
			int num5 = (int)(128f * _0023_003DqW2DiGHw9q2snsh1KVF8MOA_003D_003D);
			num4 = num4 * num5 / 128;
			_0023_003Dq4W_llVt0Pvj32vbefDskuA_003D_003D[j] = (short)_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqURBbaL72HtfW40SuvLCq7A_003D_003D(num3 + num4, -32768, 32767);
		}
	}

	public override bool _0023_003DqTHXCuf2h_0024zPiKjnBWJ21Ng_003D_003D()
	{
		return _0023_003DqNJDHFKGMbQJ3Hu7spxdOQA_003D_003D;
	}

	public override void _0023_003DqAlRtXfGk5_002418qnCwaJs9GA_003D_003D(double _0023_003Dqrv3cMJy_VAE1OuJryyy7iQ_003D_003D)
	{
		_0023_003DqMcf1HHLLYywbUUfvtExVblDD3u1gi3N1IsSv87CHXjolNgFOvB7Vg_hdIiJxis7r._0023_003DqZVXAxbqBob_5OpcNl6jofw_003D_003D(_0023_003Dq_X4iMu7MOxonxnJquM928A_003D_003D, _0023_003Dqrv3cMJy_VAE1OuJryyy7iQ_003D_003D);
		_0023_003DqNJDHFKGMbQJ3Hu7spxdOQA_003D_003D = false;
	}

	public override void _0023_003Dqaw_0024ZRoWNpX43_00246TH8oDwiQ_003D_003D()
	{
		_0023_003DqMcf1HHLLYywbUUfvtExVblDD3u1gi3N1IsSv87CHXjolNgFOvB7Vg_hdIiJxis7r._0023_003DqiDg7auILN1W_YcaszO_0024HKA_003D_003D(_0023_003Dq_X4iMu7MOxonxnJquM928A_003D_003D);
		Marshal.FreeHGlobal(_0023_003Dq_X4iMu7MOxonxnJquM928A_003D_003D);
	}
}
