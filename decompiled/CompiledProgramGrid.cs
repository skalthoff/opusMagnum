using System;
using System.Collections.Generic;
using System.Linq;

public sealed class CompiledProgramGrid
{
	[Serializable]
	private sealed class _003C_003Ec
	{
		public static readonly _003C_003Ec _003C_003E9 = new _003C_003Ec();

		public static Func<CompiledInstruction, bool> _003C_003E9__6_1;

		public static Func<CompiledProgram, int> _003C_003E9__6_0;

		internal int _0023_003DqU58s3N9bY14Fg3KqKP17mLN538Q11JcQdsm2uCVvncHdKqnObHA5GFi3rjvzJ1Wu(CompiledProgram _0023_003DqD0eE2GL7No1b2dUbOwmweA_003D_003D)
		{
			return _0023_003DqD0eE2GL7No1b2dUbOwmweA_003D_003D._0023_003Dq5Z33P_wuPyJ_0024_0024TQ1S3eTxA_003D_003D.Count(_003C_003E9._0023_003DqMEDuBJHr4Pytd8hDhbK2yustn_0cS7jTBHXQAUSfEdKEN8vYChsNoR6nfsldLPfo);
		}

		internal bool _0023_003DqMEDuBJHr4Pytd8hDhbK2yustn_0cS7jTBHXQAUSfEdKEN8vYChsNoR6nfsldLPfo(CompiledInstruction _0023_003DqQme6gnshLq_A2nDN8CHVNA_003D_003D)
		{
			return _0023_003DqQme6gnshLq_A2nDN8CHVNA_003D_003D._0023_003DqFsjBqPtolS56yaDjfGv3kw_003D_003D._0023_003DqsMddpKuoTWWsfVYmyPbsmoXOZewz3wUPckRrcEfiARM_003D;
		}
	}

	private readonly Dictionary<Part, CompiledProgram> _0023_003DqkpABeo6y3dSrKfjpCFPGeF6nEiBzoFnwnFWKOqJO3KU_003D;

	public readonly int _0023_003Dq7ozQmBasxD6FcbBhVx9LGg_003D_003D;

	private CompiledProgramGrid(Dictionary<Part, CompiledProgram> _0023_003DqkpcaCKOkfJgRf5sKoxmLfSBAgslHvLsVtbD1UVHoDew_003D)
	{
		_0023_003DqkpABeo6y3dSrKfjpCFPGeF6nEiBzoFnwnFWKOqJO3KU_003D = _0023_003DqkpcaCKOkfJgRf5sKoxmLfSBAgslHvLsVtbD1UVHoDew_003D;
		_0023_003Dq7ozQmBasxD6FcbBhVx9LGg_003D_003D = int.MaxValue;
		foreach (KeyValuePair<Part, CompiledProgram> item in _0023_003DqkpcaCKOkfJgRf5sKoxmLfSBAgslHvLsVtbD1UVHoDew_003D)
		{
			if (item.Key._0023_003DqjHP1sj_3quumJKQydW_wwg_003D_003D()._0023_003Dq3C8jwYES6g1bEWKSY_0024jLeA_003D_003D)
			{
				_0023_003Dq7ozQmBasxD6FcbBhVx9LGg_003D_003D = Math.Min(_0023_003Dq7ozQmBasxD6FcbBhVx9LGg_003D_003D, item.Value._0023_003DqEBEIQn0kJWNPqzVx1DFTqQ_003D_003D);
			}
		}
		if (_0023_003Dq7ozQmBasxD6FcbBhVx9LGg_003D_003D == int.MaxValue)
		{
			_0023_003Dq7ozQmBasxD6FcbBhVx9LGg_003D_003D = 0;
		}
	}

	public CompiledProgram _0023_003DqGXmnJ1E68pgmnB_0024m5VjIJBTJyOucQWWfNAIDueKlPqw_003D(Part _0023_003Dqj04_0024TZluuyx1u1W_ei685g_003D_003D)
	{
		return _0023_003DqkpABeo6y3dSrKfjpCFPGeF6nEiBzoFnwnFWKOqJO3KU_003D[_0023_003Dqj04_0024TZluuyx1u1W_ei685g_003D_003D];
	}

