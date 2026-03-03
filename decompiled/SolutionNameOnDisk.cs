public struct SolutionNameOnDisk
{
	public readonly string Prefix;

	public readonly Maybe<int> SerialNumber;

	public SolutionNameOnDisk(string prefix, Maybe<int> serialNumber)
	{
		Prefix = prefix;
		SerialNumber = serialNumber;
	}

	public static SolutionNameOnDisk Parse(string s)
	{
		int num = s.LastIndexOf('-');
		if (num >= 0 && int.TryParse(s.Substring(num + 1), out var result))
		{
			return new SolutionNameOnDisk(s.Substring(0, num), result);
		}
		return new SolutionNameOnDisk(s, _0023_003DqvskaUkCHqK_RGcSVqUS9Zg_003D_003D._0023_003Dqfb_Ox_0024S5BjrBRnY4lWrGlg_003D_003D);
	}

	public override string ToString()
	{
		if (SerialNumber._0023_003DqmCJ_0024iG9vMgP5KlB8KYcHOA_003D_003D())
		{
			return _0023_003Dqi69E34_0024bVVZEaemMAhvEnA_003D_003D._0023_003DqaLxlNh3zbV3vwhaCv1WohavNIW5QQzXk_0024W2hEdysVuc_003D(_0023_003DqfxeyHpgZ3aIFijHrnwYTUUpdAUCJEeTk_0024AUwNN6p03w_003D._0023_003Dq8aGVhgnrQDJe5M_sanyXyg_003D_003D(850830999), new object[2]
			{
				Prefix,
				SerialNumber._0023_003DqYrym_Gw9kA2zlivP68OzUQ_003D_003D()
			});
		}
		return Prefix;
	}
}
