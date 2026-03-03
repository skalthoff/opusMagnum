using System;
using System.Collections.Generic;

internal sealed class _0023_003DqZEd0JXETVp4kEbSXUcTZpA_003D_003D<_0023_003Dq_5wEnuF_0024zbu_0024jDIu4WiYxQ_003D_003D>
{
	public readonly List<_0023_003Dq_5wEnuF_0024zbu_0024jDIu4WiYxQ_003D_003D> _0023_003DqST3paBTFN_YbpB6UsZbojQ_003D_003D = new List<_0023_003Dq_5wEnuF_0024zbu_0024jDIu4WiYxQ_003D_003D>();

	public int _0023_003DqHqBsVE4V9kdJR5GXDV38tA_003D_003D()
	{
		return _0023_003DqST3paBTFN_YbpB6UsZbojQ_003D_003D.Count;
	}

	public void _0023_003Dqy7cJDj6e19IwCrI85Rg1_w_003D_003D(_0023_003Dq_5wEnuF_0024zbu_0024jDIu4WiYxQ_003D_003D _0023_003DqtXAxmvCPsDvlW6jqu_0024d7Bw_003D_003D)
	{
		_0023_003DqST3paBTFN_YbpB6UsZbojQ_003D_003D.Add(_0023_003DqtXAxmvCPsDvlW6jqu_0024d7Bw_003D_003D);
	}

	public _0023_003Dq_5wEnuF_0024zbu_0024jDIu4WiYxQ_003D_003D _0023_003DqVa4dNP_B6NbXWtJkKIsLFA_003D_003D()
	{
		if (_0023_003DqST3paBTFN_YbpB6UsZbojQ_003D_003D.Count == 0)
		{
			throw new InvalidOperationException(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850872941));
		}
		int index = _0023_003DqST3paBTFN_YbpB6UsZbojQ_003D_003D.Count - 1;
		_0023_003Dq_5wEnuF_0024zbu_0024jDIu4WiYxQ_003D_003D result = _0023_003DqST3paBTFN_YbpB6UsZbojQ_003D_003D[index];
		_0023_003DqST3paBTFN_YbpB6UsZbojQ_003D_003D.RemoveAt(index);
		return result;
	}

	public _0023_003Dq_5wEnuF_0024zbu_0024jDIu4WiYxQ_003D_003D _0023_003DqmscHgzQAysi_0024iQTWmOK4Gg_003D_003D()
	{
		if (_0023_003DqST3paBTFN_YbpB6UsZbojQ_003D_003D.Count == 0)
		{
			throw new InvalidOperationException(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850872941));
		}
		return _0023_003DqST3paBTFN_YbpB6UsZbojQ_003D_003D[_0023_003DqST3paBTFN_YbpB6UsZbojQ_003D_003D.Count - 1];
	}
}