	public InstructionType _0023_003DqXj2r_for4EymTZl_iTMAFSc2juxow_0024HNP0idq3FLHjU_003D(int _0023_003DqdycK45uhJNk46RpT3j0CHQ_003D_003D, Part _0023_003DqN_BFAWrL54_0024Llu2_0024GxEejg_003D_003D, out Maybe<int> _0023_003DqTxMmvJwEYM3K7QJy_00245SVEA_003D_003D)
	{
		_0023_003DqdycK45uhJNk46RpT3j0CHQ_003D_003D += _0023_003Dq7ozQmBasxD6FcbBhVx9LGg_003D_003D;
		CompiledProgram compiledProgram = _0023_003DqkpABeo6y3dSrKfjpCFPGeF6nEiBzoFnwnFWKOqJO3KU_003D[_0023_003DqN_BFAWrL54_0024Llu2_0024GxEejg_003D_003D];
		if (_0023_003DqdycK45uhJNk46RpT3j0CHQ_003D_003D < compiledProgram._0023_003DqEBEIQn0kJWNPqzVx1DFTqQ_003D_003D || compiledProgram._0023_003Dq5Z33P_wuPyJ_0024_0024TQ1S3eTxA_003D_003D.Length == 0)
		{
			_0023_003DqTxMmvJwEYM3K7QJy_00245SVEA_003D_003D = _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D;
			return _0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqnfS_RHumkmeUAypUlxzKYg_003D_003D;
		}
		int num = (_0023_003DqdycK45uhJNk46RpT3j0CHQ_003D_003D - compiledProgram._0023_003DqEBEIQn0kJWNPqzVx1DFTqQ_003D_003D) % compiledProgram._0023_003Dq5Z33P_wuPyJ_0024_0024TQ1S3eTxA_003D_003D.Length;
		_0023_003DqTxMmvJwEYM3K7QJy_00245SVEA_003D_003D = compiledProgram._0023_003DqEBEIQn0kJWNPqzVx1DFTqQ_003D_003D + num;
		return compiledProgram._0023_003Dq5Z33P_wuPyJ_0024_0024TQ1S3eTxA_003D_003D[num]._0023_003DqFsjBqPtolS56yaDjfGv3kw_003D_003D;
	}

	public int _0023_003Dqsh8FX0JW74wOeavrglKR3GnLmnBMf8EY7EqvlfFAO7E_003D(int _0023_003Dq4IUjlsLQGpSah_0024ySueIZhQ_003D_003D)
	{
		if (_0023_003DqkpABeo6y3dSrKfjpCFPGeF6nEiBzoFnwnFWKOqJO3KU_003D.Count > 0)
		{
			return _0023_003Dq4IUjlsLQGpSah_0024ySueIZhQ_003D_003D % _0023_003DqkpABeo6y3dSrKfjpCFPGeF6nEiBzoFnwnFWKOqJO3KU_003D.Values.First()._0023_003Dq5Z33P_wuPyJ_0024_0024TQ1S3eTxA_003D_003D.Length;
		}
		return 0;
	}

	public int _0023_003DqzBikIHGd8BkT2T_ZMa6rus3tUpUo2tVh5Zs9GKWC_00245s_003D()
	{
		return ((IEnumerable<CompiledProgram>)_0023_003DqkpABeo6y3dSrKfjpCFPGeF6nEiBzoFnwnFWKOqJO3KU_003D.Values).Sum((Func<CompiledProgram, int>)_003C_003Ec._003C_003E9._0023_003DqU58s3N9bY14Fg3KqKP17mLN538Q11JcQdsm2uCVvncHdKqnObHA5GFi3rjvzJ1Wu);
	}

