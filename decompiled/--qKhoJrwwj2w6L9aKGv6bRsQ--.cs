using System.Linq;
using System.Threading;

public sealed class _0023_003DqKhoJrwwj2w6L9aKGv6bRsQ_003D_003D
{
	private static readonly Mutex _0023_003Dq9gzp22LlZ1VdjpLmFILIjvUnxs3TW5LppIRegatPagQ_003D = new Mutex(initiallyOwned: true, _0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825972));

	private static void _0023_003Dq8qlPK5OJXGp8WVnnEoQfoQ_003D_003D(string[] _0023_003DqWMzCf_IVB96OG_0024pZ5wOLQA_003D_003D)
	{
		if (_0023_003DqWMzCf_IVB96OG_0024pZ5wOLQA_003D_003D.Contains(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825863)))
		{
			throw new _0023_003DqRaaOoTBvHvWK2vyz8S665Q_003D_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850825915));
		}
		if (_0023_003DqyBKPxFvFjDnVirfeHoVKCA_003D_003D._0023_003DquwDlEu2YoSRGZrN6ScWMDKn73ay_0024D4B71d5taV4UlSk_003D && !_0023_003Dq9gzp22LlZ1VdjpLmFILIjvUnxs3TW5LppIRegatPagQ_003D.WaitOne(0, exitContext: true))
		{
			return;
		}
		GameLogic gameLogic = new GameLogic();
		gameLogic._0023_003DqdjhIGxIS5szbLbcMYSDeww_003D_003D();
		while (true)
		{
			gameLogic._0023_003DqejGdQbI8sIR7gc8rd2m7xg_003D_003D();
		}
	}
}