	public static Maybe<CompiledProgramGrid> _0023_003Dq5GTg7Y6iohLt1Ny5XPf7xA_003D_003D(Solution _0023_003DqgNq20zTS18ho0LVvZ88uhQ_003D_003D)
	{
		Dictionary<Part, SortedDictionary<int, CompiledInstruction>> dictionary = new Dictionary<Part, SortedDictionary<int, CompiledInstruction>>();
		foreach (Part item in _0023_003DqgNq20zTS18ho0LVvZ88uhQ_003D_003D._0023_003DqfrDV_0024CNeCIILdYiZJ_00241dxw_003D_003D)
		{
			_0023_003DqKYuJGbytUkf2YwXktoGt8Qeu8xEFMb_0024tRFW8xyxKZjk_003D obj = item._0023_003DqQHM7j2biuh6qdumH6FrXJw_003D_003D._0023_003DqyBQSjTHnDEGcyfMCR8oAJw_003D_003D(item, _0023_003DqgNq20zTS18ho0LVvZ88uhQ_003D_003D._0023_003DqJ1MhB_0024GYDM5ApFxJO1ueLeCFQ3DB_0024TBftC0938zz9Qo_003D(item));
			SortedDictionary<int, CompiledInstruction> sortedDictionary = new SortedDictionary<int, CompiledInstruction>();
			foreach (KeyValuePair<int, _0023_003DquBkTOLR2k76qHn6i8uQcr9MfeXYDMJh_x5p9KuT6dkc_003D> item2 in obj._0023_003Dq9buXmtGFAtljeTx2qFiqDg_003D_003D)
			{
				_0023_003DquBkTOLR2k76qHn6i8uQcr9MfeXYDMJh_x5p9KuT6dkc_003D value = item2.Value;
				for (int i = 0; i < value._0023_003DqZmttNA4eyU8PIshICuILyg_003D_003D.Length; i++)
				{
					int key = item2.Key + i;
					if (sortedDictionary.ContainsKey(key))
					{
						return _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D;
					}
					sortedDictionary[key] = new CompiledInstruction
					{
						_0023_003DqFsjBqPtolS56yaDjfGv3kw_003D_003D = value._0023_003DqZmttNA4eyU8PIshICuILyg_003D_003D[i],
						_0023_003DqCMIzY_bYqX0GeYTa8cWEnaPDJTLKdmL8H9huoN7tXT4_003D = (i > 0)
					};
				}
			}
			dictionary[item] = sortedDictionary;
		}
		int num = 0;
		foreach (KeyValuePair<Part, SortedDictionary<int, CompiledInstruction>> item3 in dictionary)
		{
			if (item3.Value.Count > 0)
			{
				num = Math.Max(num, item3.Value.Keys.Last() - item3.Value.Keys.First() + 1);
			}
		}
		Dictionary<Part, CompiledProgram> dictionary2 = new Dictionary<Part, CompiledProgram>();
		foreach (KeyValuePair<Part, SortedDictionary<int, CompiledInstruction>> item4 in dictionary)
		{
			int num2 = ((item4.Value.Count != 0) ? item4.Value.Keys.First() : 0);
			CompiledProgram compiledProgram = new CompiledProgram
			{
				_0023_003DqEBEIQn0kJWNPqzVx1DFTqQ_003D_003D = num2,
				_0023_003Dq5Z33P_wuPyJ_0024_0024TQ1S3eTxA_003D_003D = new CompiledInstruction[num]
			};
			bool _0023_003DqCMIzY_bYqX0GeYTa8cWEnaPDJTLKdmL8H9huoN7tXT4_003D = false;
			for (int j = 0; j < num; j++)
			{
				Maybe<CompiledInstruction> maybe = item4.Value._0023_003DqC6vtwVlPrUBgtP2taoHUaQ_003D_003D(num2 + j);
				if (maybe._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
				{
					compiledProgram._0023_003Dq5Z33P_wuPyJ_0024_0024TQ1S3eTxA_003D_003D[j] = maybe._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D();
				}
				else
				{
					compiledProgram._0023_003Dq5Z33P_wuPyJ_0024_0024TQ1S3eTxA_003D_003D[j] = new CompiledInstruction
					{
						_0023_003DqFsjBqPtolS56yaDjfGv3kw_003D_003D = _0023_003DqNQGtJl4Z_J440611RR02ZQjNlstLMJASXacu5oPJlAY_003D._0023_003DqnfS_RHumkmeUAypUlxzKYg_003D_003D,
						_0023_003DqCMIzY_bYqX0GeYTa8cWEnaPDJTLKdmL8H9huoN7tXT4_003D = _0023_003DqCMIzY_bYqX0GeYTa8cWEnaPDJTLKdmL8H9huoN7tXT4_003D
					};
				}
				_0023_003DqCMIzY_bYqX0GeYTa8cWEnaPDJTLKdmL8H9huoN7tXT4_003D = !maybe._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D();
			}
			dictionary2[item4.Key] = compiledProgram;
		}
		_0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqfxSWRLuFXHZUSet7MLuQHg_003D_003D(_0023_003DqgNq20zTS18ho0LVvZ88uhQ_003D_003D._0023_003DqfrDV_0024CNeCIILdYiZJ_00241dxw_003D_003D.Count == dictionary2.Count, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850806410));
		return new CompiledProgramGrid(dictionary2);
	}
}
